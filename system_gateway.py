from collections import defaultdict
import time

from agent_module.agents import get_all_requests
from ipfs_layer.ipfs_client import upload_json
from trust_layer.blockchain_client import create_dispute
from conflict_engine.decision_engine import resolve_conflict

OWNER_PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"


def group_by_target(requests):
    grouped = defaultdict(list)
    for r in requests:
        grouped[r["target"]].append(r)
    return grouped


def create_conflict_json(conflict_id, target, requests):
    return {
        "conflict_id": conflict_id,
        "target": target,
        "total_resource": 100,
        "requests": requests
    }


def run_governance_cycle():
    results = []

    requests = get_all_requests()

    if not requests:
        return [{"status": "No requests"}]

    grouped = group_by_target(requests)

    conflict_counter = 1

    for target, reqs in grouped.items():

        if len(reqs) == 1:
            results.append({
                "target": target,
                "status": "Single request — granted locally"
            })
            continue

        conflict_json = create_conflict_json(
            conflict_id=conflict_counter,
            target=target,
            requests=reqs
        )

        decision = resolve_conflict(conflict_json)

        if "rejected" in decision["reason"].lower():
            results.append({
                "target": target,
                "status": "Rejected by policy"
            })
            conflict_counter += 1
            continue

        if decision.get("winner"):
            results.append({
                "target": target,
                "status": f"Winner: {decision['winner']}"
            })
            conflict_counter += 1
            continue

        # Escalate
        cid = upload_json(conflict_json)
        dispute_id = create_dispute(cid, OWNER_PRIVATE_KEY)

        results.append({
            "target": target,
            "status": "Escalated to arbitration",
            "cid": cid,
            "dispute_id": dispute_id
        })

        
        conflict_counter += 1
        time.sleep(1)

    return results


if __name__ == "__main__":
    print(run_governance_cycle())