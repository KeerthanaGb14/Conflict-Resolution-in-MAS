import time
import os
import requests
from web3 import Web3
from eth_account.messages import encode_defunct

from arbitrator_node.nash_solver import compute_nsw_allocation
from core.result_hash import compute_result_hash
from trust_layer.blockchain_client import contract
from ipfs_layer.ipfs_client import fetch_json


# --------------------------------------------------
# ENV CONFIGURATION
# --------------------------------------------------

PRIVATE_KEY = os.getenv("ARBITRATOR_KEY")
NODE_NAME = os.getenv("ARBITRATOR_NAME", "Arbitrator")

if not PRIVATE_KEY:
    raise Exception("ARBITRATOR_KEY not set")

RPC_URL = "http://127.0.0.1:8545"
CHAIN_ID = 1337
AGGREGATOR_URL = "http://127.0.0.1:8000/submit_signature"


# --------------------------------------------------
# WEB3 SETUP
# --------------------------------------------------

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
CONTRACT_ADDRESS = contract.address

print(f"{NODE_NAME} running: {account.address}")


# --------------------------------------------------
# SIGNATURE GENERATION
# --------------------------------------------------

def sign_message(dispute_id, result_hash):
    message = w3.solidity_keccak(
        ["uint256", "address", "uint256", "bytes32"],
        [
            CHAIN_ID,
            CONTRACT_ADDRESS,
            dispute_id,
            Web3.to_bytes(hexstr=result_hash)
        ]
    )

    eth_message = encode_defunct(message)
    signed = w3.eth.account.sign_message(eth_message, PRIVATE_KEY)

    return signed.signature.hex()


# --------------------------------------------------
# DISPUTE HANDLER
# --------------------------------------------------

def handle_dispute(event):
    try:
        dispute_id = event["args"]["disputeId"]
        dispute_cid = event["args"]["disputeCID"]

        print(f"\n[{NODE_NAME}] New dispute detected: {dispute_id}")

        conflict = fetch_json(dispute_cid)

        result = compute_nsw_allocation(conflict)
        allocations = result["allocations"]

        # Step 1: Deterministic allocation hash
        allocation_hash = compute_result_hash(dispute_cid, allocations)

        print(f"[{NODE_NAME}] Allocation hash: {allocation_hash}")

        # Step 2: Sign structured message
        signature = sign_message(dispute_id, allocation_hash)

        response = requests.post(
            AGGREGATOR_URL,
            json={
                "dispute_id": dispute_id,
                "result_hash": allocation_hash,
                "signature": signature,
                "allocations": allocations
            },
            timeout=10
        )

        print("Aggregator response:", response.json())

    except Exception as e:
        print(f"[{NODE_NAME}] ERROR:", str(e))

# --------------------------------------------------
# EVENT LISTENER
# --------------------------------------------------
def listen():
    print(f"[{NODE_NAME}] Listening for disputes...")

    last_processed_block = w3.eth.block_number

    while True:
        try:
            current_block = w3.eth.block_number

            if current_block >= last_processed_block:

                events = contract.events.DisputeCreated().get_logs(
                    from_block=last_processed_block,
                    to_block=current_block
                )

                for event in events:
                    handle_dispute(event)

                last_processed_block = current_block + 1

            time.sleep(2)

        except Exception as e:
            print(f"[{NODE_NAME}] Listener error:", str(e))
            time.sleep(5)
# --------------------------------------------------

if __name__ == "__main__":
    
    listen()