
import streamlit as st
import pandas as pd
import random

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
        "Blockchain",
        "Arbitration",
        "Tokens",
        "Workflow"
    ]
)

# Dummy Data (Replace with real backend imports later)
def get_agents():
    return pd.DataFrame({
        "Agent": [f"A{i}" for i in range(1, 6)],
        "Utility": [random.randint(5, 15) for _ in range(5)],
        "Urgency": [random.randint(1, 5) for _ in range(5)],
        "Guilt": [random.randint(0, 3) for _ in range(5)],
        "Tokens": [random.randint(50, 100) for _ in range(5)]
    })

def get_conflicts():
    return pd.DataFrame({
        "Conflict ID": [1, 2],
        "Target": ["GPU", "API_X"],
        "Agents Involved": [3, 2],
        "Status": ["Escalated", "Resolved"]
    })

# ---------------------- Sections ----------------------

if section == "Overview":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Agents", 105)
    col2.metric("Active Conflicts", 2)
    col3.metric("Resolved Disputes", 5)

if section == "Agents":
    st.header("Agent Behavior")
    agents = get_agents()
    st.dataframe(agents)
    st.bar_chart(agents.set_index("Agent")["Utility"])

if section == "Conflicts":
    st.header("Conflict Monitoring")
    conflicts = get_conflicts()
    st.dataframe(conflicts)

if section == "Policy":
    st.header("OPA Policy Decisions")
    st.success("Conflict 1: Policy Compliant")
    st.error("Conflict 2: Rejected by Policy Rule")

if section == "Blockchain":
    st.header("Blockchain Dispute Lifecycle")
    st.write({
        "Dispute ID": 1,
        "CID": "QmExampleCID123",
        "Block Number": 152,
        "Status": "Finalized"
    })

if section == "Arbitration":
    st.header("Fairness & NSW Metrics")
    st.metric("NSW Score", 72)
    st.metric("Total Utility", 18)
    st.metric("Gini Coefficient", 0.12)

if section == "Tokens":
    st.header("Token Economy")
    agents = get_agents()
    st.dataframe(agents[["Agent", "Tokens", "Guilt"]])

if section == "Workflow":
    st.header("Full Dispute Workflow")
    st.write("""
    1. Agent Generates Request  
    2. Conflict Detected  
    3. OPA Policy Check  
    4. IPFS Storage  
    5. Blockchain Dispute Creation  
    6. Arbitrators Compute NSW  
    7. Aggregator Finalizes  
    8. Explanation Stored on IPFS  
    """)
