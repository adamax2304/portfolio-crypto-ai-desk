"""R1 — A/B-only headline performance reporting (presentation only).

Pins that the headline performance metric reflects ACTIONABLE (A/B) signals
only, that C-tier is reported separately as watchlist/research, that the
all-tier diagnostic is still available, and that a negative C-tier never bleeds
into the headline PF. Reporting-only: no scoring / registration / Telegram /
stored-outcome changes are exercised or required.
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone

import pytest

from src import config as _config_mod
from src.config import load_config
from src.signals.analytics import headline_split
from src.signals.config import load_signal_tracking_config
from src.signals.report_section import build_signal_performance_block
from src.storage.sqlite import SQLiteStore


@pytest.fixture
def kit(tmp_path, monkeypatch):
    """Isolated temp DB + config pointed at it (never touches production)."""
    db_file = tmp_path / "ab_headline.sqlite"
    cfg = load_config()
    cfg.settings.setdefault("data", {})["db_path"] = str(db_file)
    # also redirect load_config() used inside report_section
    real = _config_mod.load_config

    def _patched(*a, **k):
        c = real(*a, **k)
        c.settings.setdefault("data", {})["db_path"] = str(db_file)
        return c

    monkeypatch.setattr(_config_mod, "load_config", _patched)
    store = SQLiteStore(cfg.db_path)
    store.init_db()
    return cfg, store


def _insert(store, *, tier, final_r, win, asset_class="stocks", symbol=None):
    sid = f"sig_{tier}_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    status = "tp3_hit" if win else "stopped"
    final_outcome = "win" if win else "loss"
    # Full geometry so the AUTHORITATIVE paper-execution R (Model F) is computable (analytics no
    # longer sums the legacy touch final_r). entry 100 / stop 98 (risk=2); tp1=104 → +2R. A tp1-hit
    # win with MFE ≥ +1R books its +2R under Model F; a stop with low MFE books −1R — so the
    # A/B totals below (+5 / PF 6) reproduce exactly, now from paper_execution_r not final_r.
    mfe = 2.4 if win else 0.0
    with store.connect() as conn:
        conn.execute(
            """INSERT INTO proposed_signals(
                 signal_id, created_at, updated_at, symbol, direction, mode,
                 tier, score, confidence, data_confidence, asset_class, status,
                 entry_low, entry_high, invalidation, tp1, tp2, tp3)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (sid, now, now, symbol or f"{tier}SYM", "long", "intraday",
             tier, 75.0, "high", "medium", asset_class, status,
             100.0, 101.0, 98.0, 102.0, 103.0, 104.0),
        )
        conn.execute(
            """INSERT INTO signal_outcomes(
                 signal_id, checked_at, status, entry_triggered,
                 tp1_hit, tp2_hit, tp3_hit, stop_hit, final_r, final_outcome,
                 max_favorable_excursion_r)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (sid, now, status, 1, 1 if win else 0, 1 if win else 0, 1 if win else 0,
             0 if win else 1, float(final_r), final_outcome, mfe),
        )
    return sid


def _seed(store, asset_class="stocks"):
    # A/B: 3 wins + 1 loss → totalR +5, PF 6.0
    _insert(store, tier="A", final_r=2.0, win=True, asset_class=asset_class)
    _insert(store, tier="A", final_r=2.0, win=True, asset_class=asset_class)
    _insert(store, tier="B", final_r=2.0, win=True, asset_class=asset_class)
    _insert(store, tier="B", final_r=-1.0, win=False, asset_class=asset_class)
    # C: 3 losses → totalR -3, PF 0
    _insert(store, tier="C", final_r=-1.0, win=False, asset_class=asset_class)
    _insert(store, tier="C", final_r=-1.0, win=False, asset_class=asset_class)
    _insert(store, tier="C", final_r=-1.0, win=False, asset_class=asset_class)


# ---------------------------------------------------------------------------
# headline_split data layer
# ---------------------------------------------------------------------------


def test_headline_excludes_ctier(kit):
    cfg, store = kit
    _seed(store)
    tcfg = load_signal_tracking_config(cfg.root)
    split = headline_split(store, config=tcfg, period="all", asset_class="stocks")
    ab = split["actionable"]
    c = split["watchlist"]
    allt = split["all_tier"]
    # Actionable A/B only
    assert ab["sample_size"] == 4
    assert ab["wins"] == 3 and ab["losses"] == 1
    assert ab["total_r"] == 5.0
    assert ab["profit_factor"] == 6.0  # 6 gross win / 1 gross loss — NOT diluted
    # Watchlist C only
    assert c["sample_size"] == 3
    assert c["total_r"] == -3.0
    # All-tier diagnostic includes everything
    assert allt["sample_size"] == 7
    assert allt["total_r"] == 2.0


def test_ab_sample_matches_a_plus_b(kit):
    cfg, store = kit
    _seed(store)
    tcfg = load_signal_tracking_config(cfg.root)
    split = headline_split(store, config=tcfg, period="all", asset_class="stocks")
    by = split["by_tier"]
    assert by["A"]["sample_size"] == 2
    assert by["B"]["sample_size"] == 2
    assert by["C"]["sample_size"] == 3
    assert split["actionable"]["sample_size"] == by["A"]["sample_size"] + by["B"]["sample_size"]


def test_negative_ctier_does_not_change_headline_pf(kit):
    cfg, store = kit
    _seed(store)
    tcfg = load_signal_tracking_config(cfg.root)
    before = headline_split(store, config=tcfg, period="all", asset_class="stocks")["actionable"]
    # Add MORE losing C-tier signals
    for _ in range(5):
        _insert(store, tier="C", final_r=-3.0, win=False)
    after = headline_split(store, config=tcfg, period="all", asset_class="stocks")["actionable"]
    assert after["total_r"] == before["total_r"] == 5.0
    assert after["profit_factor"] == before["profit_factor"] == 6.0


# ---------------------------------------------------------------------------
# rendered report section
# ---------------------------------------------------------------------------


def test_report_block_has_headline_and_separate_ctier(kit):
    cfg, store = kit
    _seed(store)
    block = build_signal_performance_block(cfg, asset_class="stocks", period="all")
    assert "Headline — Actionable Performance (A/B only)" in block
    assert "C-tier Watchlist / Research Performance" in block
    assert "All-tier diagnostic" in block
    assert "Tier split" in block
    assert "not Telegram-actionable" in block.lower() or "not** \nTelegram" in block.lower() \
        or "telegram-actionable" in block.lower()
    # headline shows the A/B total R (+5), watchlist shows C total R (-3)
    assert "Total R: 5" in block
    assert "Total R: -3" in block


def test_report_block_headline_pf_not_diluted_by_ctier(kit):
    cfg, store = kit
    _seed(store)
    block = build_signal_performance_block(cfg, asset_class="stocks", period="all")
    headline = block.split("C-tier Watchlist")[0]
    # The headline section must carry the A/B PF (6.00), not the all-tier PF.
    assert "PF: 6" in headline
    # The all-tier diagnostic line carries the diluted total (+2).
    diag = block.split("All-tier diagnostic")[1]
    assert "Total R: 2" in diag


def test_reporting_is_read_only(kit):
    cfg, store = kit
    _seed(store)
    with store.connect() as conn:
        before_sig = conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
        before_out = conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0]
    tcfg = load_signal_tracking_config(cfg.root)
    headline_split(store, config=tcfg, period="all", asset_class="stocks")
    build_signal_performance_block(cfg, asset_class="stocks", period="all")
    with store.connect() as conn:
        after_sig = conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
        after_out = conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0]
    assert (before_sig, before_out) == (after_sig, after_out)
