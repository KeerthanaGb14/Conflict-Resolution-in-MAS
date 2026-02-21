# metrics.py

def count_conflicts(requests):
    targets = {}
    conflicts = 0

    for r in requests:
        t = r["target"]
        targets.setdefault(t, 0)
        targets[t] += 1

    for t in targets:
        if targets[t] > 1:
            conflicts += 1

    return conflicts


def average_guilt(agents):
    if not agents:
        return 0

    total = sum(a.memory.guilt for a in agents)
    return total / len(agents)

# 🟦 MASTER PROMPT — PERSON 1 (FINAL VERSION)
# You are helping me implement the AGENT & SIMULATION module of a multi-agent conflict-resolution system.

# I am Person 1 in a 3-member team.

# We are building everything in parallel, so my code must be integration-ready from the start.

# My module must produce agent requests and simulate conflicts.
# I must NOT build blockchain, UI, or fairness logic.

# The rest of the team depends on my request format, so DO NOT change field names.

# ------------------------------------
# CORE GOAL
# ------------------------------------

# Build a Python module that:

# • creates 5 visible agents  
# • creates 100 simulated agents  
# • generates requests  
# • runs multiple rounds  
# • maintains agent memory  
# • exposes a function other teammates can call  

# The system must run without waiting for other modules.

# ------------------------------------
# STRICT REQUEST FORMAT (DO NOT CHANGE)
# ------------------------------------

# Every request MUST look exactly like this:

# {
#   "agent_id": "A1",
#   "request_type": "task",
#   "target": "API_X",
#   "utility": 7.5,
#   "urgency": 3,
#   "timestamp": 1710000000
# }

# Field rules:
# agent_id → string  
# request_type → "task" | "resource" | "api"  
# target → string  
# utility → float  
# urgency → int  
# timestamp → int  

# No extra keys.
# No renamed fields.

# ------------------------------------
# FILES TO CREATE
# ------------------------------------

# agents.py  
# agent_memory.py  
# simulate_agents.py  
# scenario_runner.py  

# ------------------------------------
# CRITICAL INTEGRATION RULE
# ------------------------------------

# You MUST implement this function in agents.py:

# def get_all_requests() -> list:
#     """
#     Returns list of request dictionaries
#     Used by core engine
#     """

# This is what the rest of the team will import.

# ------------------------------------
# AGENT CLASS
# ------------------------------------

# Each agent must have:

# • agent_id  
# • guilt score  
# • history  

# Methods:
# generate_request()
# update_memory(result)

# Guilt rules:
# +1 guilt when losing  
# reset or reduce when winning  

# ------------------------------------
# VISIBLE AGENTS
# ------------------------------------

# Create 5 visible agents.

# Use simple Python classes first.
# Do NOT deeply integrate LangChain yet.
# LangChain can be added later.

# ------------------------------------
# SIMULATED AGENTS
# ------------------------------------

# Create 100 simulated agents.

# They generate random requests.

# Random choices:

# target:
# ["API_X","GPU","Task_A"]

# request_type:
# ["task","resource","api"]

# utility:
# random float 1–10

# urgency:
# random int 1–5

# ------------------------------------
# SCENARIO GENERATOR
# ------------------------------------

# Create scenarios:

# • conflict: multiple agents same target  
# • non-conflict  
# • repeated selfish agent  
# • mixed targets  

# Run 3 rounds.

# ------------------------------------
# simulate_agents.py
# ------------------------------------

# When running:

# python simulate_agents.py

# It must:

# • create 5 visible agents  
# • create 100 simulated agents  
# • generate requests  
# • print requests  
# • run multiple rounds  
# • show agent state updates  

# ------------------------------------
# OUTPUT REQUIREMENTS
# ------------------------------------

# Running simulate_agents.py should show:

# • request list  
# • conflict scenarios  
# • agent memory updates  

# Also ensure:

# from agents import get_all_requests  
# reqs = get_all_requests()

# returns list of requests.

# ------------------------------------
# IMPORTANT CONSTRAINTS
# ------------------------------------

# Do NOT build:
# • UI  
# • blockchain  
# • fairness engine  
# • policy logic  

# Do NOT rename request fields.

# Keep code simple and modular.

# ------------------------------------
# DELIVERABLE
# ------------------------------------

# Generate complete code for:

# agents.py  
# agent_memory.py  
# simulate_agents.py  
# scenario_runner.py  

# Include instructions to run and test.

# Make sure everything works standalone.


# 🟢 What this revised prompt fixes
# This version ensures Person 1:
# exposes get_all_requests()
# doesn’t block Person 2
# doesn’t overbuild LangChain
# keeps schema frozen
# supports parallel integration
# So while Person 1 builds:
# Person 2 can already build gateway using dummy requests
# Person 3 can build UI/blockchain using dummy decisions
# No waiting.

# 🧠 What Person 1 must confirm after running
# They should be able to run:
# from agents import get_all_requests
# reqs = get_all_requests()
# print(len(reqs))
# print(reqs[0])

# If that works → integration safe.



