# agents.py
import time
from .agent_memory import AgentMemory
from .config import TARGETS, REQUEST_TYPES, VISIBLE_AGENT_COUNT, SIM_AGENT_COUNT
from .behaviors import choose_behavior, generate_request_for_behavior

_all_agents = []
_last_requests = []


class Agent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory = AgentMemory()
        self.behavior = choose_behavior()
        self.last_target = None

    def get_timestamp(self):
        return int(time.time())

    def generate_request(self):
        return generate_request_for_behavior(self)

    def update_memory(self, result: str):
        self.memory.record(result)

    def get_state(self):
        return {
            "agent_id": self.agent_id,
            "guilt": self.memory.guilt,
            "history": self.memory.history[-5:],
            "behavior": self.behavior
        }


def create_agents():
    global _all_agents
    _all_agents = []

    for i in range(VISIBLE_AGENT_COUNT):
        _all_agents.append(Agent(f"A{i+1}"))

    for i in range(SIM_AGENT_COUNT):
        _all_agents.append(Agent(f"S{i+1}"))


def generate_all_requests():
    global _last_requests
    _last_requests = []

    for agent in _all_agents:
        _last_requests.append(agent.generate_request())

    return _last_requests


def get_agents():
    return _all_agents


def get_all_requests() -> list:
    """
    Returns list of request dictionaries
    Used by other modules
    """
    if not _all_agents:
        create_agents()
    return generate_all_requests()
