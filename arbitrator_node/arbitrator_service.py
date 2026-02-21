import time
from web3 import Web3
from eth_account.messages import encode_defunct
from arbitrator_node.nash_solver import compute_nsw_allocation
from arbitrator_node.result_hash import compute_result_hash
from trust_layer.blockchain_client import contract
from ipfs_layer.ipfs_client import fetch_json
import requests


PRIVATE_KEY = "7058a80a147ac7ff7d21dc3d1c6ac431c00c5057dcbb2fc7873b7e976ff8cd86"

RPC_URL = "http://127.0.0.1:8545"
CHAIN_ID = 1337

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

CONTRACT_ADDRESS = contract.address

print("Arbitrator running:", account.address)


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

    return signed.signature


def handle_dispute(event):

    dispute_id = event["args"]["disputeId"]
    dispute_cid = event["args"]["disputeCID"]

    print(f"\nNew dispute detected: {dispute_id}")

    print("Processing dispute (any active arbitrator may sign)...")

    conflict = fetch_json(dispute_cid)

    print("Computing NSW allocation...")

    result = compute_nsw_allocation(conflict)
    allocations = result["allocations"]

    result_hash = compute_result_hash(dispute_cid, allocations)

    print("Result hash:", result_hash)

    signature = sign_message(dispute_id, result_hash)

    print("Signature created. Sending to aggregator.")

    response = requests.post(
        "http://127.0.0.1:8000/submit_signature",
        json={
            "dispute_id": dispute_id,
            "result_hash": result_hash,
            "signature": signature.hex(),
            "allocations": allocations
        }
    )

    print("Aggregator response:", response.json())

def listen():

    event_filter = contract.events.DisputeCreated.create_filter(
        from_block="latest"
    )

    print("Listening for disputes...")

    while True:
        for event in event_filter.get_new_entries():
            handle_dispute(event)

        time.sleep(2)


if __name__ == "__main__":
    listen()