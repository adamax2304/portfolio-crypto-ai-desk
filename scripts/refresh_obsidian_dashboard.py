"""Refresh the 11 pinned dashboard files at the Obsidian vault root.

Generates these files (each prefixed with 📌 so they cluster at the top
of Obsidian's file explorer):

    00 📌 Dashboard.md             — top-level Map of Content
    01 📌 Active Signals.md        — current B/A waiting_for_entry / triggered
    02 📌 Trade History.md         — completed signals with outcomes
    03 📌 Todays Catalysts.md      — fresh catalyst events + narrative baskets
    04 📌 Latest Reports.md        — newest scalp / intraday / stocks reports
    05 📌 Opus Auto Reviews.md     — index of OPUS_ENRICHED_REVIEW_AUTO_*.md
    06 📌 Telegram Feed.md         — latest 50 Telegram channel news rows
    07 📌 Schedule Status.md       — scheduler / collector / monitor health
    08 📌 Rejected Ideas.md        — what the system rejected and why (last 48h)
    09 📌 Macro Risk Heatmap.md    — risk-on/risk-off score + headlines
    10 📌 Performance by Mode.md   — signal-stats breakdown per mode and tier
    11 📌 Trading Desk Current State.md
                                   — single-screen sweep (health → live trades →
                                     last 5 → events → risks → routing → perf)

The script is pure read + Markdown write. It never touches SQLite write
paths, never modifies scoring / agents / strategy, and never sends
Telegram. Safe to run at the tail of every scheduler cycle.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import load_config  # noqa: E402

VAULT = PROJECT_ROOT / "obsidian_vault"
EEST_NAME = "Europe/Athens"  # EEST in practice; vault timestamps are display-only


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _now_eest() -> str:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Asia/Nicosia")).strftime("%Y-%m-%d %H:%M EEST")
    except Exception:
        return _now_iso()


def _open_db() -> sqlite3.Connection:
    cfg = load_config(PROJECT_ROOT)
    conn = sqlite3.connect(cfg.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _pct(value: float | None) -> str:
    return f"{value:+.2f}%" if isinstance(value, (int, float)) else "—"


def _fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "—"
    try:
        f = float(value)
        if abs(f) >= 1000:
            return f"{f:,.2f}"
        if abs(f) >= 1:
            return f"{f:.{digits - 2}f}" if digits >= 2 else f"{f:.2f}"
        return f"{f:.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _latest_files(directory: Path, pattern: str = "*.md", limit: int = 5) -> list[Path]:
    if not directory.exists():
        return []
    files = sorted(
        directory.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[:limit]


def _relative_to_vault(path: Path) -> str:
    """Render a clickable Obsidian link given a path anywhere under the project."""
    try:
        rel = path.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        return str(path)
    return f"[{rel.name}](../{rel.as_posix()})"


# ---------------------------------------------------------------------------
# 00 — Dashboard
# ---------------------------------------------------------------------------


def write_dashboard() -> None:
    body = f"""# 📌 Dashboard — crypto-ai-desk

_Last refreshed: **{_now_eest()}**_

This is the daily landing page. Pinned tabs (📌) refresh on every scheduler cycle.

---

## 🔥 Live trade desk

- [[11 📌 Trading Desk Current State]] — **single-screen sweep**: system health + open paper trades + last 5 closures + today's events + top risks + mode routing + performance + manual checklist
- [[01 📌 Active Signals]] — current B/A signals awaiting entry or already triggered
- [[02 📌 Trade History]] — completed signals with outcomes (wins/losses/missed)
- [[03 📌 Todays Catalysts]] — fresh catalyst events + narrative baskets
- [[06 📌 Telegram Feed]] — last 50 Telegram-channel headlines (lookonchain, BWEnews, bloomberg…)

## 📋 Reports & reviews

- [[04 📌 Latest Reports]] — most-recent scalp / intraday / stocks reports
- [[05 📌 Opus Auto Reviews]] — auto-generated enriched-reviews (6×/day)
- [[Daily_Reviews]] — daily Obsidian summaries

## ⚙️ System health

- [[07 📌 Schedule Status]] — scheduler + Telegram collector + watchlist monitor status

## 🔬 Diagnostic & performance

- [[08 📌 Rejected Ideas]] — what the system declined and why (override candidates)
- [[09 📌 Macro Risk Heatmap]] — risk-on / risk-off score + headlines
- [[10 📌 Performance by Mode]] — signal-stats breakdown per mode and tier

---

## Existing knowledge folders

| # | Folder | What it contains |
|---|--------|------------------|
| 00 | [[00_System_Overview]] | Principles, glossary, LLM ops |
| 01 | [[01_Market_Regime]] | Regime classification |
| 02 | [[02_Trading_Modes]] | Scalp / intraday / swing / invest |
| 03 | [[03_Risk_Management]] | Position sizing, stops, R-multiple |
| 04 | [[04_Indicators_and_Metrics]] | RS, momentum, volume |
| 05 | [[05_News_Telegram_Catalysts_Sentiment]] | News sources, catalyst classes |
| 06 | [[06_Sectors_and_Narratives]] | Sector rotation, narrative baskets |
| 07 | [[07_Exchange_Logic]] | Multi-exchange fusion |
| 08 | [[08_Agents]] | Agent architecture |
| 09 | [[09_Scoring_System]] | Scoring weights + tiers |
| 10 | [[10_Trade_Idea_Format]] | TradeIdea template |
| 11 | [[11_Trade_Journal]] | Trade journal (legacy folder, populated by `review-day`) |
| 12 | [[12_News_Intelligence_Journal]] | News intelligence |
| 13 | [[13_Debugging_and_Improvement]] | System debugging notes |
| 14 | [[14_Project_Commands]] | CLI commands reference |
| 15 | [[15_LLM_Context]] | LLM prompts + checklists |
| 16 | [[16_Stocks]] | Stocks-specific docs |

---

## ⚠️ Safety contract (always)

- No auto-trade
- No scoring / threshold / agent / strategy changes
- The 6×/day Opus auto-reviews run via Claude `routines` (scheduled-tasks)
- Telegram alerts only fire on B/A tier promotions (with 30–45 min cooldown per PART 2)

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "00 📌 Dashboard.md", body)


# ---------------------------------------------------------------------------
# 01 — Active Signals
# ---------------------------------------------------------------------------


