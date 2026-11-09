# Skills vs. Agents: Production AI Architecture

> **Reality Check:** A Markdown file (`SKILL.md`) does not replace an AI Agent. Saying a Skill replaces an Agent is like claiming a recipe book replaces the chef and the kitchen stove.

## The Production Stack (How It Actually Works)

```text
+-------------------------------------------------------------------+
|                   1. AGENT RUNTIME (The Engine)                   |
|   Stateful Execution Loop  ·  Error Retries  ·  Context Memory    |
+---------------------------------+---------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+---------------------------------+     +---------------------------+
|     2. MCP SERVERS (The Hands)  |     | 3. SKILLS (The Playbooks) |
|  Postgres · Stripe · GitHub API |     |  On-Demand Markdown SOPs  |
+---------------------------------+     +---------------------------+
```

## Why "Skills Replace Agents" Collapses in Production

| Engineering Requirement | Static Skill (`.md` File) | Production Agent Runtime |
| :--- | :--- | :--- |
| **Execute Loops & Retries** | `No` (Passive text) | `Yes` (State machine & backoff) |
| **Open Network / DB Sockets** | `No` (Zero I/O capability) | `Yes` (Invokes MCP server tools) |
| **Context Window Efficiency** | `Pollutes context if 500+ dumped` | `Loads 1 scoped playbook on demand` |

## Quick Start

```bash
python token_cost_simulator.py
python agent_runtime.py
```
