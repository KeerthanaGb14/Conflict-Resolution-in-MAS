# behaviors.py
import random
from .config import TARGETS, REQUEST_TYPES


def choose_behavior():
    r = random.random()

    if r < 0.2:
        return "selfish"
    elif r < 0.5:
        return "cooperative"
    else:
        return "neutral"


def generate_request_for_behavior(agent):
    behavior = agent.behavior

    # selfish agents repeat same target
    if behavior == "selfish" and agent.last_target:
        target = agent.last_target
    else:
        target = random.choice(TARGETS)

    request_type = random.choice(REQUEST_TYPES)
    utility = round(random.uniform(1, 10), 2)
    urgency = random.randint(1, 5)

    # cooperative agents slightly reduce urgency
    if behavior == "cooperative":
        urgency = max(1, urgency - 1)

    # guilty agents increase urgency
    if agent.memory.guilt > 2:
        urgency = min(5, urgency + 1)

    agent.last_target = target

    return {
        "agent_id": agent.agent_id,
        "request_type": request_type,
        "target": target,
        "utility": utility,
        "urgency": urgency,
        "timestamp": agent.get_timestamp()
    }
