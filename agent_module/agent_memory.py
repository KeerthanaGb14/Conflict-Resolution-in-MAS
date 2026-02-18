# agent_memory.py

class AgentMemory:
    def __init__(self):
        self.history = []
        self.guilt = 0

    def record(self, result: str):
        self.history.append(result)

        if result == "lose":
            self.guilt += 1
        elif result == "win":
            self.guilt = max(0, self.guilt - 1)

    def get_state(self):
        return {
            "history": self.history[-10:],
            "guilt": self.guilt
        }
