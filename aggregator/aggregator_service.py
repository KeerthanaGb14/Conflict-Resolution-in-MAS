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
from ipfs_layer.ipfs_client import upload_json
from core.result_hash import compute_result_hash  # ✅ shared import
from system_gateway import run_governance_cycle

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

app = FastAPI()
lock = threading.Lock()
finalized_metadata = {}

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

ARBITRATOR_REGISTRY_ADDRESS = "0x0d5d59ff0C39445c43870516DC1c585D2b09a628"

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

            print(f"Collected {len(pool)}/{THRESHOLD} signatures for dispute {dispute_id}")
            finalized_disputes.add(dispute_id)  # mark BEFORE chain call

            print("Threshold reached. Finalizing on-chain...")

            signatures = list(pool.values())

            explanation = {
                "dispute_id": dispute_id,
                "result_hash": result_hash,
                "allocations": allocations
            }

            cid = upload_json(explanation)

            tx_result = finalize_dispute(
                dispute_id,
                result_hash,
                cid,
                signatures,
                AGGREGATOR_KEY
            )

            if tx_result["status"] != 1:
                finalized_disputes.remove(dispute_id)
                return {"status": "finalize_failed"}

            finalized_metadata[dispute_id] = {
                "tx_hash": tx_result["tx_hash"],
                "block_number": tx_result["block_number"],
                "cid": cid,
                "allocations": allocations
            }

            signature_pool.pop(dispute_id, None)
            allocation_store.pop(dispute_id, None)

            print("Dispute fully resolved (atomic).")

            return {
                "status": "finalized",
                "cid": cid,
                "tx_hash": tx_result["tx_hash"]
            }

        return {"status": "waiting"}
    
@app.get("/dashboard_data")
def dashboard_data():

    try:
        arbitrators = registry_contract.functions.getActiveArbitrators().call()
    except:
        arbitrators = []

    try:
        total = contract.functions.getDisputeCount().call()
    except:
        total = 0

    active = []
    finalized = {}

    for i in range(1, total + 1):
        try:
            dispute = contract.functions.getDispute(i).call()

            dispute_cid = dispute[0]
            is_finalized = dispute[2]   # depends on your struct layout

            if is_finalized:
                finalized[i] = {
                    "status": "Finalized (on-chain)",
                    "cid": dispute_cid
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