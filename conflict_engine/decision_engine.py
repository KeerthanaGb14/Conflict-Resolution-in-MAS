import requests
from .gateway import validate_conflict

OPA_URL = "http://localhost:8181/v1/data/conflict/allow"

def check_policy(request_data):
    response = requests.post(
        OPA_URL,
        json={"input": request_data}
    )
    return response.json().get("result", False)

def resolve_conflict(conflict_json: dict) -> dict:

    validate_conflict(conflict_json)

    conflict_id = conflict_json["conflict_id"]
    requests = conflict_json["requests"]

    # Check full conflict against OPA
    if not check_policy(conflict_json):
        return {
            "conflict_id": conflict_id,
            "winner": None,
            "losers": [r["agent_id"] for r in requests],
            "reason": "Conflict rejected by organizational policy",
            "scores": {}
        }

    # If policy allows → DO NOT compute winner here
    # Arbitration layer (NSW) will decide

    return {
        "conflict_id": conflict_id,
        "winner": None,
        "losers": [],
        "reason": "Conflict compliant with policy, escalate to arbitration",
        "scores": {}
    }