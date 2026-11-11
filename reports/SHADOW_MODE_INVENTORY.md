# Shadow / Advisory Mode Inventory (PART 2)

**Date:** 2026-06-19 · Every shadow / advisory / alert-only / review-only / display feature, its current mode, and whether it can affect paper/live now.

Legend — **mode:** shadow (measurement only) · advisory (text/JSON to operator) · display (UI/Telegram wording) · report-only · paper-policy (already-locked routing) · disabled. **before-decision?** = label available at/near decision vs hindsight.

## A. Shadow Intelligence Layer — `src/intelligence/`
| Feature | Location | Mode | Effect | Before-decision? | Affects paper now? | Risk if enabled | Evidence |
|---|---|---|---|---|---|---|---|
| symbol timeline memory | `store.py`/timeline | shadow/display | per-symbol recent-outcome bias label | yes (cached) | no | low (label) | coverage 661 events; outcome sample ~5 |
| derivatives trajectory | `derivatives_trajectory.py` | shadow/display | funding/OI context | yes (cached) | no | low | 69 cached; mostly "unknown" (no history) |
| squeeze phase classifier | `squeeze_phase.py` | shadow/display | build/expansion/unwind/post-unwind-chop | yes (cached) | no | low | 69 cached; outcome sample ~5 |
| thesis / invalidation formatter | `thesis_formatter.py` | advisory/display | compact thesis + invalidation line | yes | no | low | n/a (formatting) |
| on-chain risk interface | `onchain_risk.py` | shadow (interface) | onchain risk score | n/a | no | n/a | `interface_ready_config_missing` (no provider) |

## B. Risk / guard layers — `src/risk/`, `scripts/`
| Feature | Location | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|---|
| circuit breaker | `circuit_breaker.py` + `scripts/circuit_breaker_dry_run.py` | alert-only/dry-run | "would-pause" diagnostic | yes | no | med if made a block | calm window; `would_pause=False`; ~0 fires |
| risk-guard visibility fields | `risk_guards.py` → Control Plane | display | day R / stops / streak / regime fields | yes | no | low | passthrough only |
| intraday risk-off label | `risk_guards.py` | advisory | btc_intraday_risk_off flag | yes | no | low | sample ~5 |
| intraday lifecycle labels | `signals/lifecycle.py` | advisory | aging/carryover/revalidation labels | yes | no | low | label-only |
| sector-cap would-bind | `scripts/sector_cap_forward_tracker.py` | shadow | "would bind" tracker | yes | no | med if a block | sparse fires |
| concentration / correlation cap | `signals/portfolio_caps.py` | shadow | proxy-duplicate / sector-cap shadow | yes | no | med if a block | sparse |
| position/leverage advisor | `risk/position_advisor.py` | label-only | sizing advice label | yes | no | low | label-only |

## C. Execution / lifecycle
| Feature | Location | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|---|
| pending-entry revalidation | `signals/revalidator.py` | tracking | stale_before_entry / entry_moved_away | yes | tracking only | low | already in tracker |
| expired / no-entry split | `status/display_status.py` | **display (LIVE)** | entered-unresolved vs no-entry | yes | no | none | mechanical — done |
| entered-unresolved tracking | `status/display_status.py` | **display (LIVE)** | lifecycle group | yes | no | none | mechanical — done |
| close-alert lifecycle R | `notifiers/close_alert.py` | **display (LIVE)** | sign-aware / "0R unresolved" | yes | no | none | dedup-safe; done |
| paper monitor Telegram status | `scripts/paper_monitor_status.py` | **display (LIVE)** | honest Status block | yes | no | none | wired non-fatal |
| open intraday carryover review | `scripts/open_intraday_lifecycle_review.py` | report-only | carryover/stale review | yes | no | low | report |

## D. Profit protection / exits
| Feature | Location | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|---|
| shadow exit manager / ledger | `exits/shadow_exit_manager.py`, `scripts/shadow_exit_*` | shadow | alt-exit measurement | hindsight (replay) | no | HIGH if made real | 146-trade replay; pessimistic vs real book |
| profit-protection path-aware replay | `reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md` | shadow | BE/partial/trailing sim | hindsight | no | HIGH | net-losing window; relative-only trustworthy |
| BE / partial-TP1 / trailing | shadow configs | shadow | exit variants | hindsight | no | HIGH | not net-positive across regimes |

## E. Playbook / sizing
| Feature | Location | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|---|
| playbook-aware sizing | `signals/sizing.py` + config | label-only/report | size weight label | yes | no | med if real | label-only |
| playbook performance labels | `signals/playbooks.py` | report | per-playbook stats | yes (hist) | no | low | dedup stats |
| crypto scalp | policy | **paper-policy: shadow (locked)** | scalp non-actionable | yes | already off | n/a | 12-mo backtest net-neg |
| stocks intraday C-tier | `signals/tier_policy.py` | **paper-policy: shadow (locked)** | C-tier review-only | yes | already off | n/a | 30d −34R drag |
| stocks swing / invest | policy | **paper-policy: paused/watchlist (locked)** | not actionable | yes | already off | n/a | prior decision |

## F. Catalyst / narrative
| Feature | Location | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|---|
| catalyst integrity monitor | `scripts/catalyst_integrity_scan.py` | alert-only | regression-signature check | yes | no | low | `ok`, none |
| catalyst mapping labels | catalyst layer | advisory | mapped/unmapped coverage | yes | no | low | unmapped-weak warnings |
| analyst-action / no-catalyst labels | catalyst classifier | advisory/display | labels in reports/Telegram | yes | no | low | label-only |
| Telegram catalyst context | notifiers | display | catalyst line in alerts | yes | no | none | done |

## G. Agent Council reason_codes — `~/.claude/scheduled-tasks/.../SKILL.md`
| Feature | Mode | Effect | Before? | Affects paper? | Risk | Evidence |
|---|---|---|---|---|---|---|
| data_quality / market_regime / catalyst_narrative / derivatives_squeeze / technical_entry / execution_lifecycle / risk_manager / playbook_performance / head_trader | **advisory (LIVE, just added)** | reason_codes + JSON in review/Telegram | yes | no | none | 0 reviews yet on new format |

## Summary
- **Already promoted (display/advisory, LIVE):** status taxonomy, expired split, lifecycle R, paper-monitor Telegram, catalyst context, Agent Council reason_codes. None affect paper/live.
- **Shadow / measurement only:** intelligence layer, circuit breaker, sector/concentration caps, shadow exits, profit protection, position advisor.
- **Locked paper-policy (not "promotable" — already decided):** crypto scalp shadow, C-tier shadow, stocks swing/invest pause.
- **Nothing currently affects paper entries except the locked routing policy.**

## Verdict
**SHADOW_MODE_INVENTORY_COMPLETE**