def write_active_signals() -> None:
    conn = _open_db()
    rows = conn.execute(
        """
        SELECT signal_id, asset_class, symbol, direction, mode, tier, score,
               status, confidence, entry_low, entry_high, invalidation,
               tp1, tp2, tp3, expected_rr_tp1, narrative, sector,
               exchange_focus, created_at, expires_at
        FROM proposed_signals
        WHERE status IN ('waiting_for_entry','triggered','tp1_hit','tp2_hit')
          AND tier IN ('A','B')
          AND datetime(created_at) >= datetime('now','-3 days')
        ORDER BY asset_class, tier, score DESC, created_at DESC
        """
    ).fetchall()
    conn.close()

    # Dedup by (symbol, mode, asset_class, direction): keep the most recent.
    seen: dict[tuple, dict] = {}
    for r in rows:
        key = (r["asset_class"], r["symbol"], r["mode"], r["direction"])
        if key not in seen:
            seen[key] = dict(r)
    deduped = list(seen.values())
    deduped.sort(key=lambda d: (d["asset_class"], d["tier"], -float(d.get("score") or 0)))

    def _section(asset_class: str) -> str:
        items = [d for d in deduped if d["asset_class"] == asset_class]
        if not items:
            return f"_No active {asset_class} signals._\n"
        lines = [
            "| Tier | Symbol | Dir | Mode | Score | Status | Entry | SL | TP1 | RR | Narrative |",
            "|------|--------|-----|------|------:|--------|-------|----|-----|----|-----------|",
        ]
        for d in items:
            entry_zone = f"{_fmt(d['entry_low'])} – {_fmt(d['entry_high'])}"
            lines.append(
                f"| **{d['tier']}** | `{d['symbol']}` | {d['direction']} | {d['mode']} | "
                f"{float(d['score'] or 0):.1f} | {d['status']} | "
                f"{entry_zone} | {_fmt(d['invalidation'])} | "
                f"{_fmt(d['tp1'])} | "
                f"{_fmt(d['expected_rr_tp1'], digits=2)} | "
                f"{d.get('narrative') or d.get('sector') or '—'} |"
            )
        return "\n".join(lines) + "\n"

    body = f"""# 📌 Active Signals — waiting / triggered (B & A tier)

_Refreshed: **{_now_eest()}**. Source: `proposed_signals` SQLite, last 72h, dedup by (symbol, mode, direction)._

Status meanings: `waiting_for_entry` = price has not reached the entry zone yet; `triggered` = price entered the zone; `tp1_hit` / `tp2_hit` = partial take-profit reached.

---

## 🪙 Crypto

{_section("crypto")}

## 📈 Stocks

{_section("stocks")}

---

## How to use this table

1. **Sort priority:** A-tier on top, then B-tier by score.
2. **`waiting_for_entry`** = the bot watches the price and will fire a Telegram alert when it approaches the entry zone (every 5 min for crypto, every 10 min for stocks during US RTH).
3. **`triggered`** = price has already entered the zone. Decide manually whether to honour the setup (system does not auto-trade).
4. **Score < 80** = B-tier (one or two confirmations missing). Use these for smaller-size positions or as watchlist.

Total active rows: **{len(deduped)}** (crypto: {sum(1 for d in deduped if d['asset_class']=='crypto')}, stocks: {sum(1 for d in deduped if d['asset_class']=='stocks')}).

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "01 📌 Active Signals.md", body)


# ---------------------------------------------------------------------------
# 02 — Trade History (completed signals)
# ---------------------------------------------------------------------------


def write_trade_history() -> None:
    conn = _open_db()
    # ⚠️ Signal-ID duplication note
    # ----------------------------------------------------------------
    # The scheduler regenerates the *same setup* every 2h with a new
    # `signal_id` (report_id + slightly-different entry/SL floats each
    # cycle make the deterministic hash diverge). Stats keyed on
    # `signal_id` therefore inflate the trade count 5-15× for stocks
    # intraday and 1-25× for crypto popular setups.
    #
    # This dashboard counts a "trade" as a unique
    # ``(asset_class, symbol, mode, direction, calendar day)``. Multiple
    # signal_ids that share that tuple are collapsed into one outcome
    # using the LATEST final outcome row across all of them.
    #
    # See `02 📌 Trade History.md` footer for the explanation users see.
    rows = conn.execute(
        """
        WITH latest_outcome AS (
            SELECT signal_id, MAX(checked_at) AS max_checked
            FROM signal_outcomes
            WHERE final_outcome IS NOT NULL AND final_outcome != ''
            GROUP BY signal_id
        ),
        signal_finals AS (
            SELECT ps.asset_class, ps.symbol, ps.direction, ps.mode, ps.tier,
                   ps.score, ps.created_at, ps.entry_low, ps.entry_high,
                   ps.invalidation, ps.tp1, ps.status,
                   so.final_outcome, so.final_r,
                   so.entry_triggered, so.tp1_hit, so.tp2_hit, so.tp3_hit,
                   so.stop_hit, so.max_favorable_excursion_r,
                   so.max_adverse_excursion_r, so.checked_at,
                   substr(ps.created_at, 1, 10) AS day,
                   ROW_NUMBER() OVER (
                       PARTITION BY ps.asset_class, ps.symbol, ps.mode,
                                    ps.direction, substr(ps.created_at, 1, 10)
                       ORDER BY so.checked_at DESC
                   ) AS rank
            FROM proposed_signals ps
            JOIN latest_outcome lo ON lo.signal_id = ps.signal_id
            JOIN signal_outcomes so
                ON so.signal_id = ps.signal_id AND so.checked_at = lo.max_checked
        )
        SELECT * FROM signal_finals WHERE rank = 1
        ORDER BY checked_at DESC LIMIT 80
        """
    ).fetchall()

    # Aggregate stats — collapse by (symbol, mode, direction, day) so one
    # setup repeated across 12 cycles counts as ONE trade. Wins/losses use
    # final_r sign (cleaner than tp1_hit/stop_hit which can both be 1 if a
    # signal hit TP1 then reversed to stop).
    stats_rows = conn.execute(
        """
        WITH latest_outcome AS (
            SELECT signal_id, MAX(checked_at) AS max_checked
            FROM signal_outcomes
            WHERE final_outcome IS NOT NULL AND final_outcome != ''
            GROUP BY signal_id
        ),
        per_setup AS (
            SELECT ps.asset_class, ps.symbol, ps.mode, ps.direction,
                   substr(ps.created_at, 1, 10) AS day,
                   MAX(so.final_r) AS best_r,
                   MIN(so.final_r) AS worst_r,
                   AVG(so.final_r) AS avg_r_setup
            FROM proposed_signals ps
            JOIN latest_outcome lo ON lo.signal_id = ps.signal_id
            JOIN signal_outcomes so
                ON so.signal_id = ps.signal_id AND so.checked_at = lo.max_checked
            GROUP BY ps.asset_class, ps.symbol, ps.mode, ps.direction, day
        )
        SELECT asset_class,
               COUNT(*) AS n,
               SUM(CASE WHEN avg_r_setup > 0 THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN avg_r_setup < 0 THEN 1 ELSE 0 END) AS losses,
               AVG(avg_r_setup) AS avg_r
        FROM per_setup
        GROUP BY asset_class
        """
    ).fetchall()

    # Also gather inflated count for the diagnostic footer.
    inflated = conn.execute(
        """
        SELECT ps.asset_class, COUNT(DISTINCT ps.signal_id) AS n
        FROM proposed_signals ps
        JOIN signal_outcomes so ON so.signal_id = ps.signal_id
        WHERE so.final_outcome IS NOT NULL AND so.final_outcome != ''
        GROUP BY ps.asset_class
        """
    ).fetchall()
    inflated_map = {r["asset_class"]: r["n"] for r in inflated}
    conn.close()

    def _line(r: dict | sqlite3.Row) -> str:
        r = dict(r)
        outcome = r.get("final_outcome") or r.get("status") or "—"
        emoji = {
            "tp1_hit": "🟢", "tp2_hit": "🟢🟢", "tp3_hit": "🟢🟢🟢",
            "stopped": "🔴", "stop": "🔴", "expired": "⚪",
            "missed_no_entry": "⚫",
        }.get(outcome, "•")
        r_val = r.get("final_r")
        r_str = f"{r_val:+.2f}R" if isinstance(r_val, (int, float)) else "—"
        mae = r.get("max_adverse_excursion_r")
        mfe = r.get("max_favorable_excursion_r")
        mae_str = f"{mae:+.2f}R" if isinstance(mae, (int, float)) else "—"
        mfe_str = f"{mfe:+.2f}R" if isinstance(mfe, (int, float)) else "—"
        return (
            f"| {emoji} | `{r['symbol']}` | {r['direction']} | {r['mode']} | "
            f"**{r['tier']}** | {(r.get('score') or 0):.1f} | "
            f"{outcome} | {r_str} | MFE {mfe_str} / MAE {mae_str} | "
            f"{(r.get('created_at') or '')[:10]} |"
        )

    history_lines = [
        "| | Symbol | Dir | Mode | Tier | Score | Outcome | Final R | MFE / MAE | Date |",
        "|---|--------|-----|------|------|------:|---------|---------|-----------|------|",
    ]
    for r in rows:
        history_lines.append(_line(r))

    stats_lines = [
        "| Class | Unique trades | Wins | Losses | WR | Avg R | Raw signal_ids (inflated) |",
        "|-------|--------------:|-----:|-------:|---:|------:|--------------------------:|",
    ]
    for sr in stats_rows:
        avg_r = sr["avg_r"] if sr["avg_r"] is not None else 0.0
        n = sr["n"] or 0
        wins = sr["wins"] or 0
        losses = sr["losses"] or 0
        wr_str = f"{(wins / n) * 100:.0f}%" if n else "—"
        raw = inflated_map.get(sr["asset_class"], 0)
        stats_lines.append(
            f"| {sr['asset_class']} | **{n}** | {wins} | "
            f"{losses} | {wr_str} | {avg_r:+.2f} | {raw} |"
        )

    body = f"""# 📌 Trade History — completed signals with outcomes

