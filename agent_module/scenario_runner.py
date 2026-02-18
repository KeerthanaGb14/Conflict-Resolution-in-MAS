# scenario_runner.py
import random
from collections import defaultdict


def resolve_round(requests, agents):
    target_map = defaultdict(list)

    for r in requests:
        target_map[r["target"]].append(r["agent_id"])

    results = {}

    for target, agent_ids in target_map.items():
        if len(agent_ids) == 1:
            results[agent_ids[0]] = "win"
        else:
            winner = random.choice(agent_ids)
            for a in agent_ids:
                if a == winner:
                    results[a] = "win"
                else:
                    results[a] = "lose"

    for agent in agents:
        if agent.agent_id in results:
            agent.update_memory(results[agent.agent_id])
        else:
            agent.update_memory("neutral")

    return results
