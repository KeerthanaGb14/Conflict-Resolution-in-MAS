from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

PRIVATE_KEY = "8ab3f3dffd3548cd3cdfe8f5972886d12073053a773d5bbfe444fbbe23888153"
OWNER = w3.to_checksum_address("0x091d58dd0F8ed75D9927Ef3bD0b13d8922D701F4")

with open("D:\\Conflict-Resolution-in-MAS\\trust_layer\\hardhat\\artifacts\\contracts\\ArbitratorRegistry.sol\\ArbitratorRegistry.json") as f:
    artifact = json.load(f)

registry = w3.eth.contract(
    address=w3.to_checksum_address("0x5c20bf69785e830b0Cd6Ed96E02fABD918d3D90D"),
    abi=artifact["abi"]
)

arbitrators = [
    "0x6D0c69e33FaC23a8D2D5E881F873630E1fEEed7c",
    "0x2Ed1cceA354691774a8630694E174a54Ac7be93f",
    "0xB4516df9E61e3e93Bb5F91f776627AD628040885",
    "0x53e0Db18A80D818FCEb028F4a4b1854A45e0Fab2",
    "0x3dC3134364037102262a1AD737DDcc6d8f564eA5"
]

nonce = w3.eth.get_transaction_count(OWNER, "pending")

for arb in arbitrators:
    tx = registry.functions.registerArbitrator(
        w3.to_checksum_address(arb)
    ).build_transaction({
        "from": OWNER,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("2", "gwei"),
        "chainId": 1337
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Registered:", arb)

    nonce += 1