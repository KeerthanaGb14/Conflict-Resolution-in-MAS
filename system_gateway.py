from collections import defaultdict
from agent_module.agents import get_all_requests
from ipfs_layer.ipfs_client import upload_json
from trust_layer.blockchain_client import create_dispute
import time

OWNER_PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"

def detect_conflicts(requests):
    """
    Groups requests by target.
    Returns only targets with >1 requests.
    """

    target_map = defaultdict(list)

    for req in requests:
        target_map[req["target"]].append(req)

    conflicts = {}

    for target, reqs in target_map.items():
        if len(reqs) > 1:
            conflicts[target] = reqs

    return conflicts


def create_conflict_json(conflict_id, target, requests):
    return {
        "conflict_id": conflict_id,
        "target": target,
        "total_resource": 100,
        "requests": requests
    }


def main():

    print("\nFetching agent requests...")
    requests = get_all_requests()

    print("Total requests:", len(requests))

    conflicts = detect_conflicts(requests)

    if not conflicts:
        print("No conflicts detected.")
        return

    print(f"Detected {len(conflicts)} conflicts")

    conflict_counter = 1

    for target, reqs in conflicts.items():

        conflict_json = create_conflict_json(
            conflict_id=conflict_counter,
            target=target,
            requests=reqs
        )

        print(f"\nUploading conflict {conflict_counter} to IPFS...")
        cid = upload_json(conflict_json)

        print("CID:", cid)

        print("Creating dispute on blockchain...")
        create_dispute(cid, OWNER_PRIVATE_KEY)

        conflict_counter += 1

        time.sleep(1)


if __name__ == "__main__":
    main()