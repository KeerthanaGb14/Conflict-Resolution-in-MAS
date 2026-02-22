from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

with open("hardhat/artifacts/contracts/DisputeManager.sol/DisputeManager.json") as f:
    artifact = json.load(f)

contract = w3.eth.contract(
    address="0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D",
    abi=artifact["abi"]
)

print(contract.functions.disputeCounter().call())
print(contract.functions.disputes(1).call())

# Dispute MetaData
# (
#   disputeCID,
#   finalResultHash,
#   explanationCID,
#   finalized,
#   exists
# )