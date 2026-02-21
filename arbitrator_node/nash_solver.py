from decimal import Decimal, getcontext

# Set high precision to avoid floating drift
getcontext().prec = 28

EPSILON = Decimal("0.000001")


def compute_nsw_allocation(conflict_json: dict) -> dict:
    """
    Deterministic Nash Social Welfare allocation.

    Input:
        {
            "total_resource": R,
            "requests": [
                {
                    "agent_id": str,
                    "utility": float,
                    "urgency": float,
                    "guilt": float
                }
            ]
        }

    Output:
        {
            "allocations": {
                agent_id: allocation_value
            }
        }
    """

    R = Decimal(str(conflict_json["total_resource"]))
    requests = conflict_json["requests"]

    weights = []
    agent_ids = []

    # Step 1 — Compute weights
    for req in requests:
        agent_id = req["agent_id"]
        utility = Decimal(str(req["utility"]))
        urgency = Decimal(str(req["urgency"]))
        guilt = Decimal(str(req.get("guilt", 0)))

        weight = utility + urgency - guilt

        # Clamp to epsilon to avoid zero product
        if weight <= 0:
            weight = EPSILON

        weights.append(weight)
        agent_ids.append(agent_id)

    # Step 2 — Compute total weight
    total_weight = sum(weights)

    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")

    # Step 3 — Compute allocations
    allocations = {}
    running_sum = Decimal("0")

    for i in range(len(weights)):
        if i < len(weights) - 1:
            share = (weights[i] / total_weight) * R
            share = share.quantize(EPSILON)  # deterministic rounding
            allocations[agent_ids[i]] = float(share)
            running_sum += share
        else:
            # Last agent adjustment to ensure exact sum
            final_share = R - running_sum
            final_share = final_share.quantize(EPSILON)
            allocations[agent_ids[i]] = float(final_share)

    return {
        "allocations": allocations
    }
