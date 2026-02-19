def compute_scores(requests: list) -> dict:
    """
    Computes fairness score for each agent.

    score = utility + urgency - guilt
    """

    scores = {}

    for request in requests:
        agent_id = request["agent_id"]
        utility = request["utility"]
        urgency = request["urgency"]
        guilt = request.get("guilt", 0)

        score = utility + urgency - guilt

        scores[agent_id] = score

    return scores