_Refreshed: **{_now_eest()}**. Last 80 unique setups (deduped) from `proposed_signals` × `signal_outcomes`._

Outcome legend: 🟢 TP1 hit · 🟢🟢 TP2 hit · 🟢🟢🟢 TP3 hit · 🔴 stop-loss · ⚪ expired · ⚫ missed (no entry).

---

## 📊 Aggregate stats — counted as UNIQUE setups (the honest view)

A **unique setup** = one row per ``(asset_class, symbol, mode, direction, calendar day)``. Multiple signal_ids that share that tuple are collapsed into one outcome — see footer for why this matters.

{chr(10).join(stats_lines)}

---

## 📜 History (most recent 80 unique setups)

{chr(10).join(history_lines)}

---

## Field meanings

- **Unique trades** — distinct setups (symbol × mode × direction × day). The fair count.
- **Raw signal_ids (inflated)** — what `proposed_signals` actually holds. Inflated because every 2h cycle re-registers the same setup with a new id (see diagnostic note below).
- **Final R** — realized R-multiple. Positive = winner, negative = stopped.
- **MFE / MAE** — maximum favourable / adverse excursion in R units while the trade was open. Even a winning trade with a large MAE indicates poor entry timing.
- **Missed (no entry)** = system fired a setup, but price never reached the entry zone before expiry → no trade.

For per-signal detail, see `11_Trade_Journal/Signal_Performance/Signal_Logs/` (one Markdown file per signal).

---

## ⚠️ Diagnostic note — why "Unique trades" ≠ "Raw signal_ids"

The default scheduler refreshes intraday reports every 2 hours. Each cycle generates new signal_ids for the SAME setup because:

1. The deterministic `signal_id_for()` hash includes `report_id` — which is unique per cycle.
2. Entry / stop floats slightly differ each cycle as fresh OHLCV recomputes ATR-based zones.

Result: one logical trade idea like `AAPL intraday long 2026-05-27` can appear as **15 separate signal_ids** in the DB. The dashboard already corrects for this by collapsing by ``(symbol, mode, direction, day)``. The underlying registry should also be fixed in a future sprint so `proposed_signals` itself stops duplicating — but the deduplication here gives an immediately honest read.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "02 📌 Trade History.md", body)


# ---------------------------------------------------------------------------
# 03 — Today's Catalysts
# ---------------------------------------------------------------------------


def write_todays_catalysts() -> None:
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cat_dir = PROJECT_ROOT / "data" / "catalysts" / today_str

    events_lines: list[str] = []
    baskets_lines: list[str] = []
    cycle_summary = ""

    if cat_dir.exists():
        ev_file = cat_dir / "catalyst_events.jsonl"
        bk_file = cat_dir / "narrative_baskets.jsonl"

        if ev_file.exists():
            events: list[dict] = []
            for line in ev_file.read_text(encoding="utf-8").splitlines():
                try:
                    events.append(json.loads(line))
                except Exception:
                    continue
            events.sort(
                key=lambda e: (
                    -float(e.get("importance") or 0),
                    e.get("timestamp") or "",
                ),
                reverse=False,
            )
            events_lines.append(
                "| Symbol | Type | Source quality | Title | Confidence |"
            )
            events_lines.append(
                "|--------|------|----------------|-------|------------|"
            )
            for ev in events[:30]:
                symbol = ev.get("symbol") or "(basket)"
                title = (ev.get("title") or "")[:140].replace("|", "/")
                src_q = ev.get("source_quality") or "—"
                ct = ev.get("catalyst_type") or "other_news"
                conf = ev.get("confidence") or "—"
                events_lines.append(
                    f"| `{symbol}` | **{ct}** | {src_q} | {title} | {conf} |"
                )
        else:
            events_lines.append("_No catalyst events today yet._")

        if bk_file.exists():
            for line in bk_file.read_text(encoding="utf-8").splitlines():
                try:
                    b = json.loads(line)
                except Exception:
                    continue
                primary = ", ".join(b.get("primary_symbols", []) or [])
                related = ", ".join(b.get("related_symbols", []) or [])
                baskets_lines.append(
                    f"### 🧺 {b.get('basket_name', 'unnamed')} "
                    f"(playbook `{b.get('suggested_playbook', '—')}`, "
                    f"freshness `{b.get('freshness', '—')}`)"
                )
                baskets_lines.append(
                    f"- Primary: `{primary or '—'}`"
                )
                if related:
                    baskets_lines.append(f"- Related: `{related}`")
                summary = b.get("catalyst_summary") or ""
                if summary:
                    baskets_lines.append(f"- Summary: {summary}")
                baskets_lines.append("")
        else:
            baskets_lines.append("_No narrative baskets today yet._")

        cycle_files = sorted(cat_dir.glob("catalyst_cycle_*.md"))
        if cycle_files:
            latest = cycle_files[-1]
            cycle_summary = f"\nLatest cycle summary: [{latest.name}](../data/catalysts/{today_str}/{latest.name})\n"
    else:
        events_lines.append("_Catalyst-scan has not run yet today._")
        baskets_lines.append("")

    body = f"""# 📌 Today's Catalysts — fresh news & narrative baskets

_Refreshed: **{_now_eest()}** · Source: `data/catalysts/{today_str}/`_

---

## 🧺 Narrative baskets

{chr(10).join(baskets_lines) or "_None._"}

---

## 📰 Top catalyst events (sorted by importance)

{chr(10).join(events_lines) or "_None._"}

{cycle_summary}

---

## How catalysts feed the desk

- `RSSNewsCollector` (every cycle) pulls from 10+ crypto RSS + 8 stocks RSS + 18 Telegram channels.
- `catalyst-scan` CLI classifies each `news_items` row into one of 26 categories (exploit_hack, earnings_event, regulatory, exchange_listing, governance_event, etc.).
- Auto-clusters related symbols into **narrative baskets** with a suggested playbook (`wait_pullback`, `related_beta_rotation`, `avoid_chase`, etc.).

Baskets with `momentum_breakout` + `avoid_chase` are the canonical "don't chase the parabola" warning.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "03 📌 Todays Catalysts.md", body)


# ---------------------------------------------------------------------------
# 04 — Latest Reports
# ---------------------------------------------------------------------------


def write_latest_reports() -> None:
    crypto_scalp = _latest_files(PROJECT_ROOT / "data/reports/scalp", "*scalp_report.md", limit=3)
    crypto_intraday = _latest_files(PROJECT_ROOT / "data/reports/intraday", "*intraday_report.md", limit=3)
    crypto_swing = _latest_files(PROJECT_ROOT / "data/reports/swing", "*swing_report.md", limit=3)
    stocks_intraday = _latest_files(PROJECT_ROOT / "data/reports/stocks/intraday", "*stocks_intraday_report.md", limit=3)
    # Old stocks swing/invest reports are DEPRECATED/REMOVED — no longer generated. Show the new
    # shadow-only stocks position framework report instead.
    stocks_position = _latest_files(PROJECT_ROOT / "reports", "stocks_position_framework_latest.md", limit=1)

    def _bullets(files: list[Path]) -> str:
        if not files:
            return "_None._"
        out: list[str] = []
        for f in files:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)
            except Exception:
                mtime = None
            stamp = mtime.strftime("%Y-%m-%d %H:%M UTC") if mtime else "?"
            rel = f.resolve().relative_to(PROJECT_ROOT.resolve())
            out.append(f"- [{f.name}](../{rel.as_posix()}) · _{stamp}_")
        return "\n".join(out)

    body = f"""# 📌 Latest Reports — newest cycle output

