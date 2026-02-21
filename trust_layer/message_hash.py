from web3 import Web3
from eth_account.messages import encode_defunct

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

chain_id = 1337
contract_address = w3.to_checksum_address("0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D")
dispute_id = 1
result_hash = bytes.fromhex("ea744a337b27cd19f2db490ed7e565c0ef8ef287972728964e8ffbb28f4914bd")

message_hash = Web3.solidity_keccak(
    ["uint256","address","uint256","bytes32"],
    [chain_id, contract_address, dispute_id, result_hash]
)

eth_message = encode_defunct(message_hash)

print("Message hash:", message_hash.hex())