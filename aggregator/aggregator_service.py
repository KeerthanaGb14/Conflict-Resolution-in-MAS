import threading
from collections import defaultdict

from fastapi import FastAPI
from pydantic import BaseModel
from web3 import Web3
from eth_account.messages import encode_defunct

from trust_layer.blockchain_client import (
    finalize_dispute,
    contract
)
from trust_layer.blockchain_client import w3
import json
import os
from ipfs_layer.ipfs_client import upload_json, fetch_json
from core.result_hash import compute_result_hash  # ✅ shared import
from system_gateway import run_governance_cycle
from explain_module.explainer import generate_deterministic_explanation, generate_explanation

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

app = FastAPI()
lock = threading.Lock()

AGGREGATOR_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"

RPC_URL = "http://127.0.0.1:8545"
CHAIN_ID = 1337
CONTRACT_ADDRESS = contract.address
THRESHOLD = 3


w3 = Web3(Web3.HTTPProvider(RPC_URL))

# dispute_id -> result_hash -> { signer_address: signature }
signature_pool = defaultdict(lambda: defaultdict(dict))

# dispute_id -> verified allocation
allocation_store = {}

# finalized disputes
finalized_disputes = set()

# Load ArbitratorRegistry ABI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

registry_abi_path = os.path.join(
    BASE_DIR,
    "..",
    "trust_layer",
    "hardhat",
    "artifacts",
    "contracts",
    "ArbitratorRegistry.sol",
    "ArbitratorRegistry.json"
)

with open(registry_abi_path) as f:
    registry_json = json.load(f)
    registry_abi = registry_json["abi"]


with open(os.path.join(BASE_DIR, "..", "trust_layer", "DeployedAddresses.json")) as f:
    deployed = json.load(f)

ARBITRATOR_REGISTRY_ADDRESS = deployed["ArbitratorRegistry"]

registry_contract = w3.eth.contract(
    address=ARBITRATOR_REGISTRY_ADDRESS,
    abi=registry_abi
)

class SignaturePayload(BaseModel):
    dispute_id: int
    result_hash: str
    signature: str
    allocations: dict


# ---------------------------------------------------
# SIGNER RECOVERY (MUST MATCH ARBITRATOR)
# ---------------------------------------------------

def recover_signer(dispute_id: int, result_hash: str, signature: str) -> str:

    message = w3.solidity_keccak(
        ["uint256", "address", "uint256", "bytes32"],
        [
            CHAIN_ID,
            CONTRACT_ADDRESS,
            dispute_id,
            Web3.to_bytes(hexstr=result_hash)
        ]
    )

    eth_message = encode_defunct(message)

    return w3.eth.account.recover_message(eth_message, signature=signature)


# ---------------------------------------------------
# API ENDPOINT
# ---------------------------------------------------


@app.post("/submit_signature")
def submit_signature(payload: SignaturePayload):

    dispute_id = payload.dispute_id
    result_hash = payload.result_hash
    signature = payload.signature
    allocations = payload.allocations

    with lock:

        if dispute_id in finalized_disputes:
            return {"status": "already_finalized"}

        # Fetch disputeCID
        try:
            dispute_data = contract.functions.getDispute(dispute_id).call()
            dispute_cid = dispute_data[0]
        except Exception as e:
            print("FETCH ERROR:", e)
            return {"status": "dispute_fetch_failed"}

        computed_hash = compute_result_hash(dispute_cid, allocations)
        if computed_hash != result_hash:
            return {"status": "hash_mismatch"}

        try:
            signer = recover_signer(dispute_id, result_hash, signature)
        except Exception:
            return {"status": "invalid_signature"}

        pool = signature_pool[dispute_id][result_hash]

        if signer in pool:
            return {"status": "duplicate_signer"}

        pool[signer] = signature
        allocation_store[dispute_id] = allocations

       

        # 🔥 ONLY trigger at exact threshold
        if len(pool) == THRESHOLD:

            finalized_disputes.add(dispute_id)

            signatures = list(pool.values())

            # 1️⃣ Get disputeCID from chain
            dispute_data = contract.functions.getDispute(dispute_id).call()
            dispute_cid = dispute_data[0]

            # 2️⃣ Fetch original conflict JSON from IPFS
            try:
                conflict_json = fetch_json(dispute_cid)
            except Exception as e:
                finalized_disputes.remove(dispute_id)
                return {"status": "ipfs_fetch_failed", "error": str(e)}

            # 3️⃣ Generate LLM explanation
            try:
                explanation_text = generate_explanation(conflict_json, allocations)
            except Exception as e:
                print("LLM error:", e)
                explanation_text = generate_deterministic_explanation(conflict_json, allocations)

            # 4️⃣ Prepare explanation payload
            explanation_payload = {
                "dispute_id": dispute_id,
                "conflict_cid": dispute_cid,
                "result_hash": result_hash,
                "total_resource": conflict_json.get("total_resource"),
                "allocations": allocations,
                "explanation": explanation_text,
            }

            # 5️⃣ Upload explanation JSON to IPFS
            explanation_cid = upload_json(explanation_payload)

            # 6️⃣ Store explanation CID on-chain
            tx_result = finalize_dispute(
                dispute_id,
                result_hash,
                explanation_cid,
                signatures,
                AGGREGATOR_KEY
            )

            if tx_result["status"] != 1:
                finalized_disputes.remove(dispute_id)
                return {"status": "finalize_failed"}

            signature_pool.pop(dispute_id, None)
            allocation_store.pop(dispute_id, None)

            return {
                "status": "finalized",
                "explanation_cid": explanation_cid,
                "tx_hash": tx_result["tx_hash"]
            }
        
@app.get("/dashboard_data")
def dashboard_data():

    try:
        arbitrators = registry_contract.functions.getActiveArbitrators().call()
    except:
        arbitrators = []

    try:
        total = contract.functions.disputeCounter().call()
    except:
        total = 0

    active = []
    finalized = {}

    # 🔥 Fetch all finalize events once (not inside loop)
    try:
        finalize_events = contract.events.DisputeFinalized().get_logs(
            from_block=0,
            to_block="latest"
        )
    except:
        finalize_events = []

    # Build quick lookup: disputeId -> (tx_hash, block_number)
    event_lookup = {}
    for event in finalize_events:
        dispute_id = event["args"]["disputeId"]
        event_lookup[dispute_id] = {
            "tx_hash": event["transactionHash"].hex(),
            "block_number": event["blockNumber"]
        }

    for i in range(1, total + 1):
        try:
            dispute = contract.functions.getDispute(i).call()

            dispute_cid = dispute[0]
            result_hash = dispute[1]
            explanation_cid = dispute[2]
            is_finalized = dispute[3]
            exists = dispute[4]

            if not exists:
                continue

            if is_finalized:

                tx_info = event_lookup.get(i, {})

                finalized[i] = {
                    "cid": dispute_cid,
                    "explanation_cid": explanation_cid,
                    "result_hash": result_hash.hex(),
                    "tx_hash": tx_info.get("tx_hash"),
                    "block_number": tx_info.get("block_number")
                }
            else:
                active.append(i)

        except Exception as e:
            print("Dashboard read error:", e)

    return {
        "active_disputes": active,
        "finalized_disputes": finalized,
        "active_arbitrators": arbitrators
    }

@app.post("/run_governance")
def trigger_governance():

    try:
        results = run_governance_cycle()
        return {
            "status": "executed",
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }