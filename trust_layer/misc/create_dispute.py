from web3 import Web3
from ipfs_layer.ipfs_client import upload_json
from trust_layer.blockchain_client import create_dispute
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

OWNER_PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"
OWNER = w3.to_checksum_address("0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4")

with open("D:\\Conflict-Resolution-in-MAS\\trust_layer\\hardhat\\artifacts\\contracts\\DisputeManager.sol\\DisputeManager.json") as f:
    artifact = json.load(f)

dispute = w3.eth.contract(
    address=w3.to_checksum_address("0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D"),
    abi=artifact["abi"]
)

conflict_data = {
    "total_resource": 100,
    "requests": [
        {"agent_id": "A", "utility": 15, "urgency": 5, "guilt": 0},
        {"agent_id": "B", "utility": 8, "urgency": 10, "guilt": 1},
        {"agent_id": "C", "utility": 6, "urgency": 9, "guilt": 2}
    ]
}

cid = upload_json(conflict_data)

print("Dispute uploaded to IPFS:", cid)

create_dispute(cid, OWNER_PRIVATE_KEY)
