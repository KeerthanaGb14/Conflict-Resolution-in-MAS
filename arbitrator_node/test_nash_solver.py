from nash_solver import compute_nsw_allocation

conflict = {
    "total_resource": 100,
    "requests": [
        {"agent_id": "A1", "utility": 10, "urgency": 5, "guilt": 1},
        {"agent_id": "A2", "utility": 7, "urgency": 3, "guilt": 0},
        {"agent_id": "A3", "utility": 2, "urgency": 1, "guilt": 0}
    ]
}

result = compute_nsw_allocation(conflict)

print(result)
print("Total:", sum(result["allocations"].values()))
