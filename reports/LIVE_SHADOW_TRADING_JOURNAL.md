# Live Shadow Trading Journal

**Last refresh:** 2026-06-14 17:55 UTC
**Scope:** A/B-tier signals, last 7 days (n=135).
**Manual fields preserved:** 0 (from existing CSV).

Manual columns are operator-owned. The audit script will NEVER overwrite them.

## Schema

| Field | Owner |
|---|---|
| signal_id, asset_class, symbol, direction, mode, playbook, tier, score, size_weight | system |
| paper_entry_price, paper_entry_time, stop, tp1/2/3, current_status, raw_r, sized_r | system |
| telegram_paper_entry_sent, obsidian_visible, rationale_summary, risk_flags | system |
| **manual_decision** (accepted / skipped / watched / rejected_*) | **operator** |
| **manual_fill_price**, **manual_r**, **notes** | **operator** |

## Active / waiting / recent (latest 30)

| Time | Asset | Sym | Dir | Mode | Tier | Status | Raw R | Sized R | TG | Decision |
|---|---|---|---|---|---|---|---:|---:|---|---|
| —                | crypto | OPG/USDT     | long  | intraday | B | waiting_for_entry  |       |  0.00 | no  | — |
| —                | crypto | MEGA/USDT    | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| 2026-06-14T09:45 | crypto | MEGA/USDT    | long  | intraday | B | expired            |  0.00 |  0.00 | yes | — |
| 2026-06-14T02:00 | crypto | OPG/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-14T02:00 | crypto | FET/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-14T02:00 | crypto | WLD/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-14T12:00 | crypto | TAO/USDT     | long  | swing    | B | expired            |  0.00 |  0.00 | yes | — |
| 2026-06-14T02:00 | crypto | PHA/USDT     | long  | swing    | B | expired            |  0.00 |  0.00 | yes | — |
| 2026-06-14T02:00 | crypto | RIF/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-14T01:35 | crypto | RIF/USDT     | long  | scalp    | B | expired            |  0.00 |  0.00 | yes | — |
| —                | crypto | TAO/USDT     | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | RIF/USDT     | long  | swing    | B | entry_moved_away   |       |  0.00 | no  | — |
| —                | crypto | MEGA/USDT    | long  | swing    | B | entry_moved_away   |       |  0.00 | no  | — |
| 2026-06-13T14:00 | crypto | NOT/USDT     | long  | swing    | B | win                |  1.00 |  1.00 | yes | — |
| —                | crypto | MEGA/USDT    | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | RIF/USDT     | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | WLD/USDT     | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | RIF/USDT     | long  | intraday | B | stale_before_entry |       |  0.00 | no  | — |
| 2026-06-13T09:45 | crypto | MEGA/USDT    | long  | intraday | B | loss               | -1.00 | -1.00 | yes | — |
| —                | crypto | AT/USDT      | long  | intraday | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | AT/USDT      | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| —                | crypto | ZBT/USDT     | long  | intraday | B | stale_before_entry |       |  0.00 | no  | — |
| 2026-06-12T18:00 | stocks | AMD          | long  | intraday | A | expired            |  0.00 |  0.00 | yes | — |
| 2026-06-12T18:00 | crypto | ALLO/USDT    | long  | intraday | B | win                |  1.00 |  1.00 | yes | — |
| —                | crypto | ALLO/USDT    | long  | scalp    | B | stale_before_entry |       |  0.00 | no  | — |
| 2026-06-12T17:00 | crypto | ALLO/USDT    | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-12T20:00 | crypto | ENJ/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-12T15:00 | crypto | XPL/USDT     | long  | swing    | B | loss               | -1.00 | -1.00 | yes | — |
| 2026-06-12T15:00 | stocks | JPM          | long  | intraday | B | expired            |  0.00 |  0.00 | yes | — |
| —                | stocks | JPM          | long  | intraday | A | stale_before_entry |       |  0.00 | no  | — |

Full journal CSV: `reports/LIVE_SHADOW_TRADING_JOURNAL.csv` (135 rows).