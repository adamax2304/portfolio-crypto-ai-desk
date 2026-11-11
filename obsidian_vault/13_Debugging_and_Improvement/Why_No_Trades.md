# Why No Trades

A diagnostic for "the desk is showing 0 A/B-tier ideas — should I be worried?"

## The desk is *supposed* to often show no trades

By design, only setups that clear every gate (regime alignment + clean structure + clean invalidation + derivatives confirmation + healthy funding + fresh data + cross-exchange agreement + no rumor cap) become B/A. Many days, especially in `bearish trend`, `range/chop`, `transition`, or `high-volatility danger`, this is zero.

## Diagnostic order

1. **Regime**: open `data/processed/agent_outputs/<latest>_market_regime_agent.json`.
   - `bearish trend` + low breadth → longs muted; expect few longs.
   - `range/chop` → momentum muted; expect few setups overall.
   - `high-volatility danger` → +25 RiskAgent → expect rejections.
2. **Coverage audit**: missing major streams → caps + penalties dominate.
3. **Score caps**: the rejected block shows cap_reasons. If every C/rejected has the same cap (e.g. all MEXC-only), the universe drifted toward discovery.
4. **Universe filters**: re-run `python -m src.cli scan-universe --mode intraday` and check the table. If most candidates have `risk_flags`, the day really is thin.
5. **Stale data**: anything older than 3h triggers cap 50. Run `update-data`.

## Common false alarms

- "I see 0 longs in `bearish trend`." — expected.
- "I see 0 shorts in `bullish trend`." — expected.
- "Every idea is C-tier." — common; the desk waits for confirmation.

## Real problems

- Coverage audit shows anchor (Binance) failed. Fix data first.
- Universe returned 0 candidates. Run `update-universe --market-type spot`.
- Trade-idea agent payload is empty. Check supervisor logs.

## How to act

- If diagnostic shows the desk is correctly being quiet → wait. Do not force trades.
- If diagnostic shows infrastructure failure → fix it, then re-run.

## Related

- [[No_Trade_Conditions]]
- [[Coverage_Audit_Agent]]
- [[Candidate_Debug_Guide]]
- [[Doctor_and_Status]]

## Implemented status

- **Diagnostic guide**.
