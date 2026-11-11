"""Diagnostics for the safe-guardrails stage (PARTS 2-6). Reads the audit dataset
CSV (already built read-only) + BTC OHLCV; emits would-pause / would-bind / profit-
protection / revalidation / risk-off counterfactual CSVs + a JSON summary.

DIAGNOSTIC ONLY. Computes "would_*" labels and counterfactual R. Does NOT touch the
trading DB, scoring, TP/SL, thresholds, sector-cap value; does NOT block or force-close.
MFE/MAE-based estimates cannot model intra-trade path order — limitations stated in reports.
"""
from __future__ import annotations
import csv, json, collections
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
DS = OUT / "LAST_3_7D_TRADE_AND_SHADOW_AUDIT_DATASET.csv"
rows = list(csv.DictReader(DS.open(encoding="utf-8")))


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def day_of(ts):
    return (ts or "")[:10]


trig = [r for r in rows if r["entry_triggered_at"]]
closed = [r for r in trig if f(r["result_R"]) is not None]

# ---------- PART 2: circuit-breaker would-pause ----------
# per UTC day x asset_class: realized R, stops, wins; consecutive stops; long streak
cb_rows = []
by_day_asset = collections.defaultdict(list)
for r in closed:
    d = day_of(r["exit_at"] or r["entry_triggered_at"])
    by_day_asset[(d, r["asset_class"])].append(r)
cb_summary = {"days_would_pause_2R": 0, "days_would_pause_3R": 0, "days_3stops": 0,
              "loss_avoided_at_2R": 0.0, "winners_missed_at_2R": 0.0}
for (d, asset), items in sorted(by_day_asset.items()):
    items.sort(key=lambda r: (r["exit_at"] or r["entry_triggered_at"]))
    realized = 0.0
    stops = 0
    consec = 0
    maxconsec = 0
    long_stops = 0
    # P&L after a -2R / -3R breaker (block entries opened after the threshold is crossed)
    after2 = after3 = 0.0
    tripped2 = tripped3 = False
    for r in items:
        R = f(r["result_R"]) or 0
        if tripped2:
            pass  # would be blocked → contributes 0 (counterfactual)
        else:
            after2 += R
        if tripped3:
            pass
        else:
            after3 += R
        realized += R
        if realized <= -2:
            tripped2 = True
        if realized <= -3:
            tripped3 = True
        if R < 0:
            stops += 1
            consec += 1
            maxconsec = max(maxconsec, consec)
            if r["direction"] == "long":
                long_stops += 1
        else:
            consec = 0
    wp2 = realized <= -2
    wp3 = realized <= -3
    s3 = stops >= 3
    cb_rows.append({"day": d, "asset_class": asset, "trades": len(items),
                    "realized_R": round(realized, 1), "stops": stops, "max_consec_stops": maxconsec,
                    "long_stops": long_stops, "would_pause_2R": wp2, "would_pause_3R": wp3,
                    "would_pause_3stops": s3,
                    "R_if_paused_at_2R": round(after2, 1), "R_saved_vs_2R": round(after2 - realized, 1)})
    if wp2:
        cb_summary["days_would_pause_2R"] += 1
    if wp3:
        cb_summary["days_would_pause_3R"] += 1
    if s3:
        cb_summary["days_3stops"] += 1
    cb_summary["loss_avoided_at_2R"] += round(after2 - realized, 1)
