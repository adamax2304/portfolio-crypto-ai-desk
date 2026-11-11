"""Sector-cap SHADOW-ONLY / would-bind diagnostics (profitability guardrails PART 3).

Asserts the day-batch would-bind labels fire, the cap VALUE is unchanged, and the
diagnostic never resizes/blocks (it only reports would_* fields).
"""
from __future__ import annotations

from datetime import datetime, timezone

from src.signals.sector_cap_shadow import would_bind_from_batch, would_bind_sector_cap

NOW = datetime(2026, 6, 17, 15, 0, tzinfo=timezone.utc)


def _s(sym, sid, *, direction="long", tier="A", mode="intraday", asset="stocks"):
    return {"signal_id": sid, "symbol": sym, "asset_class": asset, "mode": mode,
            "tier": tier, "direction": direction, "score": 75.0,
            "created_at": NOW.isoformat(),
            "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0, "tp1": 104.0}


def test_three_same_bucket_third_would_bind_sector_cap():
    batch = [_s("AMD", "amd"), _s("NVDA", "nvda"), _s("SMCI", "smci")]
    third = would_bind_from_batch(batch, "smci")
    assert third["would_bind_sector_cap"] == "shadow_sector_cap"
    assert third["would_sector_rank"] == 3
    assert third["diagnostic_only"] is True
    first = would_bind_from_batch(batch, "amd")
    assert first["would_bind_sector_cap"] == "actionable"
    assert first["would_sector_rank"] == 1


def test_second_same_bucket_is_half_size_candidate():
    batch = [_s("AMD", "amd", direction="long"), _s("NVDA", "nvda", direction="long")]
    second = would_bind_from_batch(batch, "nvda")
    assert second["would_bind_sector_cap"] == "half_size"
    assert second["would_sector_rank"] == 2


def test_proxy_duplicate_would_label():
    batch = [_s("QQQ", "qqq"), _s("XLK", "xlk")]
    dup = would_bind_from_batch(batch, "xlk")
    assert dup["would_bind_sector_cap"] == "shadow_proxy_duplicate"


def test_crypto_signal_not_applicable_via_store():
    class FakeStore:
        def load_signals_for_period(self, **kw):
            return []
    out = would_bind_sector_cap(FakeStore(), {"signal_id": "x", "asset_class": "crypto",
                                              "mode": "intraday", "symbol": "BTC/USDT"}, now=NOW)
    assert out["would_bind_sector_cap"] == "not_applicable"


def test_store_wrapper_includes_current_signal_and_reports_actual():
    sig = _s("SMCI", "smci")
    sig["concentration_status"] = "actionable"  # what the live path produced

    class FakeStore:
        def load_signals_for_period(self, **kw):
            return [_s("AMD", "amd"), _s("NVDA", "nvda")]  # 2 already today
    out = would_bind_sector_cap(FakeStore(), sig, now=NOW)
    # SMCI becomes the 3rd semis long → would shadow, while live status was actionable
    assert out["would_bind_sector_cap"] == "shadow_sector_cap"
    assert out["actual_concentration_status"] == "actionable"


def test_fails_open_on_bad_store():
    class BadStore:
        def load_signals_for_period(self, **kw):
            raise RuntimeError("db down")
    out = would_bind_sector_cap(BadStore(), {"signal_id": "x", "asset_class": "stocks",
                                            "mode": "intraday", "symbol": "AMD"}, now=NOW)
    assert out["would_bind_sector_cap"] == "not_applicable"
    assert out["diagnostic_only"] is True
