import streamlit as st
import pandas as pd
import random

# ---------------- SAFE IMPORTS ---------------- #

try:
    from agent_module.agents import get_all_requests
except:
    get_all_requests = None

try:
    from conflict_engine.decision_engine import check_policy
except:
    check_policy = None


compute_nsw = None

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="Decentralized AI Governance", layout="wide")
st.title("Decentralized AI Organizational Governance Dashboard")

st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Agents",
        "Conflicts",
        "Policy",
        "Arbitration",
        "Tokens",
        "Workflow"
    ]
)

# ---------------- DUMMY DATA FALLBACK ---------------- #

def dummy_agents():
    return pd.DataFrame({
        "Agent": [f"A{i}" for i in range(1, 6)],
        "Utility": [random.randint(5, 15) for _ in range(5)],
        "Urgency": [random.randint(1, 5) for _ in range(5)],
        "Guilt": [random.randint(0, 3) for _ in range(5)],
        "Tokens": [random.randint(50, 100) for _ in range(5)]
    })

def dummy_conflicts():
    return [
        {
            "conflict_id": 1,
            "target": "GPU",
            "requests": [
                {"agent_id": "A1", "utility": 10, "urgency": 3},
                {"agent_id": "A2", "utility": 8, "urgency": 5}
            ]
        }
    ]

# ---------------- OVERVIEW ---------------- #

if section == "Overview":
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Agents", 105)
    col2.metric("Active Conflicts", 2)
    col3.metric("Resolved Disputes", 5)

# ---------------- AGENTS ---------------- #

if section == "Agents":
    st.header("Agent Behavior")

    agents_df = dummy_agents()
    st.dataframe(agents_df)
    st.bar_chart(agents_df.set_index("Agent")["Utility"])

    st.subheader("Live Agent Requests")

    if get_all_requests:
        try:
            requests = get_all_requests()
            st.json(requests)
        except Exception as e:
            st.error(f"Backend error: {e}")
    else:
        st.warning("Backend not connected. Showing dummy data.")
        st.json(dummy_conflicts())

# ---------------- CONFLICTS ---------------- #

if section == "Conflicts":
    st.header("Conflict Monitoring")

    conflicts = dummy_conflicts()
    for conflict in conflicts:
        st.json(conflict)

# ---------------- POLICY ---------------- #

if section == "Policy":
    st.header("OPA Policy Evaluation")

    conflicts = dummy_conflicts()

    for conflict in conflicts:
        st.subheader(f"Conflict ID: {conflict['conflict_id']}")

        if check_policy:
            try:
                allowed = check_policy(conflict)
                if allowed:
                    st.success("Policy Compliant")
                else:
                    st.error("Rejected by Policy")
            except Exception as e:
                st.error(f"Policy engine error: {e}")
        else:
            st.warning("Policy engine not connected.")
            st.info("Simulated Result: Compliant")

# ---------------- ARBITRATION ---------------- #

if section == "Arbitration":
    st.header("Fairness & NSW Metrics")

    conflict = dummy_conflicts()[0]
    utilities = [r["utility"] for r in conflict["requests"]]

    if compute_nsw:
        try:
            nsw_score = compute_nsw(conflict["requests"])
        except:
            nsw_score = sum(utilities)
    else:
        nsw_score = sum(utilities)

    st.metric("NSW Score", nsw_score)
    st.metric("Total Utility", sum(utilities))

    score_df = pd.DataFrame({
        "Agent": [r["agent_id"] for r in conflict["requests"]],
        "Utility": utilities
    })

    st.bar_chart(score_df.set_index("Agent"))

# ---------------- TOKENS ---------------- #

if section == "Tokens":
    st.header("Token Economy")

    agents_df = dummy_agents()
    st.dataframe(agents_df[["Agent", "Tokens", "Guilt"]])

    st.info("Token slashing occurs when policy violations detected.")

# ---------------- WORKFLOW ---------------- #

if section == "Workflow":
    st.header("Full Dispute Workflow")

    st.write("""
    1️⃣ Agent Generates Request  
    2️⃣ Conflict Detected  
    3️⃣ OPA Policy Check  
    4️⃣ IPFS Storage  
    5️⃣ Blockchain Dispute Creation  
    6️⃣ Arbitrators Compute Nash Social Welfare  
    7️⃣ Aggregator Finalizes  
    8️⃣ Explanation Stored on IPFS  
    """)

    st.success("End-to-End Decentralized Governance Process")
