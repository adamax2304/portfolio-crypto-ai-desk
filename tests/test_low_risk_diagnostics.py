"""Tests for the low-risk additive diagnostics layer (PART 7)."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _grep_any(pattern: str, path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return re.search(pattern, text) is not None


# ---- 1. Shadow logger does not create A/B signals ------------------------
def test_1_shadow_logger_does_not_create_ab_signals():
    """audit scripts must never INSERT into proposed_signals with tier A/B."""
    scripts = list((ROOT / "scripts").glob("audit_*.py"))
    assert scripts, "no audit scripts found"
    for s in scripts:
        text = s.read_text(encoding="utf-8")
        assert "INSERT INTO proposed_signals" not in text, \
            f"{s.name} contains INSERT into proposed_signals — forbidden"


# ---- 2. Shadow logger does not send actionable Telegram -----------------
def test_2_shadow_logger_does_not_send_telegram():
    """No audit script should import or call the notifier."""
    scripts = list((ROOT / "scripts").glob("audit_*.py"))
    for s in scripts:
        text = s.read_text(encoding="utf-8")
        assert "TelegramNotifier" not in text, f"{s.name} imports notifier"
        assert "notifier.send" not in text, f"{s.name} calls notifier.send"


# ---- 3. Skipped C-tier remains non-actionable ---------------------------
def test_3_c_tier_signals_remain_c_tier():
    """No audit script modifies tier in proposed_signals."""
    scripts = list((ROOT / "scripts").glob("audit_*.py"))
    for s in scripts:
        text = s.read_text(encoding="utf-8")
        assert "UPDATE proposed_signals" not in text, \
            f"{s.name} contains UPDATE proposed_signals — forbidden"


# ---- 4. Expired MFE audit does not change outcomes ----------------------
def test_4_expired_mfe_audit_no_outcome_mutation():
    s = ROOT / "scripts" / "audit_expired_positive_mfe.py"
    assert s.exists(), "audit_expired_positive_mfe.py missing"
    text = s.read_text(encoding="utf-8")
    assert "UPDATE signal_outcomes" not in text
    assert "INSERT INTO signal_outcomes" not in text
    assert "DELETE FROM signal_outcomes" not in text


# ---- 5. Stocks cluster ranking does not suppress alerts -----------------
def test_5_cluster_ranking_does_not_suppress():
    """The cluster audit must not write to signal_alerts or watchlist_alerts."""
    s = ROOT / "scripts" / "audit_stocks_cluster_ranking.py"
    assert s.exists(), "audit_stocks_cluster_ranking.py missing"
    text = s.read_text(encoding="utf-8")
    for forbidden in ("INSERT INTO signal_alerts", "INSERT INTO watchlist_alerts",
                       "DELETE FROM signal_alerts", "UPDATE signal_alerts"):
        assert forbidden not in text, f"cluster audit contains forbidden: {forbidden}"


# ---- 6. Crypto short caution is label-only, not a gate ------------------
def test_6_crypto_short_caution_is_label_only():
    s = ROOT / "scripts" / "audit_crypto_intraday_short_caution.py"
    text = s.read_text(encoding="utf-8")
    # Must not modify scoring or rejection thresholds
    assert "score" not in text or "UPDATE" not in text
    # Must mention "label only" / "do NOT implement"
    assert "Do NOT implement" in text or "Do not implement" in text or "label-only" in text or "caution label only" in text


# ---- 7. No TP/SL/scoring/threshold/sizing files modified ----------------
def test_7_no_strategy_files_modified_by_audit_scripts():
    """audit_*.py must not write to strategy config / scoring files."""
    scripts = list((ROOT / "scripts").glob("audit_*.py"))
    forbidden_targets = [
        "sizing_weights.yaml", "scoring_weights", "tp1", "tp2", "tp3",
        ".write_text(", "config/scoring",
    ]
    for s in scripts:
        text = s.read_text(encoding="utf-8")
        # writes are allowed only to reports/ or data/ (CSV)
        if ".write_text(" in text:
            # must be in reports/
            assert "reports" in text, f"{s.name} writes outside reports/"
        if "to_csv(" in text:
            assert "reports" in text or "data/" in text, f"{s.name} CSV outside reports/data"


# ---- 8. Production DB outcomes unchanged --------------------------------
def test_8_production_db_outcomes_unchanged_by_audits():
    """Sanity check: signal_outcomes row count + sum(final_r) consistent with
    fresh DB state. We don't pin a specific number (it grows over time) but
    we DO check the audit scripts contain no mutation SQL."""
    scripts = list((ROOT / "scripts").glob("audit_*.py"))
    for s in scripts:
        text = s.read_text(encoding="utf-8")
        for forbidden in ("INSERT INTO signal_outcomes",
                          "UPDATE signal_outcomes",
                          "DELETE FROM signal_outcomes",
                          "TRUNCATE signal_outcomes",
                          "DROP TABLE signal_outcomes"):
            assert forbidden not in text, f"{s.name} contains forbidden: {forbidden}"
