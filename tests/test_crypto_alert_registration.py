"""Regression tests for PART 1 fix — crypto legacy alerts must register
into ``proposed_signals`` before Telegram is sent.

These tests cover both alert paths:

  * Supervisor report path (``_maybe_register_signals`` →
    ``_maybe_send_trade_alerts``): registration runs BEFORE alert; the
    map returned is keyed by symbol → signal_id and only those ideas may
    alert.
  * Watchlist monitor path: every complete A/B/C directional candidate is
    registered as a quiet Armed Watch. Only upgraded A/B candidates are
    eligible for a Telegram setup alert.

The tests use an isolated SQLite store; they do not run the full pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.registry import build_signal_from_idea, register_ideas
from src.storage.sqlite import SQLiteStore
from src.utils.validation import model_to_dict


def _store(tmp_path) -> SQLiteStore:
    store = SQLiteStore(tmp_path / "desk.sqlite")
    store.init_db()
    return store


def _tracking_config() -> SignalTrackingConfig:
    # Match production defaults: track A/B; C only when trigger present.
    return SignalTrackingConfig(
        enabled=True,
        track_tiers=("A", "B"),
        track_watchlist_with_trigger=True,
        default_validity_hours={"scalp": 2, "intraday": 24, "swing": 168, "invest": 720},
    )


def _crypto_short_scalp_idea(symbol: str = "UNI/USDT") -> TradeIdea:
    """Reproduces a UNI-style B-tier short scalp with full setup."""

    return TradeIdea(
        symbol=symbol,
        direction="short",
        score=65.5,
        confidence="medium",
        risk_level="medium",
        timeframe="1h thesis / 15m execution",
        tier="B",
        mode="scalp",
        asset_class="crypto",
        exchange_focus="binance",
        exchanges_confirmed=["binance"],
        data_confidence="medium",
        thesis="downtrend continuation, low-vol bounce into resistance",
        evidence=["EMA20 < EMA50", "negative RS vs BTC"],
        counterarguments=["funding negative — crowded short"],
        entry_plan="short into 3.005–3.020 zone",
        invalidation="reclaim 3.038",
        targets=["TP1 2.967", "TP2 2.935"],
        what_to_monitor=["BTC level"],
        avoid_conditions=["breakout >3.083"],
        data_sources_used=["binance"],
        raw={
            "setup": {
                "entry_low": 3.00541429,
                "entry_high": 3.01984643,
                "invalidation": 3.03748571,
                "tp1": 2.96692857,
                "tp2": 2.93485714,
                "tp3": 2.90278571,
            }
        },
    )


def _crypto_long_swing_idea(symbol: str = "INJ/USDT") -> TradeIdea:
    """Reproduces an INJ-style B-tier long swing with full setup."""

    return TradeIdea(
        symbol=symbol,
        direction="long",
        score=66.1,
        confidence="medium",
        risk_level="medium",
        timeframe="4h / daily",
        tier="B",
        mode="swing",
        asset_class="crypto",
        exchange_focus="binance",
        exchanges_confirmed=["binance"],
        data_confidence="medium",
        thesis="uptrend continuation",
        evidence=["EMA20 rising"],
        counterarguments=["resistance overhead"],
        entry_plan="long 5.98–6.05",
        invalidation="lose 5.88",
        targets=["TP1 6.26"],
        what_to_monitor=["BTC level"],
        avoid_conditions=["sweep below 5.88"],
        data_sources_used=["binance"],
        raw={
            "setup": {
                "entry_low": 5.97603929,
                "entry_high": 6.05424286,
                "invalidation": 5.88045714,
                "tp1": 6.26278571,
                "tp2": 6.43657143,
                "tp3": 6.61035714,
            }
        },
    )


def _idea_without_invalidation() -> TradeIdea:
    """An A-tier idea missing entry/invalidation — must NOT register."""

    return TradeIdea(
        symbol="ZZZ/USDT",
        direction="long",
        score=82.0,
        confidence="high",
        risk_level="medium",
        timeframe="1h",
        tier="A",
        mode="intraday",
        asset_class="crypto",
        exchange_focus="binance",
        exchanges_confirmed=["binance"],
        data_confidence="medium",
        thesis="no setup yet",
        evidence=[],
        counterarguments=[],
        entry_plan="wait",
        invalidation="tbd",
        targets=[],
        what_to_monitor=[],
        avoid_conditions=[],
        data_sources_used=[],
        raw={"setup": {}},  # NO entry / invalidation
    )


# ---------------------------------------------------------------------------
# Report-path: register_ideas + signal_id link
# ---------------------------------------------------------------------------


def test_crypto_short_scalp_registers_to_proposed_signals(tmp_path) -> None:
    store = _store(tmp_path)
    idea = _crypto_short_scalp_idea()
    result = register_ideas(
        store,
        [idea],
        config=_tracking_config(),
        report_id="test-report-1",
    )
    assert result.inserted == 1
    assert len(result.signal_ids) == 1
    # Verify the row exists with direction=short, tier=B.
    with store.connect() as conn:
        row = conn.execute(
            "SELECT symbol,direction,mode,tier FROM proposed_signals WHERE signal_id=?",
            (result.signal_ids[0],),
        ).fetchone()
    assert row is not None
    assert row["symbol"] == "UNI/USDT"
    assert row["direction"] == "short"
    assert row["mode"] == "scalp"
    assert row["tier"] == "B"


def test_crypto_long_swing_registers_to_proposed_signals(tmp_path) -> None:
    store = _store(tmp_path)
    idea = _crypto_long_swing_idea()
    result = register_ideas(
        store,
        [idea],
        config=_tracking_config(),
        report_id="test-report-2",
    )
    assert result.inserted == 1


def test_ab_idea_missing_invalidation_does_not_register(tmp_path) -> None:
    """A high score without a structural stop is research-only, not a watch."""

    store = _store(tmp_path)
    idea = _idea_without_invalidation()
    signal = build_signal_from_idea(
        idea,
        config=_tracking_config(),
        report_id="test-report-3",
    )
    assert signal is None
    result = register_ideas(
        store,
        [idea],
        config=_tracking_config(),
        report_id="test-report-3",
    )
    assert result.inserted == 0
    assert result.skipped_no_trigger == 1


def test_wrong_side_structural_stop_does_not_register(tmp_path) -> None:
    """A long stop above entry is not valid Armed Watch geometry."""

    store = _store(tmp_path)
    idea = _crypto_long_swing_idea()
    idea.raw["setup"]["invalidation"] = 6.20
    result = register_ideas(
        store,
        [idea],
        config=_tracking_config(),
        report_id="test-report-wrong-stop",
    )
    assert result.inserted == 0
    assert result.skipped_no_trigger == 1


def test_register_ideas_signal_ids_are_unique_per_idea(tmp_path) -> None:
    store = _store(tmp_path)
    ideas = [
        _crypto_short_scalp_idea("UNI/USDT"),
        _crypto_short_scalp_idea("BCH/USDT"),
        _crypto_long_swing_idea("INJ/USDT"),
        _crypto_long_swing_idea("XLM/USDT"),
    ]
    result = register_ideas(
        store,
        ideas,
        config=_tracking_config(),
        report_id="test-report-4",
    )
    assert result.inserted == 4
    assert len(set(result.signal_ids)) == 4


def test_register_ideas_dedupes_on_second_call(tmp_path) -> None:
    store = _store(tmp_path)
    idea = _crypto_short_scalp_idea()
    first = register_ideas(
        store, [idea], config=_tracking_config(), report_id="rid-A"
    )
    second = register_ideas(
        store, [idea], config=_tracking_config(), report_id="rid-A"
    )
    assert first.inserted == 1
    assert second.inserted == 0
    assert second.skipped_existing == 1


# ---------------------------------------------------------------------------
# 2026-07-13 audit: portfolio-level guard blocks registration for BOTH asset
# classes when the combined book is in severe drawdown.
# ---------------------------------------------------------------------------
def test_register_ideas_blocked_by_portfolio_guard(tmp_path, monkeypatch) -> None:
    import src.signals.registry as reg_mod

    monkeypatch.setattr(
        "src.risk.portfolio_guard.blocks_new_signals",
        lambda **kw: (True, "combined -8R over 10 resolved trades (crypto -5R, stocks -3R)"),
    )
    store = _store(tmp_path)
    ideas = [_crypto_short_scalp_idea("UNI/USDT"), _crypto_long_swing_idea("INJ/USDT")]
    result = reg_mod.register_ideas(store, ideas, config=_tracking_config(), report_id="rid-guard")
    assert result.inserted == 0
    assert result.skipped_portfolio_guard == 2
    assert "combined" in result.portfolio_guard_reason
    with store.connect() as conn:
        n = conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
    assert n == 0


def test_register_ideas_not_blocked_when_portfolio_guard_ok(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "src.risk.portfolio_guard.blocks_new_signals",
        lambda **kw: (False, "ok"),
    )
    store = _store(tmp_path)
    idea = _crypto_short_scalp_idea()
    result = register_ideas(store, [idea], config=_tracking_config(), report_id="rid-guard-ok")
    assert result.inserted == 1
    assert result.skipped_portfolio_guard == 0


# ---------------------------------------------------------------------------
# Watchlist monitor path: Armed Watch registration
# ---------------------------------------------------------------------------


@dataclass
class _FakeTick:
    """Minimal tick stand-in for a watchlist-monitor tick.

    The real ``WatchlistTick`` has the same shape; for the unit test we
    rebuild ideas directly from the payload, exactly like production.
    """

    symbol: str
    previous_tier: str
    new_tier: str
    score: float
    direction: str
    mode: str
    payload: dict
    upgraded: bool = True

    @property
    def is_actionable(self) -> bool:
        return (
            self.upgraded
            and self.new_tier in {"A", "B"}
            and self.direction in {"long", "short"}
        )


def _tick_from(idea: TradeIdea, *, previous_tier: str = "C") -> _FakeTick:
    return _FakeTick(
        symbol=idea.symbol,
        previous_tier=previous_tier,
        new_tier=idea.tier,
        score=float(idea.score),
        direction=idea.direction,
        mode=idea.mode,
        payload=model_to_dict(idea),
        upgraded=True,
    )


def test_watchlist_tick_payload_rebuilds_into_tradeidea(tmp_path) -> None:
    """The reconstruction step inside Armed Watch registration."""

    idea = _crypto_short_scalp_idea()
    tick = _tick_from(idea)
    rebuilt = TradeIdea(**tick.payload)
    assert rebuilt.symbol == idea.symbol
    assert rebuilt.direction == idea.direction
    assert rebuilt.tier == idea.tier
    assert rebuilt.mode == idea.mode
    raw_setup = (rebuilt.raw or {}).get("setup") or {}
    assert raw_setup.get("entry_low") == 3.00541429
    assert raw_setup.get("invalidation") == 3.03748571


def test_watchlist_ctier_tick_is_not_actionable() -> None:
    idea = _crypto_short_scalp_idea()
    tick = _FakeTick(
        symbol=idea.symbol,
        previous_tier="rejected",
        new_tier="C",
        score=55.0,
        direction=idea.direction,
        mode=idea.mode,
        payload=model_to_dict(idea),
        upgraded=True,
    )
    assert tick.is_actionable is False


def test_watchlist_ctier_tick_is_an_armed_watch_candidate(tmp_path, monkeypatch) -> None:
    from types import SimpleNamespace

    from src.agents.watchlist_monitor import WatchlistMonitor, WatchlistTick

    store = _store(tmp_path)
    idea = _crypto_long_swing_idea()
    payload = model_to_dict(idea)
    payload["tier"] = "C"
    tick = WatchlistTick(
        symbol=idea.symbol,
        previous_tier="rejected",
        new_tier="C",
        score=55.0,
        direction=idea.direction,
        mode=idea.mode,
        payload=payload,
        upgraded=False,
    )
    assert tick.is_armed_watch_candidate is True
    assert tick.is_actionable is False

    monkeypatch.setattr(
        "src.signals.config.load_signal_tracking_config",
        lambda _root: _tracking_config(),
    )
    monitor = WatchlistMonitor(
        SimpleNamespace(root=tmp_path, settings={}),
        file_store=SimpleNamespace(),
        db=store,
    )
    signal_ids = monitor.register_armed_watch_candidates([tick])

    assert idea.symbol in signal_ids
    row = store.load_signal(signal_ids[idea.symbol])
    assert row is not None
    assert row["tier"] == "C"
    assert row["status"] == "waiting_for_entry"


def test_watchlist_no_direction_tick_is_not_actionable() -> None:
    idea = _crypto_short_scalp_idea()
    tick = _FakeTick(
        symbol=idea.symbol,
        previous_tier="C",
        new_tier="B",
        score=70.0,
        direction="watchlist only",
        mode=idea.mode,
        payload=model_to_dict(idea),
        upgraded=True,
    )
    assert tick.is_actionable is False


def test_signal_id_link_in_watchlist_alert_payload(tmp_path) -> None:
    """When the CLI calls record_watchlist_alert it now passes signal_id
    inside the payload — verify that round-trips through SQLite."""

    store = _store(tmp_path)
    store.record_watchlist_alert(
        symbol="UNI/USDT",
        previous_tier="C",
        new_tier="B",
        score=65.5,
        direction="short",
        mode="scalp",
        payload={"signal_id": "sig_test_link_123", "report_id": "rid-X"},
    )
    last = store.last_alert_for("UNI/USDT")
    assert last is not None
    import json as _json

    payload = _json.loads(last["payload_json"])
    assert payload["signal_id"] == "sig_test_link_123"
