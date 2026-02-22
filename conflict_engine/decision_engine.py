import requests
from .gateway import validate_conflict

OPA_BASE_URL = "http://localhost:8181/v1/data/policy"

# --------------------------------------------------
# Individual Policy Check
# --------------------------------------------------

def check_individual_policy(request_data):
    response = requests.post(
        f"{OPA_BASE_URL}/individual/allow",
        json={"input": request_data}
    )
    return response.json().get("result", False)


# --------------------------------------------------
# Collective Policy Check
# --------------------------------------------------

def check_collective_policy(conflict_data):
    response = requests.post(
        f"{OPA_BASE_URL}/collective/allow",
        json={"input": conflict_data}
    )
    return response.json().get("result", False)


# --------------------------------------------------
# Conflict Resolution
# --------------------------------------------------
def resolve_conflict(conflict_json: dict) -> dict:

    validate_conflict(conflict_json)

    conflict_id = conflict_json["conflict_id"]
    target = conflict_json["target"]
    requests_list = conflict_json["requests"]

    valid_requests = []
    rejected_requests = []

    for r in requests_list:
        if check_individual_policy(r):
            valid_requests.append(r)
        else:
            rejected_requests.append(r["agent_id"])

    if len(valid_requests) == 0:
        return {
            "conflict_id": conflict_id,
            "status": "rejected",
            "rejected_agents": rejected_requests,
            "accepted_agents": [],
            "reason": "All requests rejected by individual policy"
        }

    if len(valid_requests) == 1:
        return {
            "conflict_id": conflict_id,
            "status": "granted",
            "winner": valid_requests[0]["agent_id"],
            "rejected_agents": rejected_requests,
            "reason": "Single valid request — granted directly"
        }

    collective_input = {
        "target": target,
        "system_state": {
            "locked": False,
            "resource_disabled": False
        },
        "total_resource": conflict_json.get("total_resource", 0),
        "requests": valid_requests
    }

    if not check_collective_policy(collective_input):
        return {
            "conflict_id": conflict_id,
            "status": "rejected_collective",
            "rejected_agents": [r["agent_id"] for r in valid_requests],
            "reason": "Conflict rejected by collective policy"
        }

    return {
        "conflict_id": conflict_id,
        "status": "escalated",
        "rejected_agents": rejected_requests,
        "accepted_agents": [r["agent_id"] for r in valid_requests],
        "reason": "Escalated to arbitration",
        "requests": valid_requests
    }