from web3 import Web3
import json
import os


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

abi_path = os.path.join(
    BASE_DIR,
    "hardhat",
    "artifacts",
    "contracts",
    "DisputeManager.sol",
    "DisputeManager.json"
)

with open(abi_path) as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

DISPUTE_MANAGER_ADDRESS = "0x56CA4Dc4cbd37456adFe20238c23dAEfD690dCc5"

contract = w3.eth.contract(
    address=DISPUTE_MANAGER_ADDRESS,
    abi=abi
)


def create_dispute(dispute_cid, private_key):

    local_account = w3.eth.account.from_key(private_key)

    nonce = w3.eth.get_transaction_count(local_account.address, "pending")

    tx = contract.functions.createDispute(dispute_cid).build_transaction({
        "from": local_account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("2", "gwei"),
        "chainId": 1337
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status != 1:
        raise Exception("Dispute creation failed")

    print(f"Dispute created by {local_account.address}: {tx_hash.hex()}")

    # 🔥 Extract dispute_id from event log
    logs = contract.events.DisputeCreated().process_receipt(receipt)

    dispute_id = logs[0]["args"]["disputeId"]

    return dispute_id
def finalize_dispute(dispute_id, result_hash, explanation_cid, signatures, private_key):

    local_account = w3.eth.account.from_key(private_key)

    tx = contract.functions.finalizeDispute(
        dispute_id,
        Web3.to_bytes(hexstr=result_hash),
        explanation_cid,  # <-- now string
        [Web3.to_bytes(hexstr=s) for s in signatures]
    ).build_transaction({
        "from": local_account.address,
        "nonce": w3.eth.get_transaction_count(local_account.address, "pending"),
        "gas": 1500000,
        "gasPrice": w3.to_wei("2", "gwei"),
        "chainId": 1337
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Finalize TX:", tx_hash.hex())
    return {
        "status": receipt.status,
        "tx_hash": tx_hash.hex(),
        "block_number": receipt.blockNumber
    }