# nswf_interface.py

def send_requests_to_nswf(requests):
    """
    Placeholder for real NSWF integration.
    For now, just returns fake decisions.
    """

    decisions = {}

    for r in requests:
        # simple placeholder rule
        decisions[r["agent_id"]] = "pending"

    return decisions