_Refreshed: **{_now_eest()}** · Each scheduler cycle (every 2h) writes new reports._

---

## 🪙 Crypto

### Scalp (30m–2h)
{_bullets(crypto_scalp)}

### Intraday (4h–24h)
{_bullets(crypto_intraday)}

### Swing (daily-once)
{_bullets(crypto_swing)}

---

## 📈 Stocks

### Stocks intraday (weekday cycles only)
{_bullets(stocks_intraday)}

### Stocks position framework (shadow-only research)
_Old stocks swing/invest are DEPRECATED/REMOVED and no longer generated. The new
`stocks_swing_growth_breakout` framework is shadow-only — no live, no Telegram, no actionability._

{_bullets(stocks_position)}

---

## Anatomy of a report

Each report contains:
1. **§0 Exchange coverage & candidate funnel** — how many symbols passed each filter.
2. **§1 Market regime** — bullish/bearish/sideways + risk_mode.
3. **§2 Where money is flowing** — strongest/weakest symbols + narrative heatmap.
4. **§3 Derivatives overview** (crypto only) — funding + OI + long/short.
5. **§4 Macro & geopolitics**.
6. **§5 News & catalysts** + auto-collected baskets.
7. **§6 Top trade ideas** (A/B tier).
8. **§7 C-tier / watchlist** + rejected with reason.

The deterministic reports never auto-trade. Opus enriched reviews (see [[05 📌 Opus Auto Reviews]]) wrap external WebSearch + WebFetch around these.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "04 📌 Latest Reports.md", body)


# ---------------------------------------------------------------------------
# 05 — Opus Auto Reviews
# ---------------------------------------------------------------------------


def write_opus_reviews() -> None:
    files = []
    for pat in ("OPUS_ENRICHED_REVIEW_AUTO_*.md", "OPUS_ENRICHED_REVIEW_LATEST.md",
                "OPUS_ENRICHED_REVIEW_*.md"):
        for f in PROJECT_ROOT.glob(pat):
            if f not in files:
                files.append(f)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    files = files[:20]

    bullets: list[str] = []
    for f in files:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)
        except Exception:
            mtime = None
        stamp = mtime.strftime("%Y-%m-%d %H:%M UTC") if mtime else "?"
        rel = f.resolve().relative_to(PROJECT_ROOT.resolve())
        bullets.append(f"- [{f.name}](../{rel.as_posix()}) · _{stamp}_")

    body = f"""# 📌 Opus Auto Reviews — enriched analyses

_Refreshed: **{_now_eest()}**_

The Claude `routine` **opus-enriched-review-4h** fires automatically **6×/day** (00:30, 04:30, 08:30, 12:30, 16:30, 20:30 EEST) and runs the full `enriched-review` skill:
- Reads latest reports + catalyst data.
- WebSearch + WebFetch per candidate (§14 source discipline).
- Ingests external sources into `news_items` SQLite.
- Writes `OPUS_ENRICHED_REVIEW_LATEST.md` (always overwritten) + `OPUS_ENRICHED_REVIEW_AUTO_<timestamp>.md` (history).
- Sends a compact Telegram summary with top decisions + key risks.

Manual reviews (typed `/enriched-review` in chat) use the **same** skill.

---

## 📜 Recent reviews (latest first)

{chr(10).join(bullets) if bullets else "_No reviews yet — the first auto-review fires at 00:30 EEST._"}

---

## How to read these

Each review has fixed sections:
- **Executive Summary** — 3-6 bullets, read this first.
- **Data Used** — what was loaded + what was unavailable.
- **Candidate Deep Dives** — verified external claims with URL + date.
- **Best Candidates / Avoid / Main Risks / Action Plan**.
- **Final Verdict** per mode + overall.
- **Sources** with markdown hyperlinks (verification: primary_source / single_source / social_only).

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "05 📌 Opus Auto Reviews.md", body)


# ---------------------------------------------------------------------------
# 06 — Telegram Feed (latest TG-channel news)
# ---------------------------------------------------------------------------


def write_telegram_feed() -> None:
    conn = _open_db()
    rows = conn.execute(
        """
        SELECT title, source, published_at, asset_class, detected_symbols_json
        FROM news_items
        WHERE source LIKE 't.me/%'
        ORDER BY published_at DESC
        LIMIT 50
        """
    ).fetchall()
    by_source = conn.execute(
        """
        SELECT source, asset_class, COUNT(*) AS n
        FROM news_items
        WHERE source LIKE 't.me/%'
          AND datetime(published_at) > datetime('now','-24 hours')
        GROUP BY source, asset_class
        ORDER BY n DESC
        """
    ).fetchall()
    conn.close()

    src_lines = [
        "| Channel | Class | Msgs (24h) |",
        "|---------|-------|-----------:|",
    ]
    for r in by_source:
        src_lines.append(
            f"| `{r['source']}` | {r['asset_class']} | {r['n']} |"
        )

    feed_lines: list[str] = []
    for r in rows:
        ts = (r["published_at"] or "")[:16].replace("T", " ")
        channel = (r["source"] or "").replace("t.me/", "")
        try:
            syms = json.loads(r["detected_symbols_json"] or "[]")
        except Exception:
            syms = []
        syms_str = (", ".join(f"`{s}`" for s in syms[:4])) or ""
        title = (r["title"] or "")[:200].replace("|", "/")
        feed_lines.append(
            f"- **{ts}** `[{channel}]` ({r['asset_class']}) {title}"
            + (f" — {syms_str}" if syms_str else "")
        )

    body = f"""# 📌 Telegram Feed — last 50 channel messages

_Refreshed: **{_now_eest()}**_

The Telegram collector listens to **18 curated channels** via Telethon. Messages land in `news_items` SQLite with `source = t.me/<handle>` and `asset_class = crypto | stocks`.

---

## 📊 24-hour volume by channel

{chr(10).join(src_lines) if by_source else "_No Telegram traffic in last 24h. Channels may be quiet on weekends._"}

---

## 📜 Latest 50 messages

{chr(10).join(feed_lines) if feed_lines else "_No messages yet — collector just started._"}

---

## Channels currently subscribed

