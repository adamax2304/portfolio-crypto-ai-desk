"""Regression tests for PART 5 fix — minimal daily review aggregator.

The Obsidian daily review was a stub printing "not implemented". This
test pins the new behavior: the aggregator reads ``proposed_signals``,
``trade_ideas``, ``watchlist_alerts`` etc. and renders a markdown note
without crashing on empty days.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.signals.daily_review import (
    VAULT_DAILY_REVIEWS,
    aggregate_daily_review,
    render_daily_review,
)
from src.storage.sqlite import SQLiteStore


def _store(tmp_path) -> SQLiteStore:
    store = SQLiteStore(tmp_path / "desk.sqlite")
    store.init_db()
    return store


def _insert_signal(
    store: SQLiteStore,
    *,
    signal_id: str,
    symbol: str,
    tier: str,
    direction: str,
    mode: str,
    asset_class: str = "crypto",
    score: float = 70.0,
    created_at: str | None = None,
    no_entry_conditions: list[str] | None = None,
) -> None:
    created = created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO proposed_signals(
                signal_id, created_at, updated_at, symbol, direction, mode, tier,
                score, confidence, data_confidence, asset_class, status,
                entry_low, entry_high, invalidation, no_entry_conditions_json
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal_id, created, created, symbol, direction, mode, tier,
                score, "medium", "medium", asset_class, "waiting_for_entry",
                100.0, 101.0, 98.0,
                json.dumps(no_entry_conditions or []),
            ),
        )


def test_empty_day_renders_skeleton(tmp_path):
    store = _store(tmp_path)
    data = aggregate_daily_review(store, date="2026-01-01")
    md = render_daily_review(data)
    assert "Daily Review — 2026-01-01" in md
    assert "No signals registered today." in md
    assert "Reports Generated" in md
    assert "A-tier signals" in md
    assert "Manual notes" in md


def test_aggregates_signals_by_tier(tmp_path):
    store = _store(tmp_path)
    base = "2026-05-29T10:00:00+00:00"
    _insert_signal(store, signal_id="sig_uni", symbol="UNI/USDT", tier="B",
                   direction="short", mode="scalp", score=65.5, created_at=base)
    _insert_signal(store, signal_id="sig_inj", symbol="INJ/USDT", tier="B",
                   direction="long", mode="swing", score=66.1, created_at=base)
    _insert_signal(store, signal_id="sig_aapl", symbol="AAPL", tier="A",
                   direction="long", mode="intraday", asset_class="stocks",
                   score=83.4, created_at=base)

    data = aggregate_daily_review(store, date="2026-05-29")
    assert len(data.signals_by_tier.get("B") or []) == 2
    assert len(data.signals_by_tier.get("A") or []) == 1
    assert data.counts_by_asset_class["crypto"]["B"] == 2
    assert data.counts_by_asset_class["stocks"]["A"] == 1

    md = render_daily_review(data)
    assert "**AAPL**" in md
    assert "UNI/USDT" in md and "INJ/USDT" in md


def test_legal_block_surfaced_in_review(tmp_path):
    """Cross-cuts PART 3: an A-tier signal with the legal-risk marker
    appears in the dedicated 'Legal / headline-risk blocks' section."""

    store = _store(tmp_path)
    base = "2026-05-29T10:00:00+00:00"
    _insert_signal(
        store,
        signal_id="sig_smci",
        symbol="SMCI",
        tier="A",
        direction="long",
        mode="intraday",
        asset_class="stocks",
        score=82.52,
        created_at=base,
        no_entry_conditions=[
            "do not chase",
            "ACTIVE_LEGAL_HEADLINE_RISK: class_action,indictment",
        ],
    )
    data = aggregate_daily_review(store, date="2026-05-29")
    assert len(data.legal_blocks) == 1
    assert data.legal_blocks[0]["symbol"] == "SMCI"
    md = render_daily_review(data)
    assert "Legal / headline-risk blocks" in md
    assert "**SMCI**" in md
    assert "ACTIVE_LEGAL_HEADLINE_RISK" in md


def test_telegram_alerts_aggregated_from_both_ledgers(tmp_path):
    store = _store(tmp_path)
    store.record_watchlist_alert(
        symbol="UNI/USDT",
        previous_tier="C",
        new_tier="B",
        score=65.5,
        direction="short",
        mode="scalp",
        payload={"signal_id": "sig_uni"},
    )
    data = aggregate_daily_review(
        store,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )
    assert any(a.get("symbol") == "UNI/USDT" for a in data.telegram_alerts)
    md = render_daily_review(data)
    assert "UNI/USDT" in md


def test_vault_path_points_to_daily_reviews():
    assert "Daily_Reviews" in str(VAULT_DAILY_REVIEWS)
    assert "11_Trade_Journal" in str(VAULT_DAILY_REVIEWS)
