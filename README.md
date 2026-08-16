# Agentic AI-Based Conflict Resolution in Multi-Agent Systems

## Overview

**Agentic AI-Based Conflict Resolution in Multi-Agent Systems** is a framework designed to address conflicts that arise between autonomous agents with competing objectives.

The project combines **Multi-Agent Systems (MAS), Agentic AI, Nash Social Welfare (NSW), Open Policy Agent (OPA), and Blockchain** to create a structured approach for conflict resolution, policy enforcement, and decision auditing.

The core idea is to allow autonomous agents to participate in a conflict-resolution process while separating **agent-level intelligence, policy-based arbitration, and blockchain-based record keeping**.

## Architecture

The system follows a three-layer architecture:

### 1. Off-Chain Intelligence Layer

The intelligence layer consists of autonomous agents that represent different participants in a conflict.

Agents operate with individual objectives and utilities and participate in the conflict-resolution process. Agentic AI is used to model the reasoning and interaction required for reaching a resolution.

### 2. Policy & Arbitration Layer

The policy and arbitration layer is responsible for evaluating proposed decisions and resolving conflicts.

It incorporates:

* **Nash Social Welfare (NSW)** for welfare-oriented resource allocation
* **Open Policy Agent (OPA)** for policy evaluation
* Arbitration logic for resolving conflicts between agents

This layer provides a structured mechanism for evaluating whether an outcome satisfies both the defined policies and the objectives of the participating agents.

### 3. Blockchain & Audit Layer

The blockchain layer provides a mechanism for maintaining an auditable record of arbitration outcomes.

Using blockchain enables important decisions to be recorded in a tamper-resistant manner, supporting transparency and accountability in the conflict-resolution process.

## Nash Social Welfare

Nash Social Welfare is used as the mathematical foundation for evaluating allocations between competing agents.

Instead of optimizing solely for one agent, the approach considers the utilities of multiple agents and aims to identify an allocation that provides a fair balance between their interests.

This makes NSW particularly relevant to multi-agent environments where agents have conflicting preferences over shared resources.

## Policy Enforcement with OPA

**Open Policy Agent (OPA)** is incorporated as the policy enforcement component of the architecture.

Policies can be defined independently from the application logic, allowing proposed decisions to be evaluated against predefined rules before they are accepted as valid outcomes.

This creates a separation between:

**Agent decisions → Policy evaluation → Arbitration**

## Blockchain-Based Accountability

The blockchain component complements the off-chain agent and arbitration processes by providing an immutable record of relevant decisions.

This creates an audit layer for the system, allowing arbitration outcomes to be traced and verified rather than relying entirely on a centralized record.

## Objective

The primary objective of the project is to explore how **autonomous agents with conflicting objectives can reach fair and policy-compliant resolutions through a combination of AI-based agents, welfare optimization, policy enforcement, and blockchain-based auditing**.

## Technology Stack

* Python
* Agentic AI
* Multi-Agent Systems
* Nash Social Welfare
* Open Policy Agent (OPA)
* Blockchain
* Smart Contracts
* Solidity

## Project Repository

https://github.com/KeerthanaGb14/Conflict-Resolution-in-MAS
