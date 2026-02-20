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

    approved_agents = []

    for req in requests:
        req.setdefault("guilt", 0)
        if check_policy(req):
            approved_agents.append(req)

    if not approved_agents:
        return {
            "conflict_id": conflict_id,
            "winner": None,
            "losers": [r["agent_id"] for r in requests],
            "reason": "No agent satisfied policy",
            "scores": {}
        }

    winner = max(approved_agents, key=lambda r: r["utility"])

    losers = [r["agent_id"] for r in requests if r["agent_id"] != winner["agent_id"]]

    return {
        "conflict_id": conflict_id,
        "winner": winner["agent_id"],
        "losers": losers,
        "reason": "Approved by OPA policy",
        "scores": {}
    }
