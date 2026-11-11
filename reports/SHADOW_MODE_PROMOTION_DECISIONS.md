# Shadow Mode Promotion Decisions (PART 5)

**Date:** 2026-06-19 · Gates applied strictly. Actionable closed sample = **5** (< 15, < 30) ⇒ no trade-affecting feature can clear PROMOTE_NOW or PROMOTE_PAPER_ONLY this window.

| Feature | Decision | Sample | Reason | Expected effect | Risk | Action |
|---|---|---|---|---|---|---|
| Status taxonomy / expired split / entered-unresolved | **PROMOTE_NOW (already LIVE)** | n/a (mechanical) | display correctness, tests pass, 0 trade effect | removes operator confusion | none | already implemented; keep |
| Close-alert lifecycle R | **PROMOTE_NOW (already LIVE)** | n/a | dedup-safe display fix | honest R wording | none | keep |
| Paper-monitor Telegram Status | **PROMOTE_NOW (already LIVE)** | n/a | honest status counts | clarity | none | keep (non-fatal step) |
| Catalyst context / mapping / analyst labels | **PROMOTE_NOW (already LIVE, advisory)** | n/a | label/advisory only | richer context | none | keep |
| Agent Council reason_codes + JSON | **PROMOTE_NOW (already LIVE, advisory)** | 0 reviews yet | advisory text/JSON, no trade effect | structured reviews | none | keep; evaluate predictiveness Friday |
| Symbol timeline / derivatives trajectory / squeeze phase | **KEEP_SHADOW / NEED_MORE_DATA** | ~3–5 | predictive value uncomputable; derivatives sparse | would gate entries | med if gated | stay display/advisory; revisit ≥30 |
| On-chain risk interface | **KEEP_SHADOW** | 0 | `interface_ready_config_missing` (no provider) | none | n/a | stays interface-only |
| Circuit breaker (as a block) | **NEED_MORE_DATA** | ~0 fires | calm window, no fires to judge | would pause trading | med | stays alert-only/dry-run |
| Sector / concentration / correlation caps (as blocks) | **NEED_MORE_DATA** | sparse | almost no binds in window | would block/size-down | med | stay shadow trackers |
| Position/leverage advisor | **KEEP_SHADOW** | n/a | label-only, no forward sizing evidence | sizing advice | low | stay label-only |
| Shadow exits / BE / partial / trailing / profit protection | **KEEP_SHADOW** | post_factum | hindsight replay, net-losing window, pessimistic vs real book | exit changes | **HIGH** | stay shadow; never auto |
| Playbook-aware sizing (as real) | **NEED_MORE_DATA** | 5 | too few closes; would change size | sizing | med | report/label only |
| crypto scalp / C-tier / stocks swing-invest | **KEEP_SHADOW (locked policy)** | (prior multi-week) | already decided off on stronger evidence | n/a | n/a | unchanged |
| Anything noisy to disable | **none DISABLE_OR_HIDE** | — | no shadow module is spamming; onchain is silent-by-design | — | — | nothing to hide |

## Summary
- **PROMOTE_NOW:** only the **display/advisory** features — and they are **already LIVE** from prior sessions. **No new code needed.**
- **NEED_MORE_DATA / KEEP_SHADOW:** every trade-affecting feature (intelligence gates, circuit breaker block, caps, sizing, profit protection/exits). Reason: 5 closed actionable decisions ≪ 15/30 gate.
- **DISABLE_OR_HIDE:** none — nothing is noisy; onchain is intentionally silent until config exists.

## Verdict
**PROMOTION_DECISIONS_READY** — safe (display/advisory) features already promoted; all trade-affecting features held at NEED_MORE_DATA / KEEP_SHADOW on sample-size grounds.
