from collections import defaultdict
from trust_layer.blockchain_client import finalize_dispute, set_explanation_cid
from ipfs_layer.ipfs_client import upload_json

# Aggregator private key (use owner)
AGGREGATOR_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"

# dispute_id -> { result_hash -> [signatures] }
signature_pool = defaultdict(lambda: defaultdict(list))

# store allocations for explanation
allocation_store = {}

def submit_signature(dispute_id, result_hash, signature, allocations):

    pool = signature_pool[dispute_id][result_hash]

    if signature in pool:
        return

    pool.append(signature)
    allocation_store[dispute_id] = allocations

    print(f"Signature collected ({len(pool)}/3)")

    if len(pool) >= 3:
        print("Threshold reached. Finalizing...")

        status = finalize_dispute(
            dispute_id,
            result_hash,
            pool,
            AGGREGATOR_KEY
        )

        if status == 1:
            print("Finalized successfully. Uploading explanation...")

            explanation = {
                "dispute_id": dispute_id,
                "result_hash": result_hash,
                "allocations": allocation_store[dispute_id]
            }

            cid = upload_json(explanation)

            set_explanation_cid(dispute_id, cid, AGGREGATOR_KEY)

            print("Dispute fully resolved.")