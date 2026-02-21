from web3 import Web3
from arbitrator_node.nash_solver import compute_nsw_allocation
from arbitrator_node.result_hash import compute_result_hash
from trust_layer.blockchain_client import submit_result

# Replace with your 3 private keys from Hardhat
PRIVATE_KEYS = [
    "0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba",
    "0x92db14e403b83dfe3df233f83dfa3a0d7096f21ca9b0d6d6b8d88b2b4ec1564e",
    "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
]

conflict = {
    "total_resource": 100,
    "requests": [
        {"agent_id": "A1", "utility": 10, "urgency": 5, "guilt": 1},
        {"agent_id": "A2", "utility": 7, "urgency": 3, "guilt": 0},
        {"agent_id": "A3", "utility": 2, "urgency": 1, "guilt": 0}
    ]
}

input_hash = Web3.keccak(text="test input")

result = compute_nsw_allocation(conflict)
allocations = result["allocations"]

result_hash = compute_result_hash(input_hash.hex(), allocations)

print("Result Hash:", result_hash)

for pk in PRIVATE_KEYS:
    submit_result(1, result_hash, pk)
