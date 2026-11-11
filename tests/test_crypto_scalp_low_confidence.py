"""Mode-Viability-Audit tests — crypto scalp low-confidence reporting.

The 14d mode viability audit (2026-06-09) confirmed crypto scalp has a
real entry edge (100% of expired had positive MFE, avg +0.54R) but a
TP1/2h horizon mismatch caps capture (1W/7L). We keep scalp ACTIONABLE
but surface a low-confidence banner in user-facing surfaces (crypto
report header + Telegram alert line for scalp signals).

No scoring/TP/SL/routing changes; pure reporting/UI annotation.
"""
from __future__ import annotations

from src.config import load_config
from src.models import MarketRegime
from src.reports.report_builder import ReportBuilder


def _regime() -> MarketRegime:
    return MarketRegime(
        label="transition",
        confidence=0.6,
        risk_mode="mixed",
        recommended_style="wait-for-trigger",
        btc_trend="range",
        eth_trend="range",
        alt_breadth={"above_ema20_pct": 67.0, "above_ema50_pct": 22.0},
        volatility={"label": "normal", "atr_pct": 68.0},
        key_levels={},
        explanation="Sample regime for unit test.",
        warnings=[],
    )


def _builder() -> ReportBuilder:
    cfg = load_config()
    return ReportBuilder(cfg)


# ---------------------------------------------------------------------------
# Crypto report — scalp banner
# ---------------------------------------------------------------------------


def test_scalp_report_renders_low_confidence_banner():
    builder = _builder()
    text = builder.build_daily(
        regime=_regime(),
        candidates=[],
        ideas=[],
        data_freshness="2026-06-09 11:00 UTC",
        mode="scalp",
    )
    assert "CRYPTO SCALP — low confidence" in text
    assert "TP1/2h horizon mismatch" in text
    assert "re-audit at 20 closed" in text


def test_intraday_report_has_no_scalp_banner():
    builder = _builder()
    text = builder.build_daily(
        regime=_regime(),
        candidates=[],
        ideas=[],
        data_freshness="2026-06-09 11:00 UTC",
        mode="intraday",
    )
    assert "CRYPTO SCALP — low confidence" not in text


def test_swing_report_has_no_scalp_banner():
    builder = _builder()
    text = builder.build_daily(
        regime=_regime(),
        candidates=[],
        ideas=[],
        data_freshness="2026-06-09 11:00 UTC",
        mode="swing",
    )
    assert "CRYPTO SCALP — low confidence" not in text


# ---------------------------------------------------------------------------
# Telegram alert (watchlist_monitor.format_alert) — scalp annotation
# ---------------------------------------------------------------------------


def _tick(symbol="ZEC/USDT", mode="scalp", asset_class="crypto"):
    from src.agents.watchlist_monitor import WatchlistTick

    return WatchlistTick(
        symbol=symbol,
        direction="long",
        previous_tier="C",
        new_tier="B",
        mode=mode,
        score=68.0,
        payload={
            "symbol": symbol,
            "asset_class": asset_class,
            "confidence": "medium",
            "thesis": "test thesis",
            "raw": {"setup": {
                "entry_low": 100.0, "entry_high": 101.0,
                "sl": 97.0, "tp1": 106.0, "tp2": 110.0,
            }},
            "cap_reasons": [],
        },
    )


def test_telegram_scalp_alert_includes_low_confidence_line():
    from src.agents.watchlist_monitor import WatchlistMonitor

    text = WatchlistMonitor.format_alert(_tick(mode="scalp", asset_class="crypto"))
    assert "low confidence (mode audit)" in text
    # Make sure entry/SL/TP still rendered — we only annotated, not suppressed.
    assert "entry" in text
    assert "SL" in text


def test_telegram_intraday_alert_has_no_low_confidence_line():
    from src.agents.watchlist_monitor import WatchlistMonitor

    text = WatchlistMonitor.format_alert(_tick(mode="intraday", asset_class="crypto"))
    assert "low confidence (mode audit)" not in text


def test_telegram_stocks_scalp_does_not_get_crypto_note():
    """If asset_class is stocks (hypothetical) the crypto-scalp note must
    not appear — the annotation is scoped to crypto."""
    from src.agents.watchlist_monitor import WatchlistMonitor

    text = WatchlistMonitor.format_alert(_tick(mode="scalp", asset_class="stocks"))
    assert "low confidence (mode audit)" not in text
