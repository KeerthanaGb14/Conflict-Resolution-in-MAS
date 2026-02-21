from web3 import Web3

# Connect to Besu
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Validator details
private_key = "54c11ff248c58765c7a81415a036764dfb3424953f4bc3172c58446862a641ab"
from_address = w3.to_checksum_address("0x3c1c26d3453b7797ebcf302d358ead8a630eba5d")

# To address
to_address = w3.to_checksum_address("0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4")

nonce = w3.eth.get_transaction_count(from_address, "pending")

tx = {
    "nonce": nonce,
    "to": to_address,
    "value": w3.to_wei(200, "ether"),
    "gas": 21000,
    "gasPrice": w3.to_wei("1", "gwei"),
    "chainId": 1337,
}

signed_tx = w3.eth.account.sign_transaction(tx, private_key)

tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Transaction sent!")
print("Tx hash:", tx_hash.hex())