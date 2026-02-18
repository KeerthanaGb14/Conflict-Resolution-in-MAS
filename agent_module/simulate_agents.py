from .agents import create_agents, generate_all_requests, get_agents
from .scenario_runner import resolve_round
from .nswf_interface import send_requests_to_nswf


def run_simulation(rounds=3):
    create_agents()
    agents = get_agents()

    for i in range(rounds):
        print(f"\n=========== ROUND {i+1} ===========")

        reqs = generate_all_requests()
        print("Total requests:", len(reqs))

        # send to NSWF placeholder
        decisions = send_requests_to_nswf(reqs)
        print("Sent to NSWF (placeholder)")

        # local resolver (temporary)
        results = resolve_round(reqs, agents)
        print("Sample results:", list(results.items())[:5])


if __name__ == "__main__":
    run_simulation()
