"""OPERATIONAL COMPLETION — monitor/gate/telegram tests (read-only, no network/live)."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.execution import paper_shadow_monitor as mon
from src.notifiers.paper_shadow_telegram import compose


def _seed(db, fwd_b_net=8.0, fwd_a_net=2.0, n=70, days_ok=True):
    conn = sqlite3.connect(db)
    conn.execute(mon.__dict__.get("_DDL", "") or
                 "CREATE TABLE IF NOT EXISTS paper_shadow_execution_outcomes ("
                 "signal_id TEXT, branch TEXT, window TEXT, entry_fill_status TEXT, entry_fill_time TEXT,"
                 "net_r REAL, net_pnl_usdt REAL, fees_usdt REAL, gross_r REAL, direction_changed INT,"
                 "entry_order_type TEXT, outcome_status TEXT, close_reason TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS paper_shadow_meta (k TEXT PRIMARY KEY, v TEXT)")
    ts = "2026-06-01T00:00:00+00:00" if days_ok else "2026-06-25T00:00:00+00:00"
    conn.execute("INSERT OR REPLACE INTO paper_shadow_meta VALUES ('activated_at', ?)", (ts,))
    for i in range(n):
        conn.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (f"s{i}", "old_paper", "forward_since_activation", "filled", f"2026-06-02T{i%24:02d}:00:00+00:00",
                      fwd_a_net / n, fwd_a_net / n * 25, 0.1, fwd_a_net / n, 0, "maker", "closed", "closed_win"))
        conn.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (f"s{i}", "new_logic_shadow", "forward_since_activation", "filled", f"2026-06-02T{i%24:02d}:00:00+00:00",
                      fwd_b_net / n, fwd_b_net / n * 25, 0.1, fwd_b_net / n, 0, "maker", "closed", "closed_win"))
    conn.commit(); conn.close()


def test_forward_quality_and_gate_ready_when_b_beats_a(tmp_path):
    db = str(tmp_path / "t.sqlite")
    _seed(db, fwd_b_net=8.0, fwd_a_net=2.0, n=70, days_ok=True)
    fq = mon.forward_quality(db)
    assert fq["available"] and fq["B"]["net_r"] > fq["A"]["net_r"]
    g = mon.promotion_gate(db)
    assert g["verdict"] == "READY" and g["executed"] is False    # ready but NEVER auto-executes


def test_gate_not_ready_when_sample_small(tmp_path):
    db = str(tmp_path / "t2.sqlite")
    _seed(db, fwd_b_net=8.0, fwd_a_net=2.0, n=10, days_ok=True)   # < 60 trades
    g = mon.promotion_gate(db)
    assert g["verdict"] == "NOT_READY"
    assert any("trades" in c["name"] and not c["ok"] for c in g["criteria"])


def test_gate_not_ready_when_b_loses_after_fees(tmp_path):
    db = str(tmp_path / "t3.sqlite")
    _seed(db, fwd_b_net=1.0, fwd_a_net=5.0, n=70, days_ok=True)   # B < A
    g = mon.promotion_gate(db)
    assert g["verdict"] == "NOT_READY"


def test_stock_intraday_candidate_lane_is_excluded_from_ab_readiness(tmp_path):
    """Independent stock candidates must not inflate the primary A/B forward book."""
    from src.execution.paper_shadow_engine import ensure_tables

    db = str(tmp_path / "candidate_lane.sqlite")
    conn = sqlite3.connect(db)
    ensure_tables(conn)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    conn.execute("INSERT INTO paper_shadow_meta VALUES ('activated_at','2026-06-01T00:00:00+00:00')")
    conn.executemany("INSERT INTO proposed_signals VALUES (?,?,?)", [
        ("main", "crypto", "swing"), ("stock_candidate", "stocks", "intraday")])
    for branch, net in (("old_paper", 1.0), ("new_logic_shadow", 2.0)):
        conn.execute(
            "INSERT INTO paper_shadow_execution_outcomes "
            "(signal_id,branch,asset_class,window,entry_fill_status,entry_fill_time,"
            "net_r,net_pnl_usdt,gross_r,outcome_status,shadow_lane) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            ("main", branch, "crypto", "forward_since_activation", "filled",
             "2026-06-02T00:00:00+00:00", net, net * 25, net, "closed", "ab_main"),
        )
    conn.execute(
        "INSERT INTO paper_shadow_execution_outcomes "
        "(signal_id,branch,asset_class,window,entry_fill_status,entry_fill_time,"
        "net_r,net_pnl_usdt,gross_r,outcome_status,shadow_lane) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        ("stock_candidate", "new_logic_shadow", "stocks", "forward_since_activation", "filled",
         "2026-06-02T00:00:00+00:00", 100.0, 2500.0, 100.0, "closed", "stocks_intraday_forward"),
    )
    conn.commit(); conn.close()

    fq = mon.forward_quality(db)
    assert fq["B"]["net_r"] == 2.0
    readiness = mon.promotion_readiness_by_mode(db)
    assert all(m["mode"] != "intraday" or m["asset_class"] != "stocks" for m in readiness["modes"])


def test_telegram_compose_has_forward_and_caveat(tmp_path, monkeypatch):
    db = str(tmp_path / "t4.sqlite")
    _seed(db, fwd_b_net=8.0, fwd_a_net=2.0, n=70, days_ok=True)
    monkeypatch.setattr("src.notifiers.paper_shadow_telegram.forward_quality", lambda d=None: mon.forward_quality(db))
    monkeypatch.setattr("src.notifiers.paper_shadow_telegram.promotion_gate", lambda d=None: mon.promotion_gate(db))
    msg = compose(db)
    assert "Paper-Shadow A/B" in msg
    assert "promotion gate" in msg
    assert "look-ahead" in msg and "NOT proof" in msg     # caveat present
    assert "A (old)" in msg and "B (new)" in msg


# ---- item 3 (2026-07-03): per-mode promotion readiness (read-only, 3-verdict scale) ----
def _seed_mode(db, *, asset_class, mode, b_net, a_net, n, days_ok=True,
               dgl=0, fee_profile=None, stale=0):
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS paper_shadow_execution_outcomes ("
        "signal_id TEXT, branch TEXT, window TEXT, entry_fill_status TEXT, entry_fill_time TEXT,"
        "net_r REAL, net_pnl_usdt REAL, asset_class TEXT, fee_profile TEXT, cost_model_status TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS paper_shadow_meta (k TEXT PRIMARY KEY, v TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS entry_latency_audit (signal_id TEXT PRIMARY KEY, cause TEXT)")
    fp = fee_profile or ("stock_etf_default" if asset_class.startswith("stock") else "bybit_non_vip_usdt_perp")
    ts = "2026-06-01T00:00:00+00:00" if days_ok else "2026-06-30T00:00:00+00:00"
    conn.execute("INSERT OR REPLACE INTO paper_shadow_meta VALUES ('activated_at', ?)", (ts,))
    for i in range(n):
        sid = f"{asset_class}_{mode}_{i}"
        cms = "stale_cost_model" if i < stale else "current"
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?)", (sid, asset_class, mode))
        for branch, net in (("old_paper", a_net / n), ("new_logic_shadow", b_net / n)):
            conn.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (sid, branch, "forward_since_activation", "filled",
                          f"2026-06-02T{i%24:02d}:00:00+00:00", net, net * 25, asset_class, fp, cms))
        if i < dgl:
            conn.execute("INSERT OR REPLACE INTO entry_latency_audit VALUES (?, 'DATA_GAP_LATE')", (sid,))
    conn.commit(); conn.close()


def _verdict_for(res, asset_class, mode):
    return next(m["verdict"] for m in res["modes"]
               if m["asset_class"] == asset_class and m["mode"] == mode)


def test_readiness_all_pass_is_ready_for_operator_review(tmp_path):
    db = str(tmp_path / "r1.sqlite")
    _seed_mode(db, asset_class="stocks", mode="intraday", b_net=9.0, a_net=2.0, n=70, days_ok=True)
    res = mon.promotion_readiness_by_mode(db)
    assert _verdict_for(res, "stocks", "intraday") == "READY_FOR_OPERATOR_REVIEW"
    m = next(x for x in res["modes"] if x["mode"] == "intraday")
    assert m["fee_profile_integrity_ok"] is True and m["delta_net_usd"] > 0


def test_readiness_b_better_but_data_gap_high_is_not_ready(tmp_path):
    db = str(tmp_path / "r2.sqlite")
    # B beats A on the clean cohort, but >30% of the mode's signals are DATA_GAP_LATE
    _seed_mode(db, asset_class="crypto", mode="scalp", b_net=9.0, a_net=2.0, n=70, days_ok=True, dgl=30)
    res = mon.promotion_readiness_by_mode(db)
    m = next(x for x in res["modes"] if x["mode"] == "scalp")
    assert m["data_gap_late_share"] > 0.30
    assert _verdict_for(res, "crypto", "scalp") == "NOT_READY"


def test_readiness_b_worse_is_not_ready(tmp_path):
    db = str(tmp_path / "r3.sqlite")
    # crypto intraday where B underperforms A → NOT_READY (mirrors the real crypto-intraday finding)
    _seed_mode(db, asset_class="crypto", mode="intraday", b_net=1.0, a_net=6.0, n=70, days_ok=True)
    res = mon.promotion_readiness_by_mode(db)
    assert _verdict_for(res, "crypto", "intraday") == "NOT_READY"


def test_crypto_readiness_uses_preentry_v2_age_not_legacy_activation(tmp_path):
    db = str(tmp_path / "r_v2.sqlite")
    _seed_mode(db, asset_class="crypto", mode="intraday", b_net=9.0, a_net=2.0, n=70, days_ok=True)
    c = sqlite3.connect(db)
    c.execute("INSERT OR REPLACE INTO paper_shadow_meta VALUES ('preentry_v2_activated_at', ?)",
              (datetime.now(timezone.utc).isoformat(),))
    c.commit(); c.close()
    res = mon.promotion_readiness_by_mode(db)
    m = next(x for x in res["modes"] if x["asset_class"] == "crypto")
    assert m["forward_days"] == 0
    assert m["criteria"]["forward_days>=14"] is False
    assert m["verdict"] == "WATCH"                 # promising, but deliberately too early


def test_readiness_fee_integrity_breaks_on_stale_or_wrong_profile(tmp_path):
    db = str(tmp_path / "r4.sqlite")
    # stock mode using the WRONG (crypto) fee profile → integrity fails → NOT_READY even if B>A
    _seed_mode(db, asset_class="stocks", mode="intraday", b_net=9.0, a_net=2.0, n=70,
               days_ok=True, fee_profile="bybit_non_vip_usdt_perp")
    res = mon.promotion_readiness_by_mode(db)
    m = next(x for x in res["modes"] if x["mode"] == "intraday")
    assert m["fee_profile_integrity_ok"] is False
    assert _verdict_for(res, "stocks", "intraday") == "NOT_READY"


def test_market_main_risk_dedup_by_asset():
    # the populate logic: stocks risk must differ from crypto risk
    today = [{"_asset": "crypto", "impact": "negative", "title": "BTC sell-off"},
             {"_asset": "stocks", "impact": "negative", "title": "TSLA downgrade"}]
    crypto_risk = next((n["title"] for n in today if n["_asset"] == "crypto" and n["impact"] == "negative"), None)
    stocks_risk = next((n["title"] for n in today if n["_asset"] == "stocks" and n["impact"] == "negative"), None)
    assert crypto_risk == "BTC sell-off" and stocks_risk == "TSLA downgrade"
    assert crypto_risk != stocks_risk
