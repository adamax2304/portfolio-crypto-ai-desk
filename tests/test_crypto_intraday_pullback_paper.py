from src.execution.crypto_intraday_pullback_paper import load_cfg, resolve_profile
from src.execution.paper_entry_provenance import execution_mode_for_signal


def _signal(**updates):
    row = {
        "signal_id": "intraday-pullback-1",
        "asset_class": "crypto",
        "mode": "intraday",
        "direction": "long",
        "created_at": "2026-09-18T00:01:00+00:00",
    }
    row.update(updates)
    return row


def test_forward_pullback_gets_versioned_paper_profile_without_rewriting_geometry():
    cfg = {**load_cfg(), "activated_at": "2026-09-18T00:00:00+00:00"}
    result = resolve_profile(
        signal=_signal(), source_entry_mode="PULLBACK_LIMIT", cfg=cfg,
    )
    assert result == {
        "applied": True,
        "ready": True,
        "profile_id": "crypto_intraday_pullback_paper_v1",
        "entry_mode": "PULLBACK_LIMIT",
        "source_entry_mode": "PULLBACK_LIMIT",
        "reason": "versioned_intraday_pullback_point_in_time",
    }
    assert load_cfg()["live_enabled"] is True


def test_pullback_profile_never_backfills_or_accepts_a_different_entry_mode():
    cfg = {**load_cfg(), "activated_at": "2026-09-18T00:00:00+00:00"}
    assert resolve_profile(
        signal=_signal(created_at="2026-09-17T23:59:59+00:00"),
        source_entry_mode="PULLBACK_LIMIT", cfg=cfg,
    ) == {"applied": False}
    assert resolve_profile(
        signal=_signal(), source_entry_mode="BREAKOUT_CONTINUATION", cfg=cfg,
    ) == {"applied": False}


def test_pullback_profile_is_authoritative_provenance():
    signal = {
        "paper_entry_profile": "crypto_intraday_pullback_paper_v1",
        "paper_execution_entry_mode": "PULLBACK_LIMIT",
    }
    provenance = execution_mode_for_signal(signal)
    assert provenance is not None
    assert provenance.entry_mode == "PULLBACK_LIMIT"
    assert provenance.profile_id == "crypto_intraday_pullback_paper_v1"
