import streamlit as st
import requests
import pandas as pd
from web3 import Web3
import os
import sys

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

AGGREGATOR_API = "http://127.0.0.1:8000/dashboard_data"
RPC_URL = "http://127.0.0.1:8545"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

st.set_page_config(page_title="AI Governance Control Panel", layout="wide")

st.title("AI Governance Control Panel")

st.markdown("## Governance Controls")

if st.button("Run Governance Cycle"):

    try:
        response = requests.post("http://127.0.0.1:8000/run_governance", timeout=10)
        result = response.json()

        if result.get("status") == "executed":
            st.success("Governance cycle executed successfully.")
        else:
            st.error(f"Error: {result.get('message')}")

    except Exception as e:
        st.error(f"Backend not reachable: {str(e)}")


st.markdown("---")

# ==================================================
# SECTION 1 — SYSTEM STATUS OVERVIEW
# ==================================================

st.header("System Status Overview")

col1, col2, col3, col4 = st.columns(4)

# Blockchain status
blockchain_status = "Connected" if w3.is_connected() else "Not Connected"

# Fetch dashboard data
try:
    response = requests.get(AGGREGATOR_API, timeout=5)
    data = response.json()
except:
    data = {
        "active_disputes": [],
        "finalized_disputes": {},
        "active_arbitrators": []
    }

active_disputes = data.get("active_disputes", [])
finalized_disputes = data.get("finalized_disputes", {})
active_arbitrators = data.get("active_arbitrators", [])

col1.metric("Active Disputes", len(active_disputes))
col2.metric("Finalized Disputes", len(finalized_disputes))
col3.metric("Active Arbitrators", len(active_arbitrators))
col4.metric("Blockchain", blockchain_status)

st.markdown("---")



# ==================================================
# SECTION 2 — AGENTS RUNNING
# ==================================================

st.header("Agents Running")

try:
    from agent_module.agents import get_all_requests
    requests_data = get_all_requests()
except:
    requests_data = []

if requests_data:
    agents = []
    for r in requests_data:
        agents.append({
            "Agent ID": r.get("agent_id"),
            "Target": r.get("target"),
            "Urgency": r.get("urgency"),
            "Utility": r.get("utility"),
            "Timestamp": r.get("timestamp")
        })

    df_agents = pd.DataFrame(agents)
    st.dataframe(df_agents, use_container_width=True)
else:
    st.info("No active agent requests.")

st.markdown("---")

# ==================================================
# SECTION 3 — ACTIVE DISPUTES
# ==================================================

st.header("Active Disputes")

if active_disputes:
    dispute_rows = []
    for dispute_id in active_disputes:
        dispute_rows.append({
            "Dispute ID": dispute_id,
            "Status": "Waiting Threshold"
        })

    st.dataframe(pd.DataFrame(dispute_rows), use_container_width=True)
else:
    st.success("No active disputes.")

st.markdown("---")

# ==================================================
# SECTION 4 — FINALIZED DISPUTES & EXPLANATION
# ==================================================

st.header("Finalized Disputes")

if finalized_disputes:

    for dispute_id, meta in finalized_disputes.items():

        with st.expander(f"Dispute {dispute_id}"):

            st.subheader("Blockchain Info")
            st.write("Transaction Hash:", meta.get("tx_hash"))
            st.write("Block Number:", meta.get("block_number"))
            st.write("IPFS CID:", meta.get("cid"))

            st.subheader("Final Allocation")

            allocations = meta.get("allocations", {})
            if allocations:
                alloc_df = pd.DataFrame(
                    allocations.items(),
                    columns=["Agent", "Allocated Resource"]
                )
                st.table(alloc_df)

            st.subheader("Explanation")
            st.info("Explanation currently JSON-based. LLM layer coming next.")

else:
    st.info("No finalized disputes yet.")

st.markdown("---")

# ==================================================
# SECTION 5 — REJECTED AGENTS
# ==================================================

st.header("Rejected Requests")

try:
    from conflict_engine.decision_engine import resolve_conflict

    rejected_rows = []

    if requests_data:
        conflict = {
            "conflict_id": 0,
            "target": requests_data[0]["target"],
            "requests": requests_data,
            "total_resource": 100
        }

        result = resolve_conflict(conflict)

        if result.get("rejected_agents"):
            for agent in result["rejected_agents"]:
                rejected_rows.append({
                    "Agent ID": agent,
                    "Reason": result.get("reason")
                })

    if rejected_rows:
        st.table(pd.DataFrame(rejected_rows))
    else:
        st.success("No rejected agents currently.")

except:
    st.info("Policy layer not reachable.")

st.markdown("---")

# ==================================================
# SECTION 6 — ARBITRATOR REGISTRY
# ==================================================

st.header("Arbitrator Registry")

if active_arbitrators:
    arb_df = pd.DataFrame(
        [{"Arbitrator Address": addr, "Status": "Active"} for addr in active_arbitrators]
    )
    st.table(arb_df)
else:
    st.warning("No active arbitrators found.")

st.markdown("---")

# ==================================================
# SECTION 7 — BLOCKCHAIN TRANSACTIONS
# ==================================================

st.header("Blockchain Transactions")

if finalized_disputes:

    tx_rows = []
    for dispute_id, meta in finalized_disputes.items():
        tx_rows.append({
            "Dispute ID": dispute_id,
            "TX Hash": meta.get("tx_hash"),
            "Block": meta.get("block_number"),
            "Status": "Finalized"
        })

    st.table(pd.DataFrame(tx_rows))
else:
    st.info("No blockchain activity yet.")