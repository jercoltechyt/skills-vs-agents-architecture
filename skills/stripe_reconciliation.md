---
name: stripe-reconciliation
version: 2.1.0
description: Reconcile daily Stripe payout webhooks against PostgreSQL ledger tables.
requires_mcp:
  - supabase-postgres
  - stripe-billing
  - slack-alerts
---

# SOP Playbook: Daily Stripe Payout Reconciliation

## 1. Data Extraction (Requires MCP Tool Binding)
- Invoke MCP tool `supabase.execute_sql` to fetch unsettled payouts for ` CURRENT_DATE - 1 `.
- Invoke MCP tool `stripe.list_balance_transactions` for matching payout batch IDs.

## 2. Deterministic Verification (Requires Subprocess Execution)
- Execute `python verify_ledger_hash.py --strict --tolerance=0.01`.
- Compare SHA-256 settlement digest against local transaction log.

## 3. Exception Recovery & State Loop (Requires Agent Runtime)
- If Stripe API returns `HTTP 502` or rate-limit `429`, **retry up to 3 times** with exponential backoff (`2s, 4s, 8s`).
- If fee discrepancy exceeds `$0.05`, roll back ledger cursor and dispatch P1 alert via `slack.post_message`.
