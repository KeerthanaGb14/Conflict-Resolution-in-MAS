from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict
from web3 import Web3
from trust_layer.blockchain_client import finalize_dispute, set_explanation_cid
from ipfs_layer.ipfs_client import upload_json

app = FastAPI()

AGGREGATOR_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"

# dispute_id -> result_hash -> signatures
signature_pool = defaultdict(lambda: defaultdict(list))
allocation_store = {}

class SignaturePayload(BaseModel):
    dispute_id: int
    result_hash: str
    signature: str
    allocations: dict


@app.post("/submit_signature")
def submit_signature(payload: SignaturePayload):

    dispute_id = payload.dispute_id
    result_hash = payload.result_hash
    signature = payload.signature

    pool = signature_pool[dispute_id][result_hash]

    if signature in pool:
        return {"status": "duplicate"}

    pool.append(signature)
    allocation_store[dispute_id] = payload.allocations

    print(f"Collected {len(pool)}/3 signatures for dispute {dispute_id}")

    if len(pool) >= 3:

        print("Threshold reached. Finalizing on-chain...")

        status = finalize_dispute(
            dispute_id,
            result_hash,
            pool,
            AGGREGATOR_KEY
        )

        if status == 1:
            explanation = {
                "dispute_id": dispute_id,
                "result_hash": result_hash,
                "allocations": allocation_store[dispute_id]
            }

            cid = upload_json(explanation)
            set_explanation_cid(dispute_id, cid, AGGREGATOR_KEY)

            print("Dispute fully resolved.")

            return {"status": "finalized", "cid": cid}

        return {"status": "failed"}

    return {"status": "waiting"}