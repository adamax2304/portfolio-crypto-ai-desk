# Shadow Mode Registry

> Single source of truth for every shadow / advisory / display / paper-policy feature and its promotion state. Updated by the shadow-promotion audit. **Promotion of any trade-affecting feature requires a dedicated proof report + ≥15 (paper) / ≥30 (production) closed actionable decisions.** Last audit: 2026-06-19 (`reports/FULL_SHADOW_PROMOTION_FINAL_REPORT.md`).
>
> **Machine-readable feature registry:** `config/paper_features.yaml`. **Plain-English implemented/testing/waiting/archived/locked status:** [`CURRENT_TESTING_AND_WAITING_STATE.md`](CURRENT_TESTING_AND_WAITING_STATE.md).

## Promotion states
`LIVE-DISPLAY` · `LIVE-ADVISORY` · `SHADOW` (measurement) · `NEED_MORE_DATA` · `LOCKED-POLICY` (already-decided off) · `INTERFACE-ONLY` · `DISABLED`.

| Feature | State | Affects trades? | Promote when |
|---|---|---|---|
| Safe **max-5x** leverage policy (paper sizing; was 2x, raised 2026-06-24) | LIVE-ADVISORY (paper) | no (paper sizing) | — (active paper; liq kept ≥3× stop) |
| Position lifecycle + partial exits (paper read-model) | LIVE-DISPLAY | no (read-model) | — (active paper; 2026-06-24) |
| Structural stop after TP (paper) | LIVE-ADVISORY (paper) | no | forward structural validation |
| Market dashboard (Opus routine final block) | LIVE-DISPLAY | no | — (active paper; 2026-06-24) |
| Structural TP engine (paper TP-set) | LIVE-ADVISORY (paper) | no (paper TP; prod unchanged) | forward structural re-walk validated → consider production proposal (separate approval) |
| Fee-aware execution skip/cap (paper) | LIVE-ADVISORY (paper) | paper book inclusion only | — (active paper; 2026-06-24) |
| Maker-first execution model (paper) | LIVE-ADVISORY (paper) | no (fee accounting) | forward maker-fill rate matches conservative model |
| Status taxonomy / expired split / entered-unresolved | LIVE-DISPLAY | no | — (done) |
| Close-alert lifecycle R | LIVE-DISPLAY | no | — (done) |
| Paper-monitor Telegram Status | LIVE-DISPLAY | no | — (done) |
| Catalyst context / mapping / analyst labels | LIVE-ADVISORY | no | — (done) |
| Agent Council reason_codes + JSON | LIVE-ADVISORY | no | evaluate reason_code→outcome Friday |
| Symbol timeline / derivatives trajectory / squeeze phase | SHADOW / NEED_MORE_DATA | no | ≥30 closed actionable + net ≥+2R counterfactual, pre-decision only |
| On-chain risk | INTERFACE-ONLY | no | needs provider/contracts config |
| Circuit breaker (as block) | NEED_MORE_DATA | no (alert-only now) | ≥10 real `would_pause` fires evaluated |
| Sector / concentration / correlation caps (as block/size-down) | NEED_MORE_DATA | no (shadow now) | enough binds + net-positive counterfactual |
| Position/leverage advisor | SHADOW (label-only) | no | forward sizing evidence |
| Shadow exits / BE / partial / trailing / profit protection | SHADOW | no | forward (not hindsight) net-positive ≥1 month, both regimes |
| Playbook-aware sizing (as real) | NEED_MORE_DATA | no (report-only) | ≥30 closes per bucket |
| crypto scalp | LOCKED-POLICY (shadow) | off by policy | operator-only, on stronger evidence |
| stocks C-tier intraday | LOCKED-POLICY (shadow) | off by policy | operator-only |
| stocks swing / invest | LOCKED-POLICY (paused) | off by policy | operator-only |

## Rule
No feature in this registry may be moved to a trade-affecting state without: (1) a proof report meeting the gates in `reports/SHADOW_MODE_PROMOTION_DECISIONS.md`, (2) a default-off reversible config flag, (3) paper-only first, (4) explicit operator approval for production. Live / auto-live / exchange execution remain hard-locked regardless.

