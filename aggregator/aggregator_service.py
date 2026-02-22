import threading
from collections import defaultdict

from fastapi import FastAPI
from pydantic import BaseModel
from web3 import Web3
from eth_account.messages import encode_defunct

from trust_layer.blockchain_client import (
    finalize_dispute,
    set_explanation_cid,
    contract
)
from ipfs_layer.ipfs_client import upload_json
from core.result_hash import compute_result_hash  # ✅ shared import

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

        # Prevent re-finalization
        if dispute_id in finalized_disputes:
            return {"status": "already_finalized"}

        # Fetch disputeCID from contract
        try:
            dispute_data = contract.functions.getDispute(dispute_id).call()
            dispute_cid = dispute_data[1]  # adjust index if needed
        except Exception:
            return {"status": "dispute_fetch_failed"}

        # Verify deterministic allocation hash
        computed_hash = compute_result_hash(dispute_cid, allocations)

        if computed_hash != result_hash:
            return {"status": "hash_mismatch"}

        # Recover signer
        try:
            signer = recover_signer(dispute_id, result_hash, signature)
        except Exception:
            return {"status": "invalid_signature"}

        # Verify arbitrator registration
        try:
            is_registered = contract.functions.isRegisteredArbitrator(signer).call()
        except Exception:
            return {"status": "registry_check_failed"}

        if not is_registered:
            return {"status": "not_registered_arbitrator"}

        # Group by result_hash
        pool = signature_pool[dispute_id][result_hash]

        if signer in pool:
            return {"status": "duplicate_signer"}

        pool[signer] = signature
        allocation_store[dispute_id] = allocations

        print(f"Collected {len(pool)}/{THRESHOLD} signatures for dispute {dispute_id}")

        # Threshold reached
        if len(pool) >= THRESHOLD:

            print("Threshold reached. Finalizing on-chain...")

            signatures = list(pool.values())

            # Generate explanation (minimal for now)
            explanation = {
                "dispute_id": dispute_id,
                "result_hash": result_hash,
                "allocations": allocations
            }

            cid = upload_json(explanation)

            # Convert CID to bytes32 (store keccak of CID string)
            explanation_cid_hash = Web3.keccak(text=cid).hex()

            status = finalize_dispute(
                dispute_id,
                result_hash,
                explanation_cid_hash,
                signatures,
                AGGREGATOR_KEY
            )

            if status != 1:
                return {"status": "finalize_failed"}

            finalized_disputes.add(dispute_id)

            print("Dispute fully resolved (atomic).")

            print("Dispute fully resolved.")

            # Cleanup
            signature_pool.pop(dispute_id, None)
            allocation_store.pop(dispute_id, None)

            return {"status": "finalized", "cid": cid}

        return {"status": "waiting"}