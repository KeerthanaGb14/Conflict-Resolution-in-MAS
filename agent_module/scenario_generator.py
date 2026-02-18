# scenario_generator.py
import random
from .config import TARGETS


def force_all_conflict(agents, target="GPU"):
    """
    All visible agents request same target
    """
    for agent in agents[:5]:
        agent.last_target = target


def selfish_agent_loop(agents):
    """
    First agent keeps requesting same target
    """
    agents[0].behavior = "selfish"
    agents[0].last_target = random.choice(TARGETS)


def no_conflict_scenario(agents):
    """
    Each visible agent requests different target
    """
    for i, agent in enumerate(agents[:5]):
        agent.last_target = TARGETS[i % len(TARGETS)]
