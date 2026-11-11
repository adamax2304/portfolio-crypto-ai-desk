# Crypto Scalp — Actionable Downgrade Final Decision (PART 6)

**Date:** 2026-06-16
**Basis:** 12-month, 1.55M-candle, 139k-trade scalp historical backtest →
`DISABLE_SCALP_ACTIONABLE_KEEP_SHADOW`
([SCALP_KEEP_REWORK_DISABLE_DECISION.md](SCALP_KEEP_REWORK_DISABLE_DECISION.md)).

## Verdict

```
CRYPTO_SCALP_ACTIONABLE_DOWNGRADED_TO_SHADOW
```

The approved production downgrade is implemented, tested, and verified. Crypto scalp is
now pure shadow/research: generated and tracked, never actionable, never pushed to the
operator as something to mirror.

## Answers

### 1. Is crypto scalp now fully removed from the actionable / manual-shadow flow?

**Yes.**
- **Sizing:** `crypto_scalp_momentum_continuation` weight = **0×** → `sized_r = 0` always;
  it contributes nothing to sized portfolio R / WR / PF.
- **Telegram:** setup alerts remain suppressed; paper-entry and close alerts are
  **`shadow_only`** — `notifier.send` is never called for scalp, so the phone is never
  pinged with an actionable scalp alert.
- **Dashboard:** every scalp row is flagged `🚫 SHADOW ONLY · 0x size · NOT for manual
  live shadow`, scalp is excluded from the cockpit "what to watch" candidate list, and a
  standing forbidden-list entry says "Generated for research only; do NOT mirror
  manually."
- **Journal:** each scalp row carries `actionability = "SHADOW ONLY — research, do not
  mirror"`.

### 2. Does it still run as research / shadow?

**Yes.** Generation, scoring, geometry, tracking, archive, and reports are untouched.
Production still holds 136 crypto scalp signals (latest 2026-06-15T20:24Z), each still
gets a recorded `signal_alerts` row on entry/close (just `shadow_only`), and the gross
entry edge keeps accumulating for a future low-cost rework study. `raw_r` is still
echoed verbatim by the sizing layer, so research dashboards keep the unsized truth.

### 3. Are non-scalp modes unaffected?

**Yes.** Crypto intraday (1.0×), crypto swing (1.0×), crypto failed-bounce short (1.0×),
and stocks intraday (1.0×, A-tier-long 0.5× override) are byte-for-byte unchanged in
config and all still send paper-entry/close Telegram (functionally re-tested + guardrails
`test_5`–`test_8`). Stocks swing/invest stay paused as before. No TP/SL, scoring, tier,
or routing change for any non-scalp mode.

### 4. Is Telegram noise / actionability fixed?

**Yes.** The operator no longer receives any actionable scalp ping. Setup was already
silent; paper-entry and close are now `shadow_only`. If a digest ever renders a scalp
message, it is unambiguously prefixed:

```
[SHADOW ONLY — DO NOT TRADE]
CRYPTO SCALP
Not actionable. Research only.
```

So the structurally-losing setup can never nudge a manual mirror.

### 5. What future research would be required to reconsider scalp?

The backtest pinned the binding constraint as **cost vs tight ATR-distance**, not entry
quality. Re-promotion requires a *cost/instrument* rework that clears the fee hurdle —
**not** another exit/entry-filter tweak (all of those were tested and stay net-negative).
Concretely, before any production re-promotion, a candidate variant must show:

- **net-positive (PF > 1) after realistic 15bps round-trip fees**, simultaneously in
  **TRAIN, VALIDATION, and OOS**, over **≥ 6 months**;
- ideally with **1m intrabar confirmation** of fills/stops;
- via a genuine cost reduction — e.g. **maker-only fills**, **higher-ATR alts / mid-caps**
  (the lowest-ATR majors like BTC were the worst at −1.85R), or **wider stops** that
  shrink the fee-to-edge ratio.

Nothing tested to date meets this bar, so scalp stays shadow until such evidence exists.

## Change surface (complete)

| File | Change |
|------|--------|
| `config/sizing_weights.yaml` | scalp playbook weight `0.5 → 0.0` (+ reason comment) |
| `src/notifiers/paper_entry.py` | `is_shadow_only_scalp` predicate + shadow routing |
| `src/notifiers/close_alert.py` | same predicate + shadow routing |
| `scripts/write_obsidian_current_state_dashboard.py` | scalp SHADOW ONLY banner, cockpit exclusion, forbidden-list entry |
| `scripts/build_live_shadow_journal.py` | `actionability` field |
| `tests/test_scalp_downgrade.py` | 10 new guardrails |
| `tests/test_sizing.py` | reconciled 4 tests to 0× scalp |
| `tests/test_catalyst_safe_fixes.py` | de-flaked time-dependent fixture |

No production order placement, no historical-outcome rewrite, no data deletion, no
scheduler restart.

## Deliverable reports

- [CRYPTO_SCALP_ACTIONABLE_DOWNGRADE_REPORT.md](CRYPTO_SCALP_ACTIONABLE_DOWNGRADE_REPORT.md) (PART 1)
- [CRYPTO_SCALP_TELEGRAM_SHADOW_ONLY_REPORT.md](CRYPTO_SCALP_TELEGRAM_SHADOW_ONLY_REPORT.md) (PART 2)
- [CRYPTO_SCALP_DASHBOARD_SHADOW_LABEL_REPORT.md](CRYPTO_SCALP_DASHBOARD_SHADOW_LABEL_REPORT.md) (PART 3)
- [CRYPTO_SCALP_DOWNGRADE_TEST_RESULTS.md](CRYPTO_SCALP_DOWNGRADE_TEST_RESULTS.md) (PART 4)
- [POST_CRYPTO_SCALP_ACTIONABLE_DOWNGRADE_VERIFICATION.md](POST_CRYPTO_SCALP_ACTIONABLE_DOWNGRADE_VERIFICATION.md) (PART 5)

---

**FINAL ANSWER: `CRYPTO_SCALP_ACTIONABLE_DOWNGRADED_TO_SHADOW`**