## Note (2026-06-20) — data/UI correctness ≠ shadow promotion
The POST-DATA-INTEGRITY + APP RESULTS CORRECTION work (canonical `books.py` Operator/Paper/Shadow read-model, economic dedup, honest Today R, Closed-tab redesign, catalyst/regime/delivery/near-winner visibility, Telegram ReadTimeout retry) is **data-integrity + UI correctness only**. It changes how results are *measured and displayed*, not which trades the system takes. No shadow/advisory feature was promoted to a trade-affecting state; the gates above are unchanged. The app's "Shadow Book" is a *display* lane mirroring this registry's shadow features — surfacing it does not enable any of them. See `reports/POST_DATA_INTEGRITY_APP_FIX_FINAL_REPORT.md`.

## Note (2026-06-24) — early-MFE protection graduated to ACTIVE PAPER ACCOUNTING (not a production exit)
The "early MFE-armed protection" (Model F: stop→BE @ +0.6R favorable, lock +0.5R @ +1R, runner TP3) is now the **authoritative paper PnL** (`paper_execution_r`), computed by `src/execution/paper_execution_accounting.py` into the additive `paper_execution_outcomes` table and surfaced in the app/Telegram. This is **accounting/display only** — it does NOT move any real stop, does NOT change the production tracker exits, scoring, entry, routing, or TP/SL generation, and `signal_outcomes.final_r` is never rewritten. Touch-based `final_r` is relabelled "optimistic / signal-quality". Graduating Model F from *paper accounting* to a *paper trade-execution flag* (let alone production) still requires the gates above + sign-off. Live / auto-live / exchange execution remain hard-locked. See `reports/PAPER_RISK_MANAGEMENT_UPGRADE_FINAL_REPORT.md`.

## Note (2026-06-24) — Shadow→Paper promotion audit
Full inventory + promotion audit (`reports/FULL_SHADOW_TO_PAPER_PROMOTION_FINAL_REPORT.md`). Unified registry now lives at `config/paper_features.yaml` (single source of truth, default-safe). Net changes:
- **Promoted to paper DISPLAY-ONLY:** cohort guard `crypto_intraday_catalyst_or_momentum` `off → warn` (dashboard label only, NO routing/actionability change; `paper_review_only` still gated behind `paper_cohort_guard.enabled` + sign-off). New Control Plane **Paper Features panel** (`/api/paper-features`) + per-trade feature tags.
- **ARCHIVED_SUPERSEDED_BY_MODEL_F:** `src/exits/shadow_exit_manager.py` BE/partial/trailing variants A–I (armed at/after TP1, inferior to Model F's +0.6R early protection). Kept for research only; not wired.
- **KEEP_SHADOW / NEED_MORE_DATA (unchanged):** circuit-breaker block, sector/concentration/correlation cap block, position advisor, intelligence layer (timeline/derivatives/squeeze), adaptive TP3.
- **DANGEROUS / LOCKED (unchanged):** crypto scalp, stocks C-tier, stocks swing/invest actionable.
All promotions are PAPER/DISPLAY/ACCOUNTING only — none affect real trades, none enable live/exec, `final_r` is never rewritten.

## Safe observability + DB hygiene pass (2026-06-26)

Observability/diagnostics added; **none change scoring, actionability, thresholds, or final_r; live stays locked; B is not promoted. Forward A/B monitoring continues** (gate NOT_READY, decide on the forward window after ~2–4 weeks).

- **OBSERVABILITY (live):** per-mode A/B breakdown (`/api/paper-shadow/breakdown`, By-mode UI — forward-emphasized, backfill behind a labelled toggle); once-daily Telegram A/B digest (`config/paper_shadow_digest.yaml`, `paper-shadow-digest-send` + scheduler step; best/worst mode, maker fill, gate, look-ahead caveat).
- **DB HYGIENE (ready, not yet run on live):** `signal-outcomes-retention` (per-bar `signal_outcomes` archive→delete; latest row per signal + final outcomes + recent N days always kept; dry-run default).
- **DIAGNOSTIC-ONLY (no production effect):** `catalyst-linkage-shadow-audit` (shadow labels in `catalyst_shadow_audit`; coverage 26.3%→48h 55.1%; **catalyst linkage is diagnostic only, NOT fed to scoring**); `a_tier_strictness` (A correctly rare ~3.78% — caps gate it; **A-tier threshold unchanged**); `stocks_mode_readiness` (swing/intraday = paper_shadow_candidate, scalp/invest = research_only; **stocks scalp/swing/invest remain non-actionable unless separately approved**).
