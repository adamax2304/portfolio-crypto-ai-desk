from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.execution import strategy_governance as governance
import yaml


ACTIVATED = "2026-09-28T20:05:00+00:00"


def _micro_policy() -> dict:
    return {
        "activated_at": ACTIVATED,
        "micro_canary": {
            "minimum_closed_before_decision": 10,
            "target_closed": 20,
            "minimum_profit_factor": 1.0,
            "require_positive_net_after_costs": True,
            "maximum_drawdown_r": 5.0,
            "minimum_paired_v3_trades_at_target": 10,
        },
        "evidence_contract": {"paper_exit_version": "live_exit_parity_v3_incremental"},
        "strategies": {
            "sweep": {
                "stage": "micro_canary",
                "activation_at": ACTIVATED,
                "live_strategy_version": "sweep-live-v1",
                "profile_ids": ["sweep-profile-v1"],
            }
        },
        "profile_registry": {"sweep": ["sweep-profile-v1"]},
        "frozen_strategies": {},
    }


def _live_db(path: Path, pnls: list[float]) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE mexc_canary_decisions (
            decision_id TEXT PRIMARY KEY, signal_id TEXT, decision_json TEXT
        )""")
        conn.execute("""CREATE TABLE mexc_canary_positions (
            decision_id TEXT, status TEXT, closed_at TEXT,
            realized_pnl_usdt REAL, risk_usdt REAL
        )""")
        start = datetime.fromisoformat(ACTIVATED)
        for index, pnl in enumerate(pnls):
            decision_id = f"d-{index}"
            conn.execute(
                "INSERT INTO mexc_canary_decisions VALUES(?,?,?)",
                (decision_id, f"s-{index}", json.dumps({"strategy_version": "sweep-live-v1"})),
            )
            conn.execute(
                "INSERT INTO mexc_canary_positions VALUES(?,?,?,?,?)",
                (
                    decision_id, "CLOSED",
                    (start + timedelta(minutes=index + 1)).isoformat(), pnl, 2.5,
                ),
            )
        conn.commit()


def test_micro_canary_warmup_allows_new_entries(tmp_path: Path) -> None:
    db = tmp_path / "warmup.sqlite"
    _live_db(db, [1.0] * 9)

    result = governance.runtime_route_gate("sweep", db=db, policy=_micro_policy())

    assert result["allowed"] is True
    assert result["verdict"] == "MICRO_CANARY_WARMUP"


def test_micro_canary_auto_demotes_negative_sample(tmp_path: Path) -> None:
    db = tmp_path / "losing.sqlite"
    _live_db(db, [-1.0] * 6 + [0.5] * 4)

    result = governance.runtime_route_gate("sweep", db=db, policy=_micro_policy())

    assert result["allowed"] is False
    assert result["verdict"] == "AUTO_DEMOTED_MICRO_CANARY"
    assert "LIVE_NET_NOT_POSITIVE" in result["reasons"]
    assert "LIVE_PF_BELOW_MINIMUM" in result["reasons"]


def test_canary_target_requires_paired_v3_evidence(tmp_path: Path) -> None:
    db = tmp_path / "target.sqlite"
    _live_db(db, [1.0] * 20)

    result = governance.runtime_route_gate("sweep", db=db, policy=_micro_policy())

    assert result["allowed"] is False
    assert result["verdict"] == "AUTO_DEMOTED_MICRO_CANARY"
    assert "PAIRED_V3_EVIDENCE_MISSING_AT_CANARY_TARGET" in result["reasons"]


def test_paper_metrics_accept_only_clean_live_exit_parity_v3(tmp_path: Path) -> None:
    db = tmp_path / "paper.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("""CREATE TABLE paper_execution_outcomes (
            signal_id TEXT PRIMARY KEY, paper_execution_r REAL, entry_at TEXT,
            exit_at TEXT, computed_at TEXT, path_data_quality TEXT, version TEXT,
            paper_entry_profile TEXT, lifecycle_state TEXT,
            current_price_revalidated INTEGER, entry_time_basis TEXT,
            execution_validity TEXT
        )""")
        conn.execute("""CREATE TABLE paper_portfolio_ledger (
            id INTEGER PRIMARY KEY, signal_id TEXT, event_type TEXT,
            net_pnl_usdt REAL, fees_usdt REAL, slippage_usdt REAL,
            funding_usdt REAL
        )""")
        common = (
            "2026-09-29T14:00:00+00:00", "2026-09-29T15:00:00+00:00",
            "2026-09-29T15:01:00+00:00", "complete", "profile-v1", "CLOSED",
            1, "point_in_time_current_bar", "valid",
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("good", 1.0, *common[:4], "live_exit_parity_v3_incremental", *common[4:]),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            ("legacy", 9.0, *common[:4], "legacy_touch", *common[4:]),
        )
        conn.execute(
            "INSERT INTO paper_portfolio_ledger VALUES(1,'good','exit',8.0,1.0,0.5,0.5)"
        )
        conn.commit()
        result = governance.paper_profile_metrics(
            conn,
            profiles=["profile-v1"],
            activation_at=ACTIVATED,
            exit_version="live_exit_parity_v3_incremental",
        )

    assert result["clean_closed"] == 1
    assert result["net_r"] == 1.0
    assert result["net_pnl_usdt"] == 8.0
    assert result["fees_usdt"] == 1.0
    assert result["rth_sessions"] == 1


def test_profile_registry_rejects_shared_profile_ids() -> None:
    result = governance.validate_profile_registry({
        "profile_registry": {"one": ["shared"], "two": ["shared"]}
    })

    assert result["ok"] is False
    assert result["duplicates"][0]["profile_id"] == "shared"


def test_production_sweep_fingerprint_is_frozen() -> None:
    result = governance.verify_frozen_strategy("crypto_liquidity_sweep_v1")

    assert result["ok"] is True
    assert result["actual"] == result["expected"]


def test_stock_intraday_paper_lanes_match_their_current_research_flags() -> None:
    root = governance.ROOT
    breakout = yaml.safe_load(
        (root / "config/stocks/intraday_breakout_1bar_paper.yaml").read_text(encoding="utf-8")
    )["stocks_intraday_breakout_1bar_paper"]
    pullback = yaml.safe_load(
        (root / "config/paper/stocks/pullback_limit.yaml").read_text(encoding="utf-8")
    )["stocks_intraday_pullback_paper"]
    catalyst = yaml.safe_load(
        (root / "config/paper/stocks/catalyst_rs.yaml").read_text(encoding="utf-8")
    )["stocks_catalyst_rs_paper"]

    assert breakout["enabled"] is True
    assert breakout["live_enabled"] is False
    assert breakout["minimum_distinct_rth_sessions"] == 30
    assert pullback["enabled"] is True
    assert pullback["new_signals_enabled"] is True
    assert pullback["live_enabled"] is False
    assert catalyst["enabled"] is False
    assert catalyst["new_signals_enabled"] is False


def test_llm_is_configured_advisory_only() -> None:
    root = governance.ROOT
    preus = yaml.safe_load(
        (root / "config/stocks/preus_review.yaml").read_text(encoding="utf-8")
    )["preus_review"]["llm_agent"]
    quality = yaml.safe_load(
        (root / "config/quality_agents.yaml").read_text(encoding="utf-8")
    )["quality_agents"]

    assert preus["advisory_only"] is True
    assert preus["apply_to_score"] is False
    assert preus["apply_to_actionability"] is False
    assert quality["operation_mode"] == "shadow"
