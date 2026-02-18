import random
import time
from typing import List, Dict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# =========================
# REAL LLM (Groq)
# =========================

import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192",
    temperature=0.7
)


# =========================
# MEMORY
# =========================
class AgentMemory:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.guilt = 0
        self.history = []

    def update(self, result: str):
        self.history.append(result)
        if result == "lose":
            self.guilt += 1
        elif result == "win":
            self.guilt = max(0, self.guilt - 1)

# =========================
# AGENT
# =========================
class Agent:
    def __init__(self, agent_id: str, visible=False):
        self.agent_id = agent_id
        self.memory = AgentMemory(agent_id)
        self.visible = visible

    # -------- VISIBLE (LLM) --------
    def generate_visible_request(self) -> Dict:
        prompt = f"""
You are agent {self.agent_id} in a multi-agent system.

Generate a request in JSON ONLY.
No explanation text.

Format:
{{
 "request_type": "task/resource/api",
 "target": "API_X or GPU or Task_A",
 "utility": number between 1 and 10,
 "urgency": number between 1 and 5
}}
"""

        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            text = response.content.strip()

            import json
            parsed = json.loads(text)

        except:
            parsed = {
                "request_type": "api",
                "target": "GPU",
                "utility": random.uniform(1,10),
                "urgency": random.randint(1,5),
            }

        return {
            "agent_id": self.agent_id,
            "request_type": parsed["request_type"],
            "target": parsed["target"],
            "utility": float(parsed["utility"]),
            "urgency": int(parsed["urgency"]),
            "timestamp": int(time.time())
        }

    # -------- SIMULATED --------
    def generate_random_request(self) -> Dict:
        targets = ["API_X", "GPU", "Task_A"]
        types = ["task", "resource", "api"]

        return {
            "agent_id": self.agent_id,
            "request_type": random.choice(types),
            "target": random.choice(targets),
            "utility": round(random.uniform(1,10), 2),
            "urgency": random.randint(1,5),
            "timestamp": int(time.time())
        }

    def generate_request(self) -> Dict:
        if self.visible:
            return self.generate_visible_request()
        else:
            return self.generate_random_request()

    def update_memory(self, result: str):
        self.memory.update(result)

# =========================
# CREATE AGENTS
# =========================
visible_agents: List[Agent] = [Agent(f"A{i+1}", visible=True) for i in range(5)]
simulated_agents: List[Agent] = [Agent(f"S{i+1}") for i in range(100)]

all_agents: List[Agent] = visible_agents + simulated_agents

# =========================
# EXPORT FUNCTION
# =========================
def get_all_requests() -> List[Dict]:
    requests = []
    for agent in all_agents:
        requests.append(agent.generate_request())
    return requests
