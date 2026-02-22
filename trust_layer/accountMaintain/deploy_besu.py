from web3 import Web3
import json
import os

RPC_URL = "http://127.0.0.1:8545"
PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"
DEPLOYER_ADDRESS = "0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_contract_artifact(path):
    with open(path) as f:
        return json.load(f)

def deploy_contract(abi, bytecode, constructor_args=[]):

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx = contract.constructor(*constructor_args).build_transaction({
        "from": DEPLOYER_ADDRESS,
        "nonce": w3.eth.get_transaction_count(DEPLOYER_ADDRESS, "pending"),
        "gas": 5_000_000,
        "gasPrice": w3.to_wei("2", "gwei"),
        "chainId": 1337
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Deployed at:", receipt.contractAddress)
    return receipt.contractAddress


if __name__ == "__main__":

    registry_artifact = load_contract_artifact(
        os.path.join(BASE_DIR, "hardhat", "artifacts", "contracts",
                     "ArbitratorRegistry.sol", "ArbitratorRegistry.json")
    )

    dispute_artifact = load_contract_artifact(
        os.path.join(BASE_DIR, "hardhat", "artifacts", "contracts",
                     "DisputeManager.sol", "DisputeManager.json")
    )

    print("Deploying ArbitratorRegistry...")
    registry_address = deploy_contract(
        registry_artifact["abi"],
        registry_artifact["bytecode"]
    )

    print("Deploying DisputeManager...")
    dispute_address = deploy_contract(
        dispute_artifact["abi"],
        dispute_artifact["bytecode"],
        [registry_address]
    )

    print("\n============================")
    print("ArbitratorRegistry:", registry_address)
    print("DisputeManager:", dispute_address)
    print("============================")