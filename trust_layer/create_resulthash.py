from web3 import Web3

result_hash = Web3.keccak(text="NASH_RESULT_TEAM_A_WINS")
print(result_hash.hex())