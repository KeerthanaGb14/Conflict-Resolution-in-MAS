from web3 import Web3
from decimal import Decimal

PRECISION = 6


def canonicalize_allocation(dispute_cid: str, allocations: dict) -> bytes:
    """
    Deterministic format:
    disputeCID|agent1:amount|agent2:amount|...
    """

    sorted_agents = sorted(allocations.keys())
    parts = [dispute_cid]

    for agent in sorted_agents:
        value = Decimal(str(allocations[agent]))
        value_str = format(value, f".{PRECISION}f")
        parts.append(f"{agent}:{value_str}")

    final_string = "|".join(parts)

    return final_string.encode("utf-8")


def compute_result_hash(dispute_cid: str, allocations: dict) -> str:
    canonical_bytes = canonicalize_allocation(dispute_cid, allocations)
    hash_bytes = Web3.keccak(canonical_bytes)
    return hash_bytes.hex()