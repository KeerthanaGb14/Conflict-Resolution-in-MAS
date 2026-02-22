from web3 import Web3
from eth_account.messages import encode_defunct

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

chain_id = 1337
contract_address = w3.to_checksum_address("0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D")
dispute_id = 1
result_hash = bytes.fromhex("ea744a337b27cd19f2db490ed7e565c0ef8ef287972728964e8ffbb28f4914bd")

# EXACT SAME encoding as Solidity abi.encodePacked
message = w3.solidity_keccak(
    ["uint256", "address", "uint256", "bytes32"],
    [chain_id, contract_address, dispute_id, result_hash]
)

print("Raw message:", message.hex())

eth_message = encode_defunct(message)

arbitrator_keys = [
    "367163b668653fb5858c37ac77a8bcc914ccf3d473026f9d61a4610747f01764",
    "bf6448b09c18013c367e2887ba1a55189435f73fa2a0fd19b46a37e895c5da39",
    "7058a80a147ac7ff7d21dc3d1c6ac431c00c5057dcbb2fc7873b7e976ff8cd86"
]

for key in arbitrator_keys:
    signed = w3.eth.account.sign_message(eth_message, private_key=key)
    print("Signature:", signed.signature.hex())