with (OUT / "CIRCUIT_BREAKER_WOULD_PAUSE_COUNTERFACTUAL.csv").open("w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(cb_rows[0].keys()))
    w.writeheader(); w.writerows(cb_rows)

# ---------- PART 3: sector-cap would-bind replay ----------
CLUST = {"NVDA": "semis", "AMD": "semis", "SMH": "semis", "MU": "semis", "AVGO": "semis",
         "TSM": "semis", "ARM": "semis", "INTC": "semis", "QQQ": "megacap_tech_idx",
         "XLK": "megacap_tech_idx", "AAPL": "megacap_tech", "MSFT": "megacap_tech",
         "GOOGL": "megacap_tech", "META": "megacap_tech", "AMZN": "megacap_tech",
         "SPY": "broad_idx", "DIA": "broad_idx", "IWM": "broad_idx", "COIN": "crypto_eq",
         "MSTR": "crypto_eq", "MARA": "crypto_eq", "RIOT": "crypto_eq", "TSLA": "ev"}
si = [r for r in rows if r["asset_class"] == "stocks" and r["mode"] == "intraday"]
occ = collections.defaultdict(list)
for r in si:
    base = r["symbol"].split("/")[0].upper()
    occ[(day_of(r["created_at"]), r["direction"], CLUST.get(base, "other:" + base))].append(r)
cap_rows = []
would_bind_groups = live_set = 0
for k, it in sorted(occ.items()):
    n = len(it)
    live = sum(1 for r in it if r["concentration_status"] and r["concentration_status"] != "not_applicable")
    live_set += live
    if n > 2:
        would_bind_groups += 1
    cap_rows.append({"day": k[0], "direction": k[1], "cluster": k[2], "n": n,
                     "would_shadow_cap2": max(0, n - 2), "would_shadow_cap3": max(0, n - 3),
                     "actually_shadowed_live": live,
                     "symbols": ",".join(r["symbol"] for r in it)})
with (OUT / "STOCK_SECTOR_CAP_WOULD_BIND_REPLAY.csv").open("w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(cap_rows[0].keys()))
    w.writeheader(); w.writerows(cap_rows)

# ---------- PART 4: crypto profit-protection (MFE/MAE estimate) ----------
cp = [r for r in closed if r["asset_class"] == "crypto" and r["mode"] in ("intraday", "swing")]
pp_rows = []
agg = {"current": 0.0, "be05": 0.0, "be1": 0.0, "partial1": 0.0,
       "winners_clipped_be1_max": 0, "losers_saved_be1": 0, "n": len(cp)}
for r in cp:
    R = f(r["result_R"]) or 0
    mfe = f(r["mfe_r"]) or 0
    # BE-after-+X: a loser whose MFE reached +X had +X BEFORE the stop (tracking ends at exit)
    # => stop would have been at BE => ~0R. Winners: BE doesn't reduce a trade that reached TP
    # WITHOUT a post-peak dip to BE — but that dip is UNOBSERVABLE from MFE/MAE (limitation).
    be05 = 0.0 if (R < 0 and mfe >= 0.5) else R
    be1 = 0.0 if (R < 0 and mfe >= 1.0) else R
    # partial 50% at +1R then BE on remainder: loser w/ MFE>=1 -> +0.5 ; winner unchanged (already past)
    if R < 0 and mfe >= 1.0:
        part = 0.5
    else:
        part = R
    agg["current"] += R; agg["be05"] += be05; agg["be1"] += be1; agg["partial1"] += part
    if R < 0 and mfe >= 1.0:
        agg["losers_saved_be1"] += 1
    # winners that dipped (unknown) — count winners with final>0 but mae<=-... can't know; flag MFE>=1 winners
    if R > 0 and mfe >= 1.0:
        agg["winners_clipped_be1_max"] += 1  # upper-bound of winners that COULD be clipped
    pp_rows.append({"signal_id": r["signal_id"], "symbol": r["symbol"], "mode": r["mode"],
                    "dir": r["direction"], "regime": r["market_regime"], "result_R": R,
                    "mfe_r": r["mfe_r"], "mae_r": r["mae_r"],
                    "be_after_0.5R_R": be05, "be_after_1R_R": be1, "partial0.5_at_1R_R": part})
for k in ("current", "be05", "be1", "partial1"):
    agg[k] = round(agg[k], 1)
with (OUT / "CRYPTO_PROFIT_PROTECTION_FULL_COUNTERFACTUAL.csv").open("w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(pp_rows[0].keys()))
    w.writeheader(); w.writerows(pp_rows)

# ---------- PART 5: intraday revalidation would-expire ----------
iv = [r for r in trig if r["mode"] == "intraday"]
rev_rows = []
rev = {"crypto_open_gt_12h": 0, "stocks_overnight": 0, "would_expire_crypto_12h_R": 0.0}
for r in iv:
    held = f(r["held_hours"])
    carried = r["overnight_carried"] == "True"
    R = f(r["result_R"]) or 0
    crypto_old = (r["asset_class"] == "crypto" and held is not None and held > 12)
    if crypto_old:
        rev["crypto_open_gt_12h"] += 1
        rev["would_expire_crypto_12h_R"] += R
    if r["asset_class"] == "stocks" and carried:
        rev["stocks_overnight"] += 1
    rev_rows.append({"signal_id": r["signal_id"], "symbol": r["symbol"], "asset_class": r["asset_class"],
                     "dir": r["direction"], "held_hours": r["held_hours"], "overnight_carried": carried,
                     "result_R": R, "final_outcome": r["final_outcome"],
                     "would_expire_crypto_intraday_12h": crypto_old,
                     "carryover_requires_review": carried,
                     "next_day_revalidation_required": carried})
rev["would_expire_crypto_12h_R"] = round(rev["would_expire_crypto_12h_R"], 1)
with (OUT / "INTRADAY_REVALIDATION_COUNTERFACTUAL.csv").open("w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rev_rows[0].keys()))
    w.writeheader(); w.writerows(rev_rows)

# ---------- PART 6: intraday risk-off (BTC daily %) ----------
btc = {}
try:
    import csv as _csv
    for rr in _csv.DictReader((OUT.parent / "data/raw/ohlcv/binance/1d/BTC_USDT.csv").open(encoding="utf-8")):
        tcol = [k for k in rr if k.lower() in ("timestamp", "datetime", "date", "time", "open_time")][0]
        d = str(rr[tcol])[:10]
        o, c = float(rr["open"]), float(rr["close"])
        btc[d] = round((c - o) / o * 100, 2)
except Exception:
    pass
RISK_OFF_DAY_PCT = -0.75  # BTC day <= this => intraday risk-off (diagnostic threshold)
ro_rows = []
ro = {"risk_off_days": [], "losers_caught": 0, "winners_missed": 0,
      "R_on_throttled_longs": 0.0, "by_day": {}}
for r in [x for x in closed if x["asset_class"] == "crypto" and x["direction"] == "long"]:
    d = day_of(r["entry_triggered_at"])
    daypct = btc.get(d)
    risk_off = daypct is not None and daypct <= RISK_OFF_DAY_PCT
    R = f(r["result_R"]) or 0
    if risk_off:
        ro["R_on_throttled_longs"] += R
        if R < 0:
            ro["losers_caught"] += 1
        elif R > 0:
            ro["winners_missed"] += 1
    ro_rows.append({"signal_id": r["signal_id"], "symbol": r["symbol"], "mode": r["mode"],
                    "day": d, "btc_day_pct": daypct, "regime_label": r["market_regime"],
                    "result_R": R, "btc_intraday_risk_off": risk_off,
                    "would_throttle_long": risk_off})
ro["R_on_throttled_longs"] = round(ro["R_on_throttled_longs"], 1)
ro["risk_off_days"] = sorted({day_of(r["entry_triggered_at"]) for r in closed
                              if btc.get(day_of(r["entry_triggered_at"]), 0) <= RISK_OFF_DAY_PCT})
ro["btc_daily_pct"] = btc
with (OUT / "INTRADAY_RISK_OFF_THROTTLE_COUNTERFACTUAL.csv").open("w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=list(ro_rows[0].keys()))
    w.writeheader(); w.writerows(ro_rows)

summary = {"circuit_breaker": cb_summary,
           "cb_worst_days": sorted([r for r in cb_rows if r["stops"] >= 3],
                                   key=lambda r: r["realized_R"])[:8],
           "sector_cap": {"groups": len(cap_rows), "would_bind_cap2_groups": would_bind_groups,
                          "actually_shadowed_live": live_set},
           "profit_protection": agg,
           "intraday_revalidation": rev,
           "risk_off": {k: ro[k] for k in ("risk_off_days", "losers_caught", "winners_missed",
                                           "R_on_throttled_longs", "btc_daily_pct")}}
(OUT / "_safe_guardrails_diag.json").open("w", encoding="utf-8").write(json.dumps(summary, indent=1, default=str))
print(json.dumps(summary, indent=1, default=str))
