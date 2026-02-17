from .agents import create_agents, generate_all_requests, get_agents
from .scenario_runner import resolve_round


def print_requests(reqs):
    print("\n--- REQUESTS ---")
    for r in reqs[:10]:
        print(r)
    print(f"... total: {len(reqs)}")


def print_agent_states(agents):
    print("\n--- AGENT STATES (first 10) ---")
    for a in agents[:10]:
        print(a.get_state())


def run_simulation(rounds=3):
    create_agents()
    agents = get_agents()

    for i in range(rounds):
        print(f"\n================ ROUND {i+1} ================")

        reqs = generate_all_requests()
        print_requests(reqs)

        results = resolve_round(reqs, agents)

        print("\nConflicts resolved:")
        for k in list(results.keys())[:10]:
            print(k, "→", results[k])

        print_agent_states(agents)


if __name__ == "__main__":
    run_simulation()
