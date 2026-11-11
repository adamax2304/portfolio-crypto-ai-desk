"""Open intraday lifecycle review (operational deploy PART 4).

Read-only. Labels currently open/pending/triggered intraday signals with their
lifecycle state and lists the ones that need a next-session review (carryover,
stale, expired-at-0R candidates). NEVER force-closes, expires, or resizes — it only
writes reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md for the operator.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import load_config  # noqa: E402
from src.signals.lifecycle import compute_lifecycle_label  # noqa: E402
from src.storage.sqlite import SQLiteStore  # noqa: E402

OUT = ROOT / "reports" / "OPEN_INTRADAY_LIFECYCLE_REVIEW.md"
NEEDS_REVIEW = {"intraday_carryover", "intraday_carryover_requires_review",
                "stale_intraday", "expired_at_0R_candidate"}


def main():
    now = datetime.now(timezone.utc)
    cfg = load_config()
    store = SQLiteStore(cfg.db_path)

    regime_now = None
    try:
        from src.risk.risk_off import compute_risk_off
        regime_now = compute_risk_off(now=now).get("regime_context")
    except Exception:
        pass

    try:
        active = store.load_active_signals()
    except Exception:
        active = []

    labeled = []
    for s in active:
        if str(s.get("mode") or "").lower() != "intraday":
            continue
        entry_at = None
        try:
            o = store.load_latest_outcome(s.get("signal_id"))
            entry_at = (o or {}).get("entry_triggered_at")
        except Exception:
            pass
        lc = compute_lifecycle_label(
            s, now=now, entry_triggered_at=entry_at, status=s.get("status"),
            regime_at_entry=s.get("market_regime"), regime_now=regime_now)
        labeled.append((s, lc))

    review = [(s, lc) for s, lc in labeled if lc["lifecycle_label"] in NEEDS_REVIEW
              or lc.get("next_day_revalidation_required")]

    lines = [
        "# Open Intraday — Lifecycle Review (PART 4)", "",
        f"**As of:** {now.isoformat()} · open intraday signals: {len(labeled)} · "
        f"**needing review: {len(review)}**",
        "**Read-only — nothing is force-closed or expired. Operator decides.**", "",
        "## Needs next-session review",
        "| symbol | asset | tier | dir | status | lifecycle | held_h | carryover | revalidate | regime_changed |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for s, lc in sorted(review, key=lambda x: -(x[1].get("held_hours") or 0)):
        lines.append(
            f"| {s.get('symbol')} | {s.get('asset_class')} | {s.get('tier')} | "
            f"{s.get('direction')} | {s.get('status')} | {lc['lifecycle_label']} | "
            f"{lc.get('held_hours')} | {lc.get('carryover_warning')} | "
            f"{lc.get('next_day_revalidation_required')} | {lc.get('regime_changed_since_entry')} |")
    if not review:
        lines.append("| — | — | — | — | — | (none) | — | — | — | — |")

    # full lifecycle distribution
    from collections import Counter
    dist = Counter(lc["lifecycle_label"] for _, lc in labeled)
    lines += ["", "## All open intraday — lifecycle distribution"]
    for k, v in dist.most_common():
        lines.append(f"- {k}: {v}")
    if not labeled:
        lines.append("- (no open intraday signals)")
    lines += ["", "_Diagnostic labels only. No force-close, no expiry change, no resize._"]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} · open_intraday={len(labeled)} · needs_review={len(review)}")


if __name__ == "__main__":
    main()
