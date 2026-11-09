# -*- coding: utf-8 -*-
"""
PRODUCTION AGENT STACK: Agent Runtime (Engine) + MCP (Hands) + Skill (Playbook)
"""

import time
from pathlib import Path


class MCPToolClient:
    """The Hands: Deterministic protocol connecting the Agent to external systems."""
    def call_tool(self, server: str, tool: str, payload: dict) -> dict:
        print(f"  [MCP -> {server}] Invoking {tool}({payload})")
        time.sleep(0.15)
        return {"status": "ok", "matched_rows": 142, "delta_usd": 0.00}


class AgentRuntime:
    """The Engine: Manages the execution loop, state memory, retries, and tool calls."""
    def __init__(self, model: str = "gpt-4o-mini", max_retries: int = 3):
        self.model = model
        self.max_retries = max_retries
        self.mcp = MCPToolClient()
        self.state_memory: list[dict] = []

    def load_skill_on_demand(self, skill_slug: str) -> str:
        """The Playbook: Loads ONLY the single Markdown SOP needed for this task."""
        path = Path("skills") / f"{skill_slug}.md"
        playbook = path.read_text(encoding="utf-8")
        print(f"[Agent Runtime] Loaded on-demand playbook: {path.as_posix()} ({len(playbook)} chars)")
        return playbook

    def run_task(self, task: str, skill_slug: str) -> dict:
        print(f"\n[Agent Runtime] Starting stateful loop | Model: {self.model}")
        playbook = self.load_skill_on_demand(skill_slug)

        for attempt in range(1, self.max_retries + 1):
            try:
                res_db = self.mcp.call_tool("supabase-postgres", "execute_sql", {"window": "T-1"})
                res_st = self.mcp.call_tool("stripe-billing", "verify_payouts", {"rows": res_db["matched_rows"]})
                self.state_memory.append({"task": task, "attempt": attempt, "result": res_st})
                print(f"[Agent Runtime] Completed on attempt {attempt}/{self.max_retries} | Delta: ${res_st['delta_usd']:.2f}")
                return res_st
            except RuntimeError as exc:
                print(f"  [Retry {attempt}/{self.max_retries}] Recovering from runtime error: {exc}")
        raise RuntimeError("Max retries exceeded")


if __name__ == "__main__":
    agent = AgentRuntime(model="gpt-4o-mini", max_retries=3)
    agent.run_task(task="Reconcile daily Stripe payouts", skill_slug="stripe_reconciliation")
