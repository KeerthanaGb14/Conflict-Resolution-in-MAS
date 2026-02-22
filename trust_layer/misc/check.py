from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

with open("D:\\Conflict-Resolution-in-MAS\\trust_layer\\hardhat\\artifacts\\contracts\\DisputeManager.sol\\DisputeManager.json") as f:
    artifact = json.load(f)

contract = w3.eth.contract(
    address="0x56CA4Dc4cbd37456adFe20238c23dAEfD690dCc5",
    abi=artifact["abi"]
)

print("Connected:", w3.is_connected())
print("Chain ID:", w3.eth.chain_id)
print("Block:", w3.eth.block_number)

# Dispute MetaData
# (
#   disputeCID,
#   finalResultHash,
#   explanationCID,
#   finalized,
#   exists
# )