**Stocks / macro (6):** `DeItaone`, `PiQSuite`, `cnbci`, `bloomberg`, `WalterBloomberg`, `forexlive`
**Crypto exchanges / listings (5):** `binance_announcements`, `Bybit_Announcements`, `MEXCEnglish`, `BWEnews`, `WuBlockchainEnglish`
**Crypto security / hacks (3):** `zachxbt`, `peckshield`, `RektHQ`
**Crypto whale / on-chain (2):** `lookonchain`, `ArkhamIntelligence`
**Crypto general (2):** `WatcherGuru`, `CoinTelegraph`

To add/remove channels: edit `config/sources.yaml → telegram_channels.channels` and restart `scripts/run_telegram_collector.py`.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "06 📌 Telegram Feed.md", body)


# ---------------------------------------------------------------------------
# 07 — Schedule Status
# ---------------------------------------------------------------------------


def write_schedule_status() -> None:
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_dir = PROJECT_ROOT / "data" / "scheduled_runs"
    today_dir = run_dir / f"{today_str}_default_schedule"
    cycle_lines: list[str] = []
    if today_dir.exists():
        cycle_files = sorted(today_dir.glob("cycle_*_summary.md"))
        for cf in cycle_files[-6:]:
            try:
                mtime = datetime.fromtimestamp(cf.stat().st_mtime, timezone.utc)
                stamp = mtime.strftime("%H:%M UTC")
            except Exception:
                stamp = "?"
            cycle_lines.append(f"- [{cf.name}](../data/scheduled_runs/{today_str}_default_schedule/{cf.name}) · _{stamp}_")
        marker = today_dir / f"daily_{today_str}.done"
        daily_done = marker.exists()
    else:
        daily_done = False

    conn = _open_db()
    crypto_alerts = conn.execute(
        "SELECT COUNT(*) FROM watchlist_alerts WHERE datetime(sent_at) > datetime('now','-24 hours') AND asset_class='crypto'"
    ).fetchone()[0]
    stocks_alerts_24h = 0
    try:
        stocks_alerts_24h = conn.execute(
            "SELECT COUNT(*) FROM signal_alerts WHERE datetime(sent_at) > datetime('now','-24 hours')"
        ).fetchone()[0]
    except sqlite3.OperationalError:
        # signal_alerts table may not exist on older DBs
        pass
    tg_msgs_24h = conn.execute(
        "SELECT COUNT(*) FROM news_items WHERE source LIKE 't.me/%' AND datetime(published_at) > datetime('now','-24 hours')"
    ).fetchone()[0]
    conn.close()

    body = f"""# 📌 Schedule Status — system health

_Refreshed: **{_now_eest()}**_

---

## ⚙️ Running components (expected)

| Process | Purpose |
|---------|---------|
| `scripts/run_default_market_schedule.py` | 2-hour cycle scheduler (12 cycles/day): scalp + intraday + (weekday) stocks-intraday + background monitors |
| `src.cli monitor-watchlist` | Crypto watchlist monitor — tickes every 5 min, alerts on tier upgrades |
| `src.cli stocks-monitor-session` | Stocks watchlist monitor — tickes every 10 min during US RTH only |
| `scripts/run_telegram_collector.py` | 18-channel Telegram listener |
| Claude routine `opus-enriched-review-4h` | 6×/day auto-Opus enriched reviews (00:30 / 04:30 / 08:30 / 12:30 / 16:30 / 20:30 EEST) |

---

## 🟢 Today's activity ({today_str})

- Long-horizon (swing/invest) ran already today: **{'yes' if daily_done else 'no — will run on next cycle'}**
- Crypto watchlist Telegram alerts in last 24h: **{crypto_alerts}**
- Stocks Telegram alerts in last 24h: **{stocks_alerts_24h}**
- Telegram-channel news ingested in last 24h: **{tg_msgs_24h}**

## 📜 Recent scheduler cycles

{chr(10).join(cycle_lines) if cycle_lines else "_No cycle summaries yet today._"}

---

## How to operate

| Action | Command |
|--------|---------|
| Restart scheduler | `py -3 scripts/run_default_market_schedule.py --hours 24 --interval-hours 2 --send-telegram` |
| Restart TG collector | `py -3 scripts/run_telegram_collector.py` |
| Manual single cycle (test) | `py -3 scripts/run_default_market_schedule.py --run-once --dry-run` |
| Check scheduler log | `data/scheduled_runs/<today>_default_schedule/scheduler.log` |
| List Claude routines | (Claude Desktop → left sidebar → Scheduled) |

---

## Safety contract reminder

- Scheduler never auto-trades.
- Scheduler never invokes Opus / LLM (auto-LLM happens via the Claude routine only, which the user explicitly opted in).
- `news_trader/` directory is READ-ONLY.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "07 📌 Schedule Status.md", body)


# ---------------------------------------------------------------------------
# 08 — Rejected Ideas (what system declined and why)
# ---------------------------------------------------------------------------


def write_rejected_ideas() -> None:
    conn = _open_db()
    rows = conn.execute(
        """
        SELECT created_at, symbol, asset_class, direction_bias, score,
               primary_reason, reasons_json, risk_flags_json
        FROM rejected_ideas
        WHERE datetime(created_at) >= datetime('now','-48 hours')
        ORDER BY score DESC, created_at DESC
        LIMIT 60
        """
    ).fetchall()

    # Reason frequency aggregation — see what cuts most signals.
    reason_counts = conn.execute(
        """
        SELECT primary_reason, COUNT(*) AS n
        FROM rejected_ideas
        WHERE datetime(created_at) >= datetime('now','-48 hours')
        GROUP BY primary_reason
        ORDER BY n DESC
        LIMIT 12
        """
    ).fetchall()
    total = conn.execute(
        "SELECT COUNT(*) FROM rejected_ideas WHERE datetime(created_at) >= datetime('now','-48 hours')"
    ).fetchone()[0]
    conn.close()

    # Group rows by asset class for the detail tables.
    def _section(ac: str) -> str:
        items = [r for r in rows if r["asset_class"] == ac]
        if not items:
            return f"_No {ac} rejections in last 48h._\n"
        lines = [
            "| Symbol | Dir | Score | Primary reason | When |",
            "|--------|-----|------:|----------------|------|",
        ]
        for r in items[:25]:
            reason = (r["primary_reason"] or "—")[:90].replace("|", "/")
            ts = (r["created_at"] or "")[:16].replace("T", " ")
            lines.append(
                f"| `{r['symbol']}` | {r['direction_bias'] or '—'} | "
                f"{float(r['score'] or 0):.1f} | {reason} | {ts} |"
            )
        return "\n".join(lines) + "\n"

    reason_lines = ["| Primary reason | Count |", "|----------------|------:|"]
    for r in reason_counts:
        reason = (r["primary_reason"] or "—")[:110].replace("|", "/")
        reason_lines.append(f"| {reason} | {r['n']} |")

    body = f"""# 📌 Rejected Ideas — what the system declined and why

_Refreshed: **{_now_eest()}** · Last 48h. Source: `rejected_ideas` SQLite._

Total rejections in window: **{total}**. This view explains why otherwise interesting symbols never made it to A/B tier — useful for spotting filter strictness, regime mismatches, or override candidates worth a manual Opus look.

---

## 🔢 Top rejection reasons (last 48h)

{chr(10).join(reason_lines) if reason_counts else "_None._"}

---

## 🪙 Crypto rejections (top 25 by score)

{_section("crypto")}

## 📈 Stocks rejections (top 25 by score)

{_section("stocks")}

---

## How to read this

- **Score ≥ 50 with regime-mismatch reason** = the setup itself is technically OK, only blocked because the broader regime contradicts it. These are the canonical "wait for regime flip" candidates.
- **Score ≥ 50 with "no fresh verified catalyst" reason** = manual Opus review can override if news landed late. The 6×/day auto-Opus picks up these cases as override candidates per the routine prompt.
- **"Derivatives data unavailable"** = crypto symbol without good futures data — usually a small alt or stocks-only ticker. Often safe to ignore.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "08 📌 Rejected Ideas.md", body)


