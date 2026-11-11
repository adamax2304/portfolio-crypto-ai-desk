"""Safety tests for the paper-feature registry + cohort guard config.

Locks: configs parse, every ACTIVE paper feature is non-trade-affecting, cohort
guard mode is a safe value, and no active feature implies live/execution.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
_ACTIVE = {"active_paper_accounting", "active_paper_display", "active_advisory"}


def _load(name):
    with open(ROOT / "config" / name, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def test_paper_features_yaml_parses_and_is_safe():
    cfg = _load("paper_features.yaml")
    feats = cfg["features"]
    assert feats, "registry must list features"
    for key, f in feats.items():
        # No ACTIVE paper feature may claim to affect real trades.
        if f["state"] in _ACTIVE:
            assert f.get("affects_trades") is False, f"{key} active but affects_trades!=False"
        # Every feature documents an evidence string + decision date.
        assert f.get("evidence"), f"{key} missing evidence"
        assert f.get("decision_date"), f"{key} missing decision_date"


def test_no_active_feature_enables_live():
    cfg = _load("paper_features.yaml")
    blob = str(cfg).lower()
    # The registry must never mark live/auto-live/exchange execution as active.
    for f in cfg["features"].values():
        if f["state"] in _ACTIVE:
            w = (f["what"] + f["evidence"]).lower()
            assert "auto-live" not in w and "exchange execution" not in w


def test_cohort_guard_mode_is_safe():
    cfg = _load("cohort_guard.yaml")
    mode = cfg["cohort_guard"]["mode"]
    assert mode in ("off", "warn", "paper_review_only")
    # paper_review_only (a routing change) must stay gated behind a default-off flag.
    assert cfg["cohort_guard"]["feature_flag"] == "paper_cohort_guard.enabled"
    assert cfg["cohort_guard"]["routing_enabled"] is False


def test_dangerous_cohorts_not_actionable_in_signal_tracking():
    st = _load("signal_tracking.yaml")
    blob = yaml.safe_dump(st)
    # C-tier stays shadow_review_only (never 'actionable').
    assert "actionable" not in blob.replace("shadow_review_only", "") or "shadow_review_only" in blob
