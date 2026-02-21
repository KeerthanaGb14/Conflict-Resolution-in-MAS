from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

OWNER_PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"
OWNER = w3.to_checksum_address("0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4")

with open("D:\\Conflict-Resolution-in-MAS\\trust_layer\\hardhat\\artifacts\\contracts\\DisputeManager.sol\\DisputeManager.json") as f:
    artifact = json.load(f)

contract = w3.eth.contract(
    address=w3.to_checksum_address("0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D"),
    abi=artifact["abi"]
)

dispute_id = 1
result_hash = bytes.fromhex("ea744a337b27cd19f2db490ed7e565c0ef8ef287972728964e8ffbb28f4914bd")

signatures = [
    bytes.fromhex("6420bb30194327d9b5a816146d56a770cf234c4de1d362102ad964f6f5462b5434cf3ac16aa544f06e3aa878b0c1677dcd515a74b8d9954eea580249d4b56bcf1b"),
    bytes.fromhex("3eb0329b3424378cf6892e9d4becfa552968a6b2413582ca30a08788f9186cbd40619044cc8dd10fe9b4ecd13b440b362e7c8e4151f20d0bcc0d92e38cf175e11b"),
    bytes.fromhex("de94b5ef5512a8ae5716683a2768eb7979e9f9fb58c28b58166ad48783cfff520eee36caa4972fb030a51a1acf04a9ce3c6a8168832f48aaf8b235cfbaa620071c")
]

nonce = w3.eth.get_transaction_count(OWNER, "pending")

tx = contract.functions.finalizeDispute(
    dispute_id,
    result_hash,
    signatures
).build_transaction({
    "from": OWNER,
    "nonce": nonce,
    "gas": 500000,
    "gasPrice": w3.to_wei("2", "gwei"),
    "chainId": 1337
})

signed = w3.eth.account.sign_transaction(tx, OWNER_PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Finalize TX:", tx_hash.hex())
print("Status:", receipt.status)