# ---------------------------------------------------------------------------
# 09 — Macro Risk Heatmap
# ---------------------------------------------------------------------------


def write_macro_heatmap() -> None:
    agent_dir = PROJECT_ROOT / "data" / "processed" / "agent_outputs"
    macro_files = _latest_files(agent_dir, "*_macro_geopolitics_agent.json", limit=6)
    payloads: list[tuple[Path, dict]] = []
    for f in macro_files:
        try:
            payloads.append((f, json.loads(f.read_text(encoding="utf-8"))))
        except Exception:
            continue

    if not payloads:
        body = f"""# 📌 Macro Risk Heatmap

_Refreshed: **{_now_eest()}**_

_No macro_geopolitics_agent output found yet._

The macro agent emits a risk score 0–100 every cycle (higher = more risk-off). Wait for the next scheduler cycle and the file will populate.
"""
        _write(VAULT / "09 📌 Macro Risk Heatmap.md", body)
        return

    latest_path, latest = payloads[0]
    risk_score = float(latest.get("risk_score") or 0.0)
    bias = latest.get("btc_bias") or "neutral"
    themes = latest.get("themes") or []
    headlines = latest.get("headlines") or []
    explanation = latest.get("explanation") or ""

    # Render a simple 10-block visual heatmap (each block = 10 points).
    filled = max(0, min(10, round(risk_score / 10)))
    heat = "🟥" * filled + "⬜" * (10 - filled)

    # Trend over last 6 readings
    trend_lines = ["| When | Score | BTC bias | Themes |", "|------|------:|----------|--------|"]
    for f, p in payloads:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)
            stamp = mtime.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            stamp = "?"
        score = float(p.get("risk_score") or 0.0)
        tlist = ", ".join((p.get("themes") or [])[:4]) or "—"
        trend_lines.append(
            f"| {stamp} | {score:.0f} | {p.get('btc_bias') or '—'} | {tlist} |"
        )

    headline_lines = []
    for h in headlines[:8]:
        headline_lines.append(f"- {h}")

    body = f"""# 📌 Macro Risk Heatmap

_Refreshed: **{_now_eest()}** · Source: `data/processed/agent_outputs/*_macro_geopolitics_agent.json`_

---

## 🔥 Current reading

**Risk score:** **{risk_score:.0f} / 100**

{heat}

- **BTC bias:** `{bias}`
- **Active themes:** {", ".join(themes) if themes else "—"}
- **Explanation:** {explanation}

---

## 📰 Top macro headlines (last cycle)

{chr(10).join(headline_lines) if headline_lines else "_No headlines flagged._"}

---

## 📈 Recent trend (last 6 cycles)

{chr(10).join(trend_lines)}

---

## Score interpretation

- **0–30** — risk-on backdrop. Longs more reliable, breadth supportive.
- **30–60** — mixed / data-watch. Trade with normal discipline; avoid hero positions.
- **60–80** — risk-off building. Reduce size, prefer shorts in crypto, defensives in stocks.
- **80–100** — full risk-off (war, large hack, regulatory shock). No new longs; trail existing positions tight.

The macro agent reads RSS + Telegram news against `config/sources.yaml → macro_keywords` (risk_off / risk_on / neutral_watch buckets). Increase to >60 needs **two independent sources** to trigger an alert.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "09 📌 Macro Risk Heatmap.md", body)


# ---------------------------------------------------------------------------
# 10 — Performance by Mode / Tier
# ---------------------------------------------------------------------------


def write_performance_breakdown() -> None:
    conn = _open_db()
    # Dedupe by (asset_class, symbol, mode, direction, day) — every cycle
    # re-registers the same setup with a new signal_id, so raw counts are
    # inflated 5-15× for stocks intraday. We collapse to one row per
    # unique setup before any aggregation.
    cte = """
        WITH latest_outcome AS (
            SELECT signal_id, MAX(checked_at) AS max_checked
            FROM signal_outcomes
            WHERE final_outcome IS NOT NULL AND final_outcome != ''
            GROUP BY signal_id
        ), per_setup AS (
            SELECT ps.asset_class, ps.mode, ps.tier, ps.direction,
                   substr(ps.created_at, 1, 10) AS day,
                   ps.symbol,
                   MAX(ps.news_supported) AS news_supported,
                   MAX(so.entry_triggered) AS entry_triggered,
                   MAX(so.tp1_hit) AS tp1_hit,
                   MAX(so.stop_hit) AS stop_hit,
                   AVG(so.final_r) AS final_r
            FROM proposed_signals ps
            JOIN latest_outcome lo ON lo.signal_id = ps.signal_id
            JOIN signal_outcomes so
                ON so.signal_id = ps.signal_id AND so.checked_at = lo.max_checked
            GROUP BY ps.asset_class, ps.mode, ps.tier, ps.direction,
                     ps.symbol, substr(ps.created_at, 1, 10)
        )
    """

    by_mode_tier = conn.execute(
        cte + """
        SELECT asset_class, mode, tier,
               COUNT(*) AS n,
               SUM(CASE WHEN entry_triggered=1 THEN 1 ELSE 0 END) AS trig,
               SUM(CASE WHEN final_r > 0 THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN final_r < 0 THEN 1 ELSE 0 END) AS losses,
               AVG(final_r) AS avg_r,
               SUM(final_r) AS total_r
        FROM per_setup
        GROUP BY asset_class, mode, tier
        ORDER BY asset_class, mode,
                 CASE tier WHEN 'A' THEN 0 WHEN 'B' THEN 1 WHEN 'C' THEN 2 ELSE 3 END
        """
    ).fetchall()

    by_direction = conn.execute(
        cte + """
        SELECT asset_class, tier, direction,
               COUNT(*) AS n,
               SUM(CASE WHEN final_r > 0 THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN final_r < 0 THEN 1 ELSE 0 END) AS losses,
               AVG(final_r) AS avg_r,
               SUM(final_r) AS total_r
        FROM per_setup
        GROUP BY asset_class, tier, direction
        ORDER BY asset_class,
                 CASE tier WHEN 'A' THEN 0 WHEN 'B' THEN 1 WHEN 'C' THEN 2 ELSE 3 END,
                 direction
        """
    ).fetchall()

    # 2026-06-10 — Playbook-aware sizing layer (reporting only).
    # Pull per_setup rows AS dicts so we can route each through the
    # sizing helper. We need (asset_class, mode, tier, direction,
    # news_supported, score, final_r). See config/sizing_weights.yaml.
    per_setup_rows = conn.execute(
        cte + """
        SELECT asset_class, mode, tier, direction, news_supported,
               final_r
        FROM per_setup
        WHERE final_r IS NOT NULL
        """
    ).fetchall()
    conn.close()

    # 2026-06-10 fix: WR is `Wins ÷ Closed` (Closed = Wins + Losses).
    # The previous `Wins ÷ n` was depressed by pending / expired /
    # not_triggered rows, producing the misleading 16-17% headline the
    # user observed. See reports/DASHBOARD_WINRATE_DEFINITION_AUDIT.md.
    def _wr_closed(wins: int, losses: int) -> str:
        closed = wins + losses
        if not closed:
            return "—"
        return f"{(wins / closed) * 100:.0f}%"

    def _pf(wins_r: float, losses_r: float) -> str:
        if not losses_r:
            return "∞" if wins_r > 0 else "—"
        return f"{wins_r / losses_r:.2f}"

    # ── Headline: actionable A/B closed ──────────────────────────────────
    # Excludes C-tier / watchlist counterfactuals and pending/expired.
    def _headline_for(asset_class: str, mode_filter: str | None = None) -> tuple[int, int, int, int, int, float]:
        """Return (n, trig, W, L, closed, netR) for A/B closed cohort."""
        sub = [r for r in by_mode_tier
               if r["asset_class"] == asset_class
               and r["tier"] in ("A", "B")
               and (mode_filter is None or r["mode"] == mode_filter)]
        n = sum(r["n"] or 0 for r in sub)
        trig = sum(r["trig"] or 0 for r in sub)
        W = sum(r["wins"] or 0 for r in sub)
        L = sum(r["losses"] or 0 for r in sub)
        netR = sum(r["total_r"] or 0 for r in sub)
        return n, trig, W, L, W + L, netR

    crypto_n, crypto_trig, crypto_W, crypto_L, crypto_C, crypto_netR = _headline_for("crypto")
    stocks_n, stocks_trig, stocks_W, stocks_L, stocks_C, stocks_netR = _headline_for("stocks", "intraday")
    crypto_wr = _wr_closed(crypto_W, crypto_L)
    stocks_wr = _wr_closed(stocks_W, stocks_L)

    # ── By mode × tier (separate actionable / watchlist tables) ──────────
    actionable_rows = [r for r in by_mode_tier if r["tier"] in ("A", "B")]
    watchlist_rows = [r for r in by_mode_tier if r["tier"] not in ("A", "B")]

    def _mode_tier_line(r) -> str:
        wins = r["wins"] or 0
        losses = r["losses"] or 0
        n = r["n"] or 0
        trig = r["trig"] or 0
        avg_r = r["avg_r"] or 0
        total_r = r["total_r"] or 0
        pending = n - wins - losses
        return (
            f"| {r['asset_class']} | {r['mode']} | **{r['tier']}** | "
            f"{n} | {trig} | {pending} | {wins} | {losses} | {wins+losses} | "
            f"{_wr_closed(wins, losses)} | "
            f"{avg_r:+.2f} | {total_r:+.2f} |"
        )

    actionable_lines = [
        "| Asset | Mode | Tier | n | Trig | Pend* | W | L | Closed | **WR (closed)** | Avg R | Total R |",
        "|-------|------|------|--:|----:|----:|----:|----:|----:|---:|------:|--------:|",
    ] + [_mode_tier_line(r) for r in actionable_rows]

    watchlist_lines = [
        "| Asset | Mode | Tier | n | Trig | Pend* | W | L | Closed | WR (closed) | Avg R | Total R |",
        "|-------|------|------|--:|----:|----:|----:|----:|----:|---:|------:|--------:|",
    ] + [_mode_tier_line(r) for r in watchlist_rows]

    # ── By direction split by tier (actionable vs watchlist) ─────────────
    def _dir_line(r) -> str:
        wins = r["wins"] or 0
        losses = r["losses"] or 0
        n = r["n"] or 0
        avg_r = r["avg_r"] or 0
        total_r = r["total_r"] or 0
        pending = n - wins - losses
        return (
            f"| {r['asset_class']} | **{r['tier']}** | {r['direction']} | "
            f"{n} | {pending} | {wins} | {losses} | {wins+losses} | "
            f"{_wr_closed(wins, losses)} | {avg_r:+.2f} | {total_r:+.2f} |"
        )

    actionable_dir = [r for r in by_direction if r["tier"] in ("A", "B")]
    watchlist_dir = [r for r in by_direction if r["tier"] not in ("A", "B")]

    actionable_dir_lines = [
        "| Asset | Tier | Direction | n | Pend* | W | L | Closed | **WR (closed)** | Avg R | Total R |",
        "|-------|------|-----------|--:|----:|----:|----:|----:|---:|------:|--------:|",
    ] + [_dir_line(r) for r in actionable_dir]
    watchlist_dir_lines = [
        "| Asset | Tier | Direction | n | Pend* | W | L | Closed | WR (closed) | Avg R | Total R |",
        "|-------|------|-----------|--:|----:|----:|----:|----:|---:|------:|--------:|",
    ] + [_dir_line(r) for r in watchlist_dir]

    # ── Raw R vs Sized R (playbook-aware sizing) ─────────────────────────
    # Reporting-only layer. See config/sizing_weights.yaml and
    # src/signals/sizing.py.
    try:
        from src.signals.sizing import size_decision, portfolio_totals
        decisions = [size_decision(dict(r)) for r in per_setup_rows]
        totals = portfolio_totals(decisions)
        sum_raw = sum((d.raw_r or 0) for d in decisions)
        # Per-playbook contribution table — track the SET of weights seen so
        # mixed playbooks (e.g. stocks_intraday with A-long=0.5× + B-long=1.0×
        # + shorts=1.0×) render an honest "mix" rather than a single "last
        # seen" weight that misleads.
        from collections import defaultdict
        pb_contrib: dict[str, dict] = defaultdict(
            lambda: {"raw": 0.0, "sized": 0.0, "n": 0, "n_sized": 0,
                     "wins": 0, "losses": 0, "weights": set()})
        for d in decisions:
            row = pb_contrib[d.playbook]
            row["raw"] += (d.raw_r or 0)
            row["sized"] += (d.sized_r or 0)
            row["n"] += 1
            row["weights"].add(round(d.weight, 2))
            if d.weight > 0:
                row["n_sized"] += 1
                if (d.sized_r or 0) > 0:
                    row["wins"] += 1
                elif (d.sized_r or 0) < 0:
                    row["losses"] += 1

        def _weight_label(weights: set) -> str:
            if not weights:
                return "—"
            if len(weights) == 1:
                return f"{next(iter(weights)):.1f}×"
            return ", ".join(f"{w:.1f}×" for w in sorted(weights))

        # Sort by sized contribution
        pb_sorted = sorted(pb_contrib.items(), key=lambda x: -x[1]["sized"])
        top_positive = [(pb, x) for pb, x in pb_sorted if x["sized"] > 0][:5]
        top_negative = sorted(
            [(pb, x) for pb, x in pb_sorted if x["sized"] < 0],
            key=lambda x: x[1]["sized"],
        )[:5]

        size_table_lines = [
            "| Playbook | weight(s) | n | n_sized | W | L | rawR | **sizedR** |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for pb, x in pb_sorted:
            size_table_lines.append(
                f"| `{pb}` | {_weight_label(x['weights'])} | {x['n']} | {x['n_sized']} | {x['wins']} | "
                f"{x['losses']} | {x['raw']:+.1f} | **{x['sized']:+.1f}** |"
            )
        sized_section = (
            "\n\n---\n\n"
            "## 💰 Raw R vs Sized R (playbook-aware reporting layer)\n\n"
            "> Reporting/paper-PnL annotation only — does **not** influence "
            "signal generation, scoring, TP/SL, alerts, or `signal_outcomes`. "
            "Weights: `config/sizing_weights.yaml`. Logic: `src/signals/sizing.py`. "
            "Audit: [reports/PROFITABILITY_LEVERS_AUDIT.md].\n\n"
            "### Portfolio totals (deduped per-setup, all-time)\n\n"
            "| Metric | equal 1× (raw) | playbook-aware (sized) |\n"
            "|---|---:|---:|\n"
            f"| Total R | **{sum_raw:+.1f}R** | **{totals['sum_sized_r']:+.1f}R** |\n"
            f"| n setups | {totals['n']} | {totals['n_sized']} (sized > 0) |\n"
            f"| Wins (sized > 0) | — | {totals['wins']} |\n"
            f"| Losses (sized < 0) | — | {totals['losses']} |\n"
            f"| WR (sized closed) | — | {totals['WR_closed']}% |\n"
            f"| PF (sized) | — | {totals['PF']} |\n\n"
            "### By-playbook contribution\n\n"
            + "\n".join(size_table_lines) + "\n\n"
            "### Top positive contributors (sized)\n\n"
            + "\n".join(
                f"- `{pb}` — sizedR **{x['sized']:+.1f}R** (weights {_weight_label(x['weights'])}, n_sized={x['n_sized']})"
                for pb, x in top_positive) + ("\n" if top_positive else "_none_\n") + "\n"
            "### Top negative contributors (sized)\n\n"
            + "\n".join(
                f"- `{pb}` — sizedR **{x['sized']:+.1f}R** (weights {_weight_label(x['weights'])}, n_sized={x['n_sized']})"
                for pb, x in top_negative) + ("\n" if top_negative else "_none_\n") + "\n"
            "### Sizing notes\n\n"
            "- `crypto_scalp_momentum_continuation`: 0.5× (low-confidence; TP/horizon mismatch).\n"
            "- `stocks_intraday_rth_momentum` A-tier long: 0.5× (A-tier overpromotion symptom).\n"
            "- `stocks_swing_watchlist_rs_rotation` + `stocks_invest_watchlist_30d_thesis`: **0×** (DEPRECATED/REMOVED; never sized; not paused-to-return).\n"
            "- `stocks_swing_growth_breakout`: **0×** (NEW shadow-only research framework; separate; not actionable/sized).\n"
            "- C-tier / watchlist / shadow: **0×** (informational only).\n"
            "- All other playbooks at 1.0×.\n"
            "- Raw R is **never modified**; this section only shows what the portfolio R would be under sizing discipline.\n"
        )
    except Exception as exc:
        sized_section = (
            "\n\n---\n\n"
            "## 💰 Raw R vs Sized R\n\n"
            f"_Section skipped this run: {type(exc).__name__}: {exc}_\n"
        )

    body = f"""# 📌 Performance by Mode / Tier

