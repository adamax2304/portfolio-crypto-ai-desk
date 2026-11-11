# Full Post-Weekend System & Trade Audit

**As of:** 2026-06-07 ~13:20 EEST (Sun) · window: weekend (06-05 → 06-07, 72h).
READ-ONLY on strategy/scoring/thresholds. Only technical/audit-script bugs fixed.
Companion files: `SYSTEM_HEALTH_AUDIT_POST_WEEKEND.md`,
`POST_WEEKEND_FIX_VERIFICATION.md`, `NEWS_CATALYST_NARRATIVE_POST_WEEKEND_AUDIT.md`,
`AGENT_SYSTEM_AUDIT_POST_WEEKEND.md`, `POST_WEEKEND_TRADE_UNIVERSE.{csv,md}`,
`POST_WEEKEND_PERFORMANCE_AUDIT.md`, `POST_WEEKEND_TRADE_BY_TRADE_REVIEW.md`,
`POST_WEEKEND_MODE_COMPARISON.md`, `OPUS_POST_WEEKEND_REVIEW_AUDIT.md`.

## 1. Executive summary
- **System healthy; paper trading net positive and improving.** Crypto A/B
  **+16R PF 2.6**, stocks A/B **+6R PF 1.75** over 72h — up from the 48h audit
  (crypto +6R, stocks −15R). Infra stable; all agents and Opus working.
- **Engine:** crypto **shorts +16R PF 3.67** (risk-off tape) + **catalyst-backed
  +9R PF 5.5**; stocks **intraday +10R PF 3.5 WR 71%**.
- **One non-fatal infra issue:** crypto scalp/intraday **report timeouts** on
  daytime cycles (P1). Everything else green.
- **Verdict: SYSTEM_PARTIAL_NEEDS_MINOR_FIXES** (the only "fix" is the infra
  timeout; trading logic is performing).

## 2. System health
All core processes UP: scheduler PID 13864, collector PID 11136 (@sbegemotho, 18
channels), crypto monitor PID 3584, watchlist-monitor task running. Untracked
legacy alerts **0**, bad asset_class **0**, no SQLite locks. Boot-time DLL race
(0xC0000142) self-healed via autostart loop. Stocks correctly idle (weekend).
**Issue:** daytime `crypto scalp/intraday report` TIMEOUT at the 2700s wall
(overnight cycles finish clean). Details: `SYSTEM_HEALTH_AUDIT_POST_WEEKEND.md`.

## 3. Fix verification
All prior fixes still active: squeeze guard wired (0 caps — none qualified),
clean shorts +16R, RS-leaders trading, untracked=0; stocks swing pause (0 new
A/B), market-closed gate (48×), legal gate (9×), Telegram plain-text (**0 post-fix
400s**), A/B-only headline. Details: `POST_WEEKEND_FIX_VERIFICATION.md`.

## 4. News / catalyst / narrative
News flowing (614/24h, 1345/48h, 2304/72h), good source mix + Telegram bridge.
Catalysts persist to `data/catalysts/<date>/*.jsonl` (601 events today). Narratives
sensible (AI/Memes/momentum). **Symbol mapping 26–27% (weak, unchanged — P2).**

## 5. Agent status
All PASS except crypto **report generation** = PARTIAL (timeout). Scanner,
scoring, regime, RS, squeeze guard, shorts, catalyst, tracking, alerts, all stock
gates, and Opus: PASS. Details: `AGENT_SYSTEM_AUDIT_POST_WEEKEND.md`.

## 6. Crypto performance
+16R PF 2.6 WR 50% (33 resolved). Shorts +16R PF 3.67; intraday +10R; swing +9R
(n3); **scalp −3R PF 0.25** (13/28 expired). Catalyst +9R PF 5.5. A-tier: none
produced (risk-off funnel stayed B-tier). 5 active.

## 7. Stocks performance
+6R PF 1.75 WR 56%. Intraday **+10R PF 3.5 WR 71%** (best); shorts +9R; B-tier
+8R PF 2.6; **A-tier −2R PF 0.33** (overpromotion); swing −4R (pre-fix residual,
pause confirmed); invest 0R (6 waiting). C-tier −12R (excluded). 264 active.

## 8. Trade-by-trade findings
94 A/B diagnosed. Crypto losses = late/faded entries + chop (2 thin-alt wick
stops); 7 marginally-tight stops but short book +16R → no geometry change. Stocks
losses = pre-fix swing residual (MFE≈0) + A-tier givebacks (LLY 1R→stop). No
stale/market-closed fills, no catalyst-contradicted winners. Details:
`POST_WEEKEND_TRADE_BY_TRADE_REVIEW.md`.

