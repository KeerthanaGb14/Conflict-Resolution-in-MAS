from trust_layer.blockchain_client import create_dispute
from web3 import Web3

# Replace with actual Hardhat private key
PRIVATE_KEY_1 = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

input_hash = Web3.keccak(text="test input")

create_dispute(input_hash, PRIVATE_KEY_1)
