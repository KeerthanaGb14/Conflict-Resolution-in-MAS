from conflict_engine.decision_engine import resolve_conflict

conflict = {
    "conflict_id": 1,
    "target": "GPU",
    "requests": [
        {
            "agent_id": "A1",
            "request_type": "resource",
            "target": "GPU",
            "utility": 8,
            "urgency": 4,
            "timestamp": 1000,
            "guilt": 1
        },
        {
            "agent_id": "A2",
            "request_type": "resource",
            "target": "GPU",
            "utility": 5,
            "urgency": 2,
            "timestamp": 1001,
            "guilt": 0
        }
    ]
}

decision = resolve_conflict(conflict)
print(decision)
