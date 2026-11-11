# Crypto Quality / Risk Overlay — Deliverable

Date: 2026-07-08 · Scope: **crypto PAPER / read-model / actionability only**. Live / auto-live /
manual-live **LOCKED**. Signal generation, tier, score, TP/SL, `final_r`, `signal_outcomes` untouched.
Every behaviour reversible via `config/crypto_quality_overlay.yaml`.

A soft circuit-breaker that runs **after signal generation, before the paper-entry decision** and routes
a crypto paper candidate to **FULL_SIZE / HALF_SIZE / SHADOW_ONLY / BLOCK** from BTC/ETH regime, session
quality, rolling session + per-symbol cooldowns, open-exposure and entry-mode quality. It only ever
**downgrades** (never upgrades), and **BLOCK is off by default** (`hard_block_enabled: false`) — the
mechanism is HALF / SHADOW.

---

## What was built

| Piece | File |
|---|---|
| Config (all knobs, reversible) | `config/crypto_quality_overlay.yaml` |
| Core overlay (context readers, session, cooldowns, exposure, `evaluate`, live `decide_for_signal`, batch `refresh`, report) | `src/execution/crypto_quality_overlay.py` |
| Counterfactual + weak-session profit-protection sim | `src/execution/crypto_overlay_counterfactual.py` |
| Paper-entry hook (HALF→0.5×, SHADOW/BLOCK→shadow channel) | `src/notifiers/paper_entry.py` |
| CLI: `crypto-quality-refresh`, `crypto-cooldown-refresh`, `crypto-overlay-report` | `src/cli.py` |
| Scheduler: fast cooldown refresh every cycle + heavier counterfactual/report 2×/day | `scripts/run_default_market_schedule.py` |
| Tests (18) | `tests/test_crypto_quality_overlay.py` |

**Additive read-model tables** (self-created; no migration framework): `crypto_quality_overlay_decisions`
(all required diagnostic fields per signal), `crypto_quality_cooldowns` (session + symbol),
`crypto_quality_counterfactual` (baseline vs overlay per closed trade).

**Data sources** (no new network calls): BTC/ETH 15m/1h returns + EMA-slope + trend from cached OHLCV;
regime from `market_dashboard_snapshots.crypto_market_mode`; RVOL from the symbol's OHLCV; OI-change +
funding from `data/raw/{open_interest,funding}/*_latest.json`; spread from the universe cache; session
bucket from UTC hour (Asia/Europe/US/off bands from the 2026-07-06 session audit). **Missing data →
UNKNOWN/MISSING, never "good"**: it lowers `crypto_quality_score` and cannot upgrade a risky entry mode,
but it does **not** blanket-halve a clean primary setup.

---

## The honest finding: calibration matters more than the rules

The counterfactual reconstructs the overlay decision **lookahead-safe** at each closed trade's entry
(BTC/ETH sliced to `created_at`, cooldowns rebuilt from only trades closed before), compares baseline
(full size, actual paper USD) vs overlay (HALF→0.5×, SHADOW/BLOCK→0), and counts winners lost.

**The literal-spec tuning (SHADOW every 2-stop symbol, HALF on any weak/unknown context) STRANGLED the
system and was net-negative** — it kept only **11 / 674** trades at full size, killed **27 / 69 tp3
runners**, and lost **−$720 / −$904 (7d/14d)**. That is the exact failure the task warned against.

**Recalibrated to surgical** (demote on *confirmed* bad-regime evidence, never on *absence of good data*;
symbol cooldown → HALF by default, SHADOW only in a confirmed-weak regime; strong-confirmation bypass):

| window | net Δ USD | PF base → overlay | orig-stop reduction | **missed tp3 runners** | missed winners | kept full |
|---|---|---|---|---|---|---|
| 48h (bad tape) | **+$180** | 0.62 → **0.75** | 4/23 | **0/1** | 0 | 33 |
| 7d | −$96 | 1.38 → **1.44** | 7/65 | **0/23** | 2 | 133 |
| 14d | −$63 | 1.45 → **1.54** | 7/77 | **0/31** | 2 | 160 |
| all (446 USD trades) | −$64 | 1.37 → **1.43** | 10/173 | **0/69** | 2 | 332 |

---

## Success-criteria assessment

- ✅ **Does NOT kill winners** — 0 tp3 runners missed in every window; only 2 winners ever fully dropped.
- ✅ **Improves PF** in every window; strongly protective in the bad 48h window (**+$180**, PF 0.62→0.75).
- ✅ **Trade count falls modestly** (~2–4% shadowed), not strangled — 332/446 kept full size.
- ✅ **Reversible** — every rule gated by `config/crypto_quality_overlay.yaml`; `live_enabled: false` hard-off.
- ⚠️ **Total USD is marginally negative on calm 7d/14d windows (−$96 / −$63, ~5–7% of baseline profit).**
  This is the honest insurance cost of a risk overlay: it halves some winners along with losers. It is
  **PF-positive and runner-safe**, and strongly positive when the tape is bad.

**Recommendation:** ship it **active in paper** (`paper_actionability_enabled: true`) as the requested soft
breaker — it is runner-safe, PF-positive and protective in bad regimes — but treat the marginally-negative
calm-window USD as the reason to **forward-validate before any promotion beyond paper** (live stays locked
regardless). If the operator prefers strict USD-neutrality on calm windows first, set
`paper_actionability_enabled: false` to run it observe-only (decisions still recorded) until a forward
window confirms. The `weak_session_profit_protection_v1` counterfactual is **diagnostic only** and is never
applied to a real exit.

---

## Tests + verification (real DB)

- `tests/test_crypto_quality_overlay.py` — **18 passed**: read-model-only guardrail (no
  `create_order`/`final_r =`/`update signal_outcomes`), `live_enabled` hard-off, missing-data ≠ good,
  LIMIT_THEN_TAKER stays shadow, no global score threshold (65 vs 73 → same action), intraday 66 not
  auto-blocked, BREAKOUT needs strong confirmation, swing ≠ intraday regime guard, exposure downgrades,
  session cooldown on 3 stops, symbol cooldown on 2 stops + strong-confirmation bypass, counterfactual
  avoided-loss / missed-runner, UI `report_data` fields.
- Crypto regression (`paper_entry_alerts` / `scoring` / `supervisor_smoke` / `supervisor_routing` /
  `crypto_scalp_low_confidence` / `intraday_lifecycle`) — **48 passed**. No breakage from the hook.
- Real-DB overlay refresh: 488 recent crypto signals evaluated; cooldowns 306 rows (46 symbols active).
- **Invariants unchanged before/after refresh** — `proposed_signals` 3325, `signal_outcomes` 776811,
  `SUM(final_r)` 927559.0 identical. Only the additive `crypto_quality_*` tables were written.

---

## Diagnostics / UI surface

- `reports/CRYPTO_QUALITY_OVERLAY.md` (decision mix, active cooldowns, avoided-loss vs missed-profit,
  missed runners, weak sessions, worst current symbols, version).
- API-ready JSON: `crypto_quality_overlay.report_data()`; per-signal fields in
  `crypto_quality_overlay_decisions` and carried into the `signal_alerts` payload as `cqo_*`
  (quality_action, verdict, score, btc_regime, session, cooldown states) so the existing per-signal card
  can render them. The **control-plane "Crypto Quality Overlay" card** belongs in the separate
  `trading-desk-control` project (read-only, consuming the above) — flagged as a bounded follow-up.

## Guardrails confirmed
Live LOCKED · no live orders · `final_r` not authoritative-changed · no rewrite of old outcomes · no
destructive migration · all new decisions reversible by config.
