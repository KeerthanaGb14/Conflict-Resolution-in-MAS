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

    # -------------------------------
    # STEP 1: Individual Filtering
    # -------------------------------

    valid_requests = []
    rejected_requests = []

    for r in requests_list:
        if check_individual_policy(r):
            valid_requests.append(r)
        else:
            rejected_requests.append(r["agent_id"])

    # If all rejected → stop
    if len(valid_requests) == 0:
        return {
            "conflict_id": conflict_id,
            "winner": None,
            "losers": rejected_requests,
            "reason": "All requests rejected by individual policy",
            "scores": {}
        }

    # -------------------------------
    # STEP 2: Single Request Case
    # -------------------------------

    if len(valid_requests) == 1:
        return {
            "conflict_id": conflict_id,
            "winner": valid_requests[0]["agent_id"],
            "losers": rejected_requests,
            "reason": "Single valid request — granted directly",
            "scores": {}
        }

    # -------------------------------
    # STEP 3: Collective Policy Check
    # -------------------------------

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
            "winner": None,
            "losers": [r["agent_id"] for r in valid_requests],
            "reason": "Conflict rejected by collective policy",
            "scores": {}
        }

    # -------------------------------
    # STEP 4: Escalate to Arbitration
    # -------------------------------

    return {
        "conflict_id": conflict_id,
        "winner": None,
        "losers": [],
        "reason": "Conflict compliant with policy — escalate to arbitration",
        "scores": {},
        "requests": valid_requests
    }