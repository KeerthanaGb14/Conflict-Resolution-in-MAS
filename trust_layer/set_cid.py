from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

OWNER_PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"
OWNER = w3.to_checksum_address("0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4")

CONTRACT_ADDRESS = w3.to_checksum_address("0xbdDB6221AAd47bA3A9ec2E67142e21843a0cE04D")

with open("hardhat/artifacts/contracts/DisputeManager.sol/DisputeManager.json") as f:
    artifact = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=artifact["abi"])

dispute_id = 1
cid = "Qmch6Ex3LP8f9WsiEkfeaZZhXMq63Y5fXTcMayZZAm3jst"   # <-- replace

nonce = w3.eth.get_transaction_count(OWNER, "pending")

tx = contract.functions.setExplanationCID(
    dispute_id,
    cid
).build_transaction({
    "from": OWNER,
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("2", "gwei"),
    "chainId": 1337
})

signed = w3.eth.account.sign_transaction(tx, OWNER_PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("CID stored TX:", tx_hash.hex())
print("Status:", receipt.status)