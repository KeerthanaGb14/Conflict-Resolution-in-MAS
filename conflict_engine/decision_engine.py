from .gateway import validate_conflict
from .fairness_engine import compute_scores


def resolve_conflict(conflict_json: dict) -> dict:
    """
    Main integration function.

    Takes conflict JSON from Person 1
    Returns decision JSON for Person 3
    """

    validate_conflict(conflict_json)

    conflict_id = conflict_json["conflict_id"]
    requests = conflict_json["requests"]

    scores = compute_scores(requests)

    max_score = max(scores.values())

    winners = [agent for agent, score in scores.items() if score == max_score]

    if len(winners) == 1:
        winner = winners[0]
        reason = "highest score"
    else:
        earliest = None
        winner = None

        for request in requests:
            if request["agent_id"] in winners:
                if earliest is None or request["timestamp"] < earliest:
                    earliest = request["timestamp"]
                    winner = request["agent_id"]

        reason = "tie resolved by earliest timestamp"

    losers = [req["agent_id"] for req in requests if req["agent_id"] != winner]

    decision = {
        "conflict_id": conflict_id,
        "winner": winner,
        "losers": losers,
        "reason": reason,
        "scores": scores
    }

    return decision
