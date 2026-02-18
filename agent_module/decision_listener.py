# decision_listener.py

def apply_decisions_to_agents(agents, decisions):
    """
    decisions: dict {agent_id: 'win'|'lose'|'partial'}
    Updates memory based on NSWF output
    """

    for agent in agents:
        if agent.agent_id in decisions:
            agent.update_memory(decisions[agent.agent_id])
