from web3 import Web3
import json
import os
import time

# Connect to Hardhat node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load ABI directly from Hardhat artifacts


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

abi_path = os.path.join(
    BASE_DIR,
    "hardhat",
    "artifacts",
    "contracts",
    "DecisionLogger.sol",
    "DecisionLogger.json"
)

with open(abi_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]


contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

contract = w3.eth.contract(address=contract_address, abi=abi)

# Use deployer private key (Account #0 from Hardhat node)
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
account = w3.eth.account.from_key(private_key)


def log_decision(dispute_text, winner_address):

    dispute_hash = w3.keccak(text=dispute_text)

    tx = contract.functions.storeDecision(
        dispute_hash,
        winner_address
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 200000,
        "gasPrice": w3.to_wei("2", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Decision stored successfully")
    print("Transaction hash:", tx_hash.hex())

def get_total_decisions():
    total = contract.functions.totalDecisions().call()
    print("Total decisions:", total)

def get_decision(index):
    decision = contract.functions.getDecision(index).call()
    print("Decision:", decision)

if __name__ == "__main__":
    get_total_decisions()
    get_decision(0)

    import time
    log_decision(f"Dispute#{time.time()}", "0x0000000000000000000000000000000000012345")