_Refreshed: **{_now_eest()}** · Source: `proposed_signals` × latest `signal_outcomes` per signal_id._

> **Headline WR excludes** `waiting_for_entry`, `stale_before_entry`, `entry_moved_away`, `not_triggered`, `expired`, C-tier / watchlist, and shadow candidates. **WR = Wins ÷ (Wins + Losses)**.

---

## 🎯 Headline (actionable A/B, closed-only)

_`netR` below is LEGACY TOUCH R (optimistic highest-TP-touched) — **NOT PnL**. Authoritative PnL is
USD net (`paper_portfolio_ledger.net_pnl_usdt`) and realistic R is `paper_execution_r` in the app._

| Cohort | n | Triggered | Wins | Losses | Closed | **WR** | netR (legacy touch) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Crypto A/B (all modes, closed)** | {crypto_n} | {crypto_trig} | {crypto_W} | {crypto_L} | {crypto_C} | **{crypto_wr}** | {crypto_netR:+.0f}R |
| **Stocks intraday A/B (closed)** | {stocks_n} | {stocks_trig} | {stocks_W} | {stocks_L} | {stocks_C} | **{stocks_wr}** | {stocks_netR:+.0f}R |

_Old stocks swing & invest are DEPRECATED/REMOVED (not paused-to-return) and **not included** in the stocks headline. The new `stocks_swing_growth_breakout` is a separate shadow-only research lane, also excluded from the headline._