## 9. Mode comparison
Continue: crypto intraday, crypto swing (small), stocks intraday, shorts
(cross-mode). Stay paused: stocks swing. More data: crypto swing, stocks invest.
Review: crypto scalp (PF 0.25, expire-heavy). Details:
`POST_WEEKEND_MODE_COMPARISON.md`.

## 10. Opus review quality
PASS — every slot ran, market-aware, cited (WebSearch/WebFetch), advisory-only,
caught report staleness + closed-market catalysts. Details:
`OPUS_POST_WEEKEND_REVIEW_AUDIT.md`.

## 11. Root causes of losses (ranked)
| rank | bucket | R | root cause | fixability | overfit risk |
|---|---|---|---|---|---|
| 1 | crypto scalp | −3R | expire/no-fill + faded alt entries (low edge in scalp tf) | medium | medium |
| 2 | stocks A-tier | −2R | A-tier overpromotion (score over-credits) | medium | medium |
| 3 | stocks swing (residual) | −4R | pre-fix longs faded into pullback (already paused) | done | low |
| 4 | crypto longs | 0R | chop in risk-off tape (shorts favored) | low | low |

## 12. What works
Crypto **shorts** (+16R) + **catalyst-backed** (+9R); crypto **intraday**
(+10R); stocks **intraday** (+10R PF 3.5). All safety gates. Swing pause.
Telegram-400 fix. Opus reviews. News/collector. Tracker.

## 13. What does not work / weak
Crypto **scalp** (PF 0.25, expire-heavy). Stocks **A-tier** (PF 0.33). Catalyst
**symbol mapping** (27%). Crypto **report timeout** (infra). Stocks **swing**
(paused, correctly).

## 14. What was fixed during this audit
- **Audit tooling only:** fixed two bugs in my own audit script
  (`_audit_postweekend_tbt.py`: missing `src` path + `ORDER BY` alias). No
  production code touched. (Production schema confirmed fine — catalysts live in
  JSONL, not a DB table; my first query used wrong names.)
- **No production fixes were required** — no production-breaking technical bug
  was found. The timeout is a perf issue needing diagnosis, not a one-line fix.

## 15. What still needs approval (TODOs — NOT implemented)
| ID | P | issue | evidence | proposed fix | risk |
|---|---|---|---|---|---|
| TODO-crypto-report-timeout | **P1** | scalp/intraday report TIMEOUT on daytime cycles | 2700s wall hit; overnight clean | add per-stage timing log to scalp report → find bottleneck; then either raise concurrency in collector or trim deep-scan universe (NOT timeout-bump alone) | low (diag) / medium (scope change) |
| TODO-stocks-atier-promotion | **P1** | A-tier PF 0.33 < B-tier 2.60 (recurring) | 12 A-tier, −2R | scoped study of what over-credits A (score/extension/RS) | medium (touches scoring) |
| TODO-crypto-scalp-review | **P2** | scalp PF 0.25, 13/28 expire/no-fill | mode comparison | tighten scalp entry quality / catalyst-weight; needs more data | medium |
| TODO-catalyst-symbol-mapping | **P2** | 73% catalysts unmapped | 162/601 mapped | improve entity/alias matcher | medium |
| TODO-stocks-chart-ohlcv-path | **P3** | stocks 15m cache not loadable by audit charts | 48 no_ohlcv (audit only) | fix audit loader path | none (tooling) |

## 16. Recommended next steps
1. **Approve the safe diagnostic** for the crypto report timeout (per-stage
   timing log) so we can root-cause without guessing — then act.
2. **Approve a scoped A-tier study** (read-only simulation first, like the
   sector-gate validation) before any scoring change.
3. Keep crypto shorts + catalyst + intraday as the core; keep stocks intraday;
   keep stocks swing paused.
4. Re-audit after the next full RTH week to grow the stock/swing samples.

## Final verdict
```
SYSTEM_PARTIAL_NEEDS_MINOR_FIXES
```
Infra healthy and self-healing, all agents + Opus working, every prior fix
holding, and **paper trading is net positive and improved** (crypto +16R, stocks
+6R). The only blemish is the intermittent crypto report timeout (P1 infra,
non-fatal). No strategy/scoring change was made; the meaningful improvements
(A-tier, scalp, mapping, timeout root-cause) are documented as TODOs awaiting
approval.
