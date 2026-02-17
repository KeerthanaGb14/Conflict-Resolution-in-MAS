import random
import time
from .agent_memory import AgentMemory


TARGETS = ["API_X", "GPU", "Task_A"]
REQUEST_TYPES = ["task", "resource", "api"]

VISIBLE_AGENT_COUNT = 5
SIM_AGENT_COUNT = 100

_all_agents = []
_last_requests = []


class Agent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory = AgentMemory()

    def generate_request(self):
        request = {
            "agent_id": self.agent_id,
            "request_type": random.choice(REQUEST_TYPES),
            "target": random.choice(TARGETS),
            "utility": round(random.uniform(1, 10), 2),
            "urgency": random.randint(1, 5),
            "timestamp": int(time.time())
        }
        return request

    def update_memory(self, result: str):
        self.memory.record(result)

    def get_state(self):
        return {
            "agent_id": self.agent_id,
            "guilt": self.memory.guilt,
            "history": self.memory.history[-5:]
        }


def create_agents():
    global _all_agents
    _all_agents = []

    # 5 visible agents
    for i in range(VISIBLE_AGENT_COUNT):
        _all_agents.append(Agent(f"A{i+1}"))

    # 100 simulated agents
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
    Used by core engine
    """
    if not _all_agents:
        create_agents()
    return generate_all_requests()