---

## 📊 Actionable A/B — by asset class × mode × tier

{chr(10).join(actionable_lines) if actionable_rows else "_No A/B outcomes yet._"}

---

## 📊 Actionable A/B — by direction

{chr(10).join(actionable_dir_lines) if actionable_dir else "_No A/B outcomes yet._"}

---

## 🔬 Watchlist / Counterfactual (C-tier, paused modes — NOT trading performance)

These rows show what watchlist setups would have done if actionable — they validate the pause decisions for stocks_swing and stocks_invest. **They are not Telegram-actionable** and should not be read as "the system is losing".

{chr(10).join(watchlist_lines) if watchlist_rows else "_No C-tier outcomes yet._"}

### By direction (watchlist)

{chr(10).join(watchlist_dir_lines) if watchlist_dir else "_No C-tier outcomes yet._"}
{sized_section}
---

## Column meanings

- **n** — unique setups (`(asset, mode, tier, direction, symbol, day)` tuple). Duplicate signal_ids collapse to one row.
- **Trig / Triggered** — setups where price reached the entry zone (`entry_triggered=1` on at least one duplicate signal_id).
- **Pend*** — setups still pending / expired / not_triggered (= `n − Closed`). Excluded from WR by design.
- **W** (Wins) — closed setups with positive average R across duplicate signal_ids.
- **L** (Losses) — closed setups with negative average R.
- **Closed** — `W + L`. The denominator for WR.
- **WR** — `Wins ÷ Closed × 100`. **Closed-only**, never depressed by pending/expired/not_triggered.
- **Avg R / Total R** — these are the **LEGACY TOUCH R** (old `final_r` = highest-TP-touched,
  OPTIMISTIC) per setup / cumulative. **NOT PnL.** Kept for signal-quality only.
- **Authoritative profitability = USD net** (gross − exchange fees − slippage − funding) from
  `paper_portfolio_ledger.net_pnl_usdt`; realistic R = `paper_execution_r` — both in the
  control-plane app. The R columns on this page are the legacy touch metric, never PnL.

A bucket with **Avg R ≥ +0.5** and **Closed ≥ 30** is usually a stronger signal-quality read (still
legacy-touch, not PnL). Anything below 30 closures is "weak confidence" — don't lean on it yet.

### Why the 2026-06-10 fix changed the numbers
Prior to today this dashboard computed `WR = Wins ÷ n` where `n` included pending/expired/not_triggered. That depressed every WR by a factor of (Closed/n) and produced misleading "16-17%" headlines. The corrected formula uses `Closed` in the denominator so a 0/9 scalp now reads `0%` while a 9/18 swing reads `50%` — matching tab 11's `## 8b. Playbook Performance Snapshot`.

⚠️ **Note vs CLI `signal-stats`**: that tool counts raw signal_ids (inflated). This dashboard counts unique setups (deflated, honest). Numbers will differ — trust this dashboard for edge-checking, use the CLI for raw signal-row inspection.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
"""
    _write(VAULT / "10 📌 Performance by Mode.md", body)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def write_current_state() -> None:
    """Refresh the Trading-Desk Current-State pinned tab.

    Delegates the markdown body to
    ``scripts/write_obsidian_current_state_dashboard.build_page`` so the
    two entry points (refresh cycle / manual standalone run) stay in
    sync. Best-effort: any failure inside the builder is logged and the
    other tabs still refresh.
    """
    try:
        from scripts.write_obsidian_current_state_dashboard import build_page
        body = build_page()
        _write(VAULT / "11 📌 Trading Desk Current State.md", body)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[warn] current-state tab refresh failed: {type(exc).__name__}: {exc}")


def main() -> int:
    VAULT.mkdir(parents=True, exist_ok=True)
    write_dashboard()
    write_active_signals()
    write_trade_history()
    write_todays_catalysts()
    write_latest_reports()
    write_opus_reviews()
    write_telegram_feed()
    write_schedule_status()
    write_rejected_ideas()
    write_macro_heatmap()
    write_performance_breakdown()
    write_current_state()
    print(f"obsidian dashboard refreshed at {_now_eest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
