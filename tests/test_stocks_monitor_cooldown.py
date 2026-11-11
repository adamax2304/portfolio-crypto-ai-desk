"""Regression tests for PART 2 fix — 45-min per-signal cooldown.

The 12h cycle-2 monitor fired 78 alerts in ~1h because the same 8–10 A/B
setups re-fired ``entry_change`` on every 0.5 % wobble. These tests pin
the new behavior:

  * ``new_signal`` and ``tier_upgrade`` bypass the cooldown — they are
    always material.
  * ``score_improvement`` / ``entry_change`` / ``invalidation_change``
    are suppressed when the last alert was sent inside the cooldown
    window. ``decision.alert_type == 'cooldown'`` and
    ``decision.should_send is False``.
  * After the cooldown elapses, the same material change fires normally.

The checker is pure logic — these tests use ``now`` injection rather
than mocking the system clock.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.stocks.monitor import (
    COOLDOWN_BYPASS_TYPES,
    DEFAULT_COOLDOWN_MINUTES,
    MaterialImprovementChecker,
)


def _last_alert(
    *,
    sent_at: datetime,
    tier: str = "B",
    score: float = 75.0,
    entry_low: float = 102.0,
    entry_high: float = 103.0,
    invalidation: float = 100.0,
) -> dict:
    import json

    return {
        "tier": tier,
        "score": score,
        "sent_at": sent_at.isoformat(),
        "payload_json": json.dumps(
            {
                "entry_low": entry_low,
                "entry_high": entry_high,
                "invalidation": invalidation,
            }
        ),
    }


def test_default_cooldown_is_45_minutes():
    assert DEFAULT_COOLDOWN_MINUTES == 45.0


def test_cooldown_bypass_types_include_new_signal_and_tier_upgrade():
    assert "new_signal" in COOLDOWN_BYPASS_TYPES
    assert "tier_upgrade" in COOLDOWN_BYPASS_TYPES
    # Soft updates are NOT in the bypass set — they go through cooldown.
    assert "entry_change" not in COOLDOWN_BYPASS_TYPES
    assert "invalidation_change" not in COOLDOWN_BYPASS_TYPES
    assert "score_improvement" not in COOLDOWN_BYPASS_TYPES


def test_entry_change_within_cooldown_is_suppressed():
    """The exact 78-alert cycle-2 scenario: same B-tier setup with mid
    entry drifting 1% within 5 minutes of the last alert."""

    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    five_min_ago = now - timedelta(minutes=5)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={
            "tier": "B",
            "invalidation": 100.0,
            "score": 75.0,
            "entry_low": 103.0,  # 1 % up vs 102 mid
            "entry_high": 104.0,
        },
        last_alert=_last_alert(sent_at=five_min_ago),
        now=now,
    )
    assert decision.should_send is False
    assert decision.alert_type == "cooldown"
    assert "entry_change" in decision.reason
    assert "40.0 min" in decision.reason  # 45 - 5 = 40 remaining


def test_invalidation_change_within_cooldown_is_suppressed():
    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    twenty_min_ago = now - timedelta(minutes=20)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 95.0, "score": 75.0},
        last_alert=_last_alert(sent_at=twenty_min_ago),
        now=now,
    )
    assert decision.should_send is False
    assert decision.alert_type == "cooldown"


def test_score_improvement_within_cooldown_is_suppressed():
    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    ten_min_ago = now - timedelta(minutes=10)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0, score_threshold=5.0)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 100.0, "score": 82.0},  # +7 vs 75
        last_alert=_last_alert(sent_at=ten_min_ago, score=75.0),
        now=now,
    )
    assert decision.should_send is False
    assert decision.alert_type == "cooldown"


def test_entry_change_after_cooldown_elapses_fires_normally():
    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    fifty_min_ago = now - timedelta(minutes=50)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={
            "tier": "B",
            "invalidation": 100.0,
            "score": 75.0,
            "entry_low": 103.0,
            "entry_high": 104.0,
        },
        last_alert=_last_alert(sent_at=fifty_min_ago),
        now=now,
    )
    assert decision.should_send is True
    assert decision.alert_type == "entry_change"


def test_tier_upgrade_bypasses_cooldown():
    """B → A must always fire even one minute after the last alert."""

    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    one_min_ago = now - timedelta(minutes=1)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={"tier": "A", "invalidation": 100.0, "score": 82.0},
        last_alert=_last_alert(sent_at=one_min_ago, tier="B"),
        now=now,
    )
    assert decision.should_send is True
    assert decision.alert_type == "tier_upgrade"


def test_new_signal_bypasses_cooldown():
    """A brand-new signal (last_alert=None) is always material."""

    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={"tier": "B", "invalidation": 100.0, "score": 75.0},
        last_alert=None,
    )
    assert decision.should_send is True
    assert decision.alert_type == "new_signal"


def test_cooldown_failopen_when_sent_at_missing():
    """If a legacy alert row lacks ``sent_at`` we don't block — fail-open
    keeps backward compatibility with the existing test_stocks_monitor_alerts
    suite (which builds last_alert dicts without sent_at)."""

    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={
            "tier": "B",
            "invalidation": 100.0,
            "score": 75.0,
            "entry_low": 110.0,
            "entry_high": 111.0,
        },
        last_alert={
            "tier": "B",
            "score": 75.0,
            "payload_json": '{"entry_low": 102.0, "entry_high": 103.0, "invalidation": 100.0}',
            # NO sent_at — should fail-open to alert
        },
    )
    assert decision.should_send is True
    assert decision.alert_type == "entry_change"


def test_cooldown_failopen_when_sent_at_unparseable():
    now = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    decision = checker.decide(
        current={
            "tier": "B",
            "invalidation": 100.0,
            "score": 75.0,
            "entry_low": 110.0,
            "entry_high": 111.0,
        },
        last_alert={
            "tier": "B",
            "score": 75.0,
            "sent_at": "not-a-date",
            "payload_json": '{"entry_low": 102.0, "entry_high": 103.0, "invalidation": 100.0}',
        },
        now=now,
    )
    assert decision.should_send is True
    assert decision.alert_type == "entry_change"


def test_cycle2_repro_one_alert_per_setup_per_cooldown_window():
    """Reproduces the 78-alerts-in-1h scenario in miniature: a single
    B-tier setup whose entry mid drifts on every tick. Over 6 ticks
    within 30 minutes we expect at most one alert."""

    checker = MaterialImprovementChecker(cooldown_minutes=45.0)
    base = datetime(2026, 5, 29, 14, 0, 0, tzinfo=timezone.utc)
    # Tick 0 — first alert (new_signal, bypasses cooldown).
    decision = checker.decide(
        current={
            "tier": "B",
            "invalidation": 100.0,
            "score": 75.0,
            "entry_low": 102.0,
            "entry_high": 103.0,
        },
        last_alert=None,
        now=base,
    )
    assert decision.should_send is True
    assert decision.alert_type == "new_signal"

    sent_at = base
    last_alert = _last_alert(sent_at=sent_at)

    cooldown_count = 0
    sent_count = 1
    # All follow-ups drift mid ≥1% from the original 102.5, so each one
    # is a candidate entry_change — but cooldown suppresses every one of
    # them within the 45-min window.
    for minute_offset, entry_mid in [(5, 105.0), (10, 106.0), (20, 107.0),
                                     (30, 108.0), (40, 109.0)]:
        now = base + timedelta(minutes=minute_offset)
        decision = checker.decide(
            current={
                "tier": "B",
                "invalidation": 100.0,
                "score": 75.0,
                "entry_low": entry_mid - 0.5,
                "entry_high": entry_mid + 0.5,
            },
            last_alert=last_alert,
            now=now,
        )
        if decision.should_send:
            sent_count += 1
            last_alert = _last_alert(sent_at=now, entry_low=entry_mid - 0.5,
                                     entry_high=entry_mid + 0.5)
        else:
            assert decision.alert_type == "cooldown", (
                f"at minute {minute_offset} expected cooldown, got "
                f"{decision.alert_type}: {decision.reason}"
            )
            cooldown_count += 1

    assert sent_count == 1, f"only the initial new_signal should send; got {sent_count}"
    assert cooldown_count == 5, "all 5 follow-up entry_change attempts must be cooled down"
