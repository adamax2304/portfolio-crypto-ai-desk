# Crypto Scalp — Dashboard / Journal SHADOW ONLY Labels (PART 3)

**Date:** 2026-06-16

## Goal

Make every crypto-scalp signal self-explanatory in the operator-facing surfaces:
SHADOW ONLY, 0× size, not for manual live shadow, with the reason inline.

## Changes

### 1. Obsidian current-state dashboard — `scripts/write_obsidian_current_state_dashboard.py`

**Per open scalp trade** (`render_open_trade`): a banner line is injected for any
`asset_class='crypto' AND mode='scalp'` row:

```
🚫 SHADOW ONLY · 0x size · NOT for manual live shadow — reason: 12m backtest net-negative after fees
```

Verified in the regenerated page `obsidian_vault/11 📌 Trading Desk Current State.md` —
the banner appears on all 14 currently-open scalp rows.

**Cockpit "what to watch" candidate query:** filtered with
`AND NOT (ps.asset_class='crypto' AND ps.mode='scalp')` so scalp setups are never
surfaced as actionable candidates to mirror.

**Forbidden / caution list** (line ~776): added a standing entry:

```
crypto_scalp_momentum_continuation — SHADOW ONLY (0× sized weight). Generated for
research only; do NOT mirror manually. 12m backtest net-negative after fees —
see reports/SCALP_KEEP_REWORK_DISABLE_DECISION.md
```

This is the required note: **"Crypto scalp remains generated for research only. Do not
mirror manually."**

### 2. Live shadow journal — `scripts/build_live_shadow_journal.py`

Every journal row now carries an explicit `actionability` field:

- crypto scalp → `"SHADOW ONLY — research, do not mirror"`
- everything else → `"actionable"`

So a reader scanning the journal sees the scalp/non-scalp distinction on every row
rather than having to infer it.

## Label coverage matrix

| Surface                         | SHADOW ONLY | 0× size | not for manual shadow | reason shown |
|---------------------------------|:-----------:|:-------:|:---------------------:|:------------:|
| Dashboard — open scalp trade    | ✅ | ✅ | ✅ | ✅ (12m backtest neg after fees) |
| Dashboard — forbidden list      | ✅ | ✅ | ✅ | ✅ (+ link to decision doc) |
| Dashboard — cockpit candidates  | scalp excluded entirely | — | — | — |
| Live shadow journal             | ✅ (`actionability`) | implied (0×) | ✅ | via dashboard/report cross-ref |

## What was NOT changed

- No change to scalp **generation, scoring, geometry, or stored outcomes** — labels are
  presentation-only.
- Non-scalp rows render exactly as before (`actionability="actionable"`, no banner).
- Dashboard regenerates cleanly (`OK — wrote 11 📌 Trading Desk Current State.md`,
  54,991 chars).

**PART 3 status: DONE.**
