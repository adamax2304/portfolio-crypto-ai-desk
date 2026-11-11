"""Catalyst integrity daily monitor (profitability guardrails PART 7).

Read-only. Runs `scan_catalyst_integrity` against the live DB + today's catalyst
artifacts and writes reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md. Optionally prints
a compact warning line (for a future Telegram hook). Never promotes a trade, never
changes scoring. Safe to schedule after the catalyst-scan step.
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.catalysts.integrity import scan_catalyst_integrity  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUT = ROOT / "reports" / "CATALYST_INTEGRITY_DAILY_SUMMARY.md"


def main():
    now = datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    res = scan_catalyst_integrity(conn, now=now, lookback_hours=24)
    conn.close()

    def _fmt_list(v, n=25):
        if v is None:
            return "n/a (artifact missing)"
        if not v:
            return "none"
        return ", ".join(v[:n]) + (" …" if len(v) > n else "")

    lines = [
        "# Catalyst Integrity — Daily Summary (PART 7)",
        "",
        f"**As of:** {res['as_of']} · **Status:** `{res['catalyst_integrity_status']}`"
        f" · **Confidence:** {res['catalyst_mapping_confidence']}"
        f" · **Warning:** {res['warning']}",
        "",
        "## Counts",
        f"- High-importance (>=1.0) symbol-tagged news_items (all-time): "
        f"**{res['high_importance_symbol_tagged']}**",
        f"- Catalyst symbols in last 24h: **{len(res['catalyst_symbols'])}** — {_fmt_list(res['catalyst_symbols'])}",
        f"- Mapped into today's catalyst_events: "
        f"{'n/a' if res['mapped_event_symbols'] is None else len(res['mapped_event_symbols'])}",
        f"- **Raw-news symbols outside the narrower catalyst artifact scope:** "
        f"{res['unmapped_high_importance_count'] if res['unmapped_high_importance_count'] is not None else 'n/a'}"
        f" — {_fmt_list(res['unmapped_high_importance_symbols'])}",
        f"- **No-catalyst basket symbols with direct news hits (regression signature):** "
        f"{_fmt_list(res['no_catalyst_basket_news_hits'])}",
        "",
        "## Warnings",
    ]
    if res["warnings"]:
        lines += [f"- ⚠ {w}" for w in res["warnings"]]
    else:
        lines.append("- none — catalyst mapping consistent")
    lines += [
        "",
        "## Interpretation",
        "- `direct_news_items_checked` is True — the no-catalyst label is only applied "
        "after a direct `news_items` lookup (the ASTER fix).",
        "- A non-empty *regression signature* list means a momentum/no-catalyst basket "
        "still contains a symbol that has a direct high-importance news hit. If this is "
        "from an on-disk artifact written before the fix, re-run the catalyst-scan to "
        "regenerate `narrative_baskets.jsonl` with the fixed builder; if it persists "
        "after a fresh scan, the fix has regressed — investigate.",
        "- Raw-news symbols not emitted into `catalyst_events` are reported as coverage "
        "diagnostics only: that artifact intentionally excludes diffuse/non-actionable headlines. "
        "They are not a mapping failure unless the regression signature is also present.\n"
        "- This monitor never promotes a symbol to actionable; ASTER-like names remain "
        "catalyst-backed watch-on-pullback.",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    if res["warning"]:
        print("WARNING:", "; ".join(res["warnings"]))


if __name__ == "__main__":
    main()
