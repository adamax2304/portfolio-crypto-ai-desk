"""Read-only mode viability audit. Builds deduped per-signal dataset and emits
slice statistics across windows, modes, conditions. No code paths touched, no
state mutated. Output is plain text to stdout for capture into markdown reports.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "crypto_ai_desk.sqlite")

# Anchor "now" — newest checked_at in DB so windows are stable for replay.
def latest_now(db: sqlite3.Connection) -> str:
    return db.execute("SELECT MAX(checked_at) FROM signal_outcomes").fetchone()[0]


def iso_minus_hours(now_iso: str, hours: float) -> str:
    """Lightweight ISO-arithmetic via datetime."""
    from datetime import datetime, timedelta, timezone
    s = now_iso.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return (dt - timedelta(hours=hours)).isoformat()


@dataclass
class Signal:
    signal_id: str
    asset_class: str
    symbol: str
    mode: str
    tier: str
    direction: str
    score: float
    created_at: str
    market_regime: str
    news_supported: int
    telegram_supported: int
    derivatives_supported: int
    sector: str
    setup_type: str
    primary_exchange: str
    expires_at: str
    validity_window_hours: float
    entry_low: float
    entry_high: float
    stop_loss: float
    invalidation: float
    tp1: float
    tp2: float
    expected_rr_tp1: float
    expected_rr_tp2: float
    final_outcome: str | None
    final_r: float | None
    entry_triggered: int | None
    entry_triggered_at: str | None
    stop_hit: int | None
    tp1_hit: int | None
    tp2_hit: int | None
    mfe_r: float | None
    mae_r: float | None
    status: str


def load_deduped(db: sqlite3.Connection, since: str | None = None) -> list[Signal]:
    """One row per signal_id with latest outcome attached."""
    where = ""
    args: tuple = ()
    if since:
        where = "WHERE ps.created_at >= ?"
        args = (since,)
    q = f"""
        SELECT ps.signal_id, ps.asset_class, ps.symbol, ps.mode, ps.tier,
               ps.direction, ps.score, ps.created_at,
               COALESCE(ps.market_regime,'') as market_regime,
               COALESCE(ps.news_supported,0) as news_supported,
               COALESCE(ps.telegram_supported,0) as telegram_supported,
               COALESCE(ps.derivatives_supported,0) as derivatives_supported,
               COALESCE(ps.sector,'') as sector,
               COALESCE(ps.setup_type,'') as setup_type,
               COALESCE(ps.primary_exchange,'') as primary_exchange,
               COALESCE(ps.expires_at,'') as expires_at,
               COALESCE(ps.validity_window_hours,0) as validity_window_hours,
               COALESCE(ps.entry_low,0), COALESCE(ps.entry_high,0),
               COALESCE(ps.stop_loss,0), COALESCE(ps.invalidation,0),
               COALESCE(ps.tp1,0), COALESCE(ps.tp2,0),
               COALESCE(ps.expected_rr_tp1,0), COALESCE(ps.expected_rr_tp2,0),
               so.final_outcome, so.final_r, so.entry_triggered, so.entry_triggered_at,
               so.stop_hit, so.tp1_hit, so.tp2_hit,
               so.max_favorable_excursion_r, so.max_adverse_excursion_r,
               ps.status
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id = ps.signal_id)
        {where}
        ORDER BY ps.created_at DESC
    """
    rows = db.execute(q, args).fetchall()
    out: list[Signal] = []
    for r in rows:
        out.append(Signal(
            signal_id=r[0], asset_class=r[1], symbol=r[2], mode=r[3], tier=r[4],
            direction=r[5], score=r[6] or 0, created_at=r[7],
            market_regime=r[8], news_supported=r[9], telegram_supported=r[10],
            derivatives_supported=r[11], sector=r[12], setup_type=r[13],
            primary_exchange=r[14], expires_at=r[15], validity_window_hours=r[16],
            entry_low=r[17], entry_high=r[18], stop_loss=r[19], invalidation=r[20],
            tp1=r[21], tp2=r[22], expected_rr_tp1=r[23], expected_rr_tp2=r[24],
            final_outcome=r[25], final_r=r[26], entry_triggered=r[27],
            entry_triggered_at=r[28], stop_hit=r[29], tp1_hit=r[30], tp2_hit=r[31],
            mfe_r=r[32], mae_r=r[33], status=r[34],
        ))
    return out


def stats(rows: list[Signal]) -> dict[str, Any]:
    wins = [r for r in rows if r.final_outcome == "win"]
    losses = [r for r in rows if r.final_outcome == "loss"]
    expired = [r for r in rows if r.final_outcome == "expired"]
    not_tr = [r for r in rows if r.final_outcome == "not_triggered"]
    pending = [r for r in rows if r.final_outcome is None]
    closed = wins + losses
    net_r = sum((r.final_r or 0) for r in closed)
    win_r = sum((r.final_r or 0) for r in wins)
    loss_r = abs(sum((r.final_r or 0) for r in losses)) or 1e-9
    return {
        "n": len(rows), "W": len(wins), "L": len(losses),
        "expired": len(expired), "not_triggered": len(not_tr), "pending": len(pending),
        "closed": len(closed),
        "WR": (len(wins) / len(closed) * 100) if closed else 0.0,
        "netR": net_r, "PF": (win_r / loss_r) if losses else (float("inf") if wins else 0.0),
    }


def fmt(s: dict[str, Any]) -> str:
    return (f"n={s['n']:<4} W={s['W']:<3} L={s['L']:<3} closed={s['closed']:<3} "
            f"WR={s['WR']:>5.1f}% PF={s['PF']:>5.2f} netR={s['netR']:+.1f} "
            f"exp={s['expired']} nt={s['not_triggered']} pend={s['pending']}")


def slice_by(rows: list[Signal], key) -> list[tuple[Any, dict]]:
    buckets: dict[Any, list[Signal]] = defaultdict(list)
    for r in rows:
        buckets[key(r)].append(r)
    return sorted(
        ((k, stats(v)) for k, v in buckets.items()),
        key=lambda x: (-x[1]["closed"], x[0] if x[0] is not None else "")
    )


def main() -> None:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    now = latest_now(db)
    print(f"# ANCHOR_NOW = {now}")
    h48 = iso_minus_hours(now, 48)
    h7d = iso_minus_hours(now, 24 * 7)
    h14d = iso_minus_hours(now, 24 * 14)
    print(f"# 48h cutoff = {h48}")
    print(f"# 7d  cutoff = {h7d}")
    print(f"# 14d cutoff = {h14d}")

    # Major fix dates derived from reports/memory:
    fix_p1_stocks = "2026-06-05T19:00:00+00:00"   # swing pause + telegram 400
    fix_parallel = "2026-06-07T22:34:00+00:00"    # parallel fetch deployed

    full = load_deduped(db)
    print(f"# Total deduped signals: {len(full)}")
    print(f"# Date range: {min(r.created_at for r in full)} -> {max(r.created_at for r in full)}")

    windows = [("48h", h48), ("7d", h7d), ("14d", h14d), ("ALL", None)]

    print("\n" + "=" * 78)
    print("SECTION A — Overall by window (A/B only, deduped)")
    print("=" * 78)
    for wname, cutoff in windows:
        sub = [r for r in full if r.tier in ("A", "B") and (cutoff is None or r.created_at >= cutoff)]
        print(f"\n[{wname}] A/B all: {fmt(stats(sub))}")
        for ac in ("crypto", "stocks"):
            sub_ac = [r for r in sub if r.asset_class == ac]
            print(f"  {ac:<7} {fmt(stats(sub_ac))}")

    print("\n" + "=" * 78)
    print("SECTION B — Mode breakdown per window (A/B)")
    print("=" * 78)
    for wname, cutoff in windows:
        print(f"\n--- {wname} ---")
        sub = [r for r in full if r.tier in ("A", "B") and (cutoff is None or r.created_at >= cutoff)]
        for ac in ("crypto", "stocks"):
            print(f"  {ac}:")
            for mode in ("scalp", "intraday", "swing", "invest"):
                sub_m = [r for r in sub if r.asset_class == ac and r.mode == mode]
                if sub_m:
                    print(f"    {mode:<9} {fmt(stats(sub_m))}")

    print("\n" + "=" * 78)
    print("SECTION C — Crypto A/B 14d slices: direction, news, regime, tier")
    print("=" * 78)
    crypto_14d_ab = [r for r in full if r.asset_class == "crypto" and r.tier in ("A","B") and r.created_at >= h14d]
    print(f"\nCrypto A/B 14d total: {fmt(stats(crypto_14d_ab))}")
    print("\nBy direction:")
    for k, s in slice_by(crypto_14d_ab, lambda r: r.direction):
        print(f"  {k:<10} {fmt(s)}")
    print("\nBy news_supported:")
    for k, s in slice_by(crypto_14d_ab, lambda r: f"news={r.news_supported}"):
        print(f"  {k:<10} {fmt(s)}")
    print("\nBy market_regime (raw label):")
    for k, s in slice_by(crypto_14d_ab, lambda r: r.market_regime or "(empty)"):
        print(f"  {k:<22} {fmt(s)}")
    print("\nBy tier:")
    for k, s in slice_by(crypto_14d_ab, lambda r: r.tier):
        print(f"  {k:<3} {fmt(s)}")
    print("\nMode x news_supported (A/B 14d):")
    for mode in ("scalp", "intraday", "swing"):
        for ns in (1, 0):
            sub = [r for r in crypto_14d_ab if r.mode == mode and r.news_supported == ns]
            if sub:
                print(f"  {mode:<9} news={ns}: {fmt(stats(sub))}")

    print("\n" + "=" * 78)
    print("SECTION D — Crypto scalp deep dive (A/B 14d)")
    print("=" * 78)
    scalp = [r for r in crypto_14d_ab if r.mode == "scalp"]
    print(f"\nScalp 14d total: {fmt(stats(scalp))}")
    print("\nBy direction:")
    for k, s in slice_by(scalp, lambda r: r.direction):
        print(f"  {k:<6} {fmt(s)}")
    print("\nBy news_supported:")
    for k, s in slice_by(scalp, lambda r: f"news={r.news_supported}"):
        print(f"  {k:<8} {fmt(s)}")
    print("\nBy regime:")
    for k, s in slice_by(scalp, lambda r: r.market_regime or "(empty)"):
        print(f"  {k:<22} {fmt(s)}")
    print("\nBy entry triggered/not:")
    triggered_scalp = [r for r in scalp if r.entry_triggered == 1]
    not_tr_scalp = [r for r in scalp if r.entry_triggered != 1]
    print(f"  triggered={len(triggered_scalp)}: {fmt(stats(triggered_scalp))}")
    print(f"  not_triggered={len(not_tr_scalp)}: {fmt(stats(not_tr_scalp))}")
    print("\nExpired scalp — MFE distribution:")
    expired_scalp = [r for r in scalp if r.final_outcome == "expired"]
    pos_mfe = [r for r in expired_scalp if (r.mfe_r or 0) > 0]
    mfe_05R = [r for r in expired_scalp if (r.mfe_r or 0) >= 0.5]
    mfe_07R = [r for r in expired_scalp if (r.mfe_r or 0) >= 0.7]
    print(f"  total expired: {len(expired_scalp)}")
    print(f"  positive MFE: {len(pos_mfe)} ({len(pos_mfe)/max(len(expired_scalp),1)*100:.0f}%)")
    print(f"  MFE >= 0.5R: {len(mfe_05R)}")
    print(f"  MFE >= 0.7R: {len(mfe_07R)}")
    print(f"  avg MFE among expired: {sum((r.mfe_r or 0) for r in expired_scalp)/max(len(expired_scalp),1):.2f}R")
    print(f"  avg MAE among expired: {sum((r.mae_r or 0) for r in expired_scalp)/max(len(expired_scalp),1):.2f}R")
    print("\nLosses MAE/MFE:")
    losses_scalp = [r for r in scalp if r.final_outcome == "loss"]
    if losses_scalp:
        avg_mfe = sum((r.mfe_r or 0) for r in losses_scalp) / len(losses_scalp)
        avg_mae = sum((r.mae_r or 0) for r in losses_scalp) / len(losses_scalp)
        print(f"  n={len(losses_scalp)}, avg MFE before stop: {avg_mfe:.2f}R, avg MAE: {avg_mae:.2f}R")
    print("\nWins MFE (would trailing have given more?):")
    wins_scalp = [r for r in scalp if r.final_outcome == "win"]
    if wins_scalp:
        avg_mfe = sum((r.mfe_r or 0) for r in wins_scalp) / len(wins_scalp)
        print(f"  n={len(wins_scalp)}, avg MFE: {avg_mfe:.2f}R, avg final_r: {sum(r.final_r or 0 for r in wins_scalp)/len(wins_scalp):.2f}R")

    # Liquidity proxy: primary_exchange + symbol (BTC/ETH/SOL = liquid major)
    liquid_majors = {"BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"}
    print("\nBy liquidity tier:")
    for k, s in [
        ("liquid_major", [r for r in scalp if r.symbol in liquid_majors]),
        ("other_liquid", [r for r in scalp if r.symbol not in liquid_majors and r.primary_exchange == "binance"]),
        ("alt_thin",     [r for r in scalp if r.primary_exchange != "binance"]),
    ]:
        if k:
            print(f"  {k:<14} {fmt(stats(s))}")

    print("\n" + "=" * 78)
    print("SECTION E — Stocks A/B slices (14d)")
    print("=" * 78)
    stocks_14d_ab = [r for r in full if r.asset_class == "stocks" and r.tier in ("A","B") and r.created_at >= h14d]
    print(f"\nStocks A/B 14d: {fmt(stats(stocks_14d_ab))}")
    print("\nBy mode:")
    for k, s in slice_by(stocks_14d_ab, lambda r: r.mode):
        print(f"  {k:<9} {fmt(s)}")
    print("\nBy tier:")
    for k, s in slice_by(stocks_14d_ab, lambda r: r.tier):
        print(f"  {k:<3} {fmt(s)}")
    ETFS = {"SPY","QQQ","DIA","IWM","XLK","XLV","XLY","XLE","XLF","XLI","XLP","XLU","XLB","XLRE","SMH","XLC","XBI","XOP"}
    print("\nETF vs single-name:")
    for k, s in [
        ("ETF", [r for r in stocks_14d_ab if r.symbol in ETFS]),
        ("single-name", [r for r in stocks_14d_ab if r.symbol not in ETFS]),
    ]:
        print(f"  {k:<12} {fmt(stats(s))}")
    print("\nBy sector:")
    for k, s in slice_by(stocks_14d_ab, lambda r: r.sector or "(none)")[:20]:
        print(f"  {k:<22} {fmt(s)}")
    print("\nBy direction:")
    for k, s in slice_by(stocks_14d_ab, lambda r: r.direction):
        print(f"  {k:<7} {fmt(s)}")

    print("\n" + "=" * 78)
    print("SECTION F — Pre-fix vs Post-fix (stocks swing pause = 2026-06-05T19:00)")
    print("=" * 78)
    s_swing = [r for r in full if r.asset_class == "stocks" and r.mode == "swing"]
    pre_pause = [r for r in s_swing if r.created_at < fix_p1_stocks]
    post_pause = [r for r in s_swing if r.created_at >= fix_p1_stocks]
    print(f"\nStocks swing PRE-pause (any tier): {fmt(stats(pre_pause))}")
    pre_ab = [r for r in pre_pause if r.tier in ("A","B")]
    print(f"  PRE pause A/B only: {fmt(stats(pre_ab))}")
    print(f"\nStocks swing POST-pause (any tier): {fmt(stats(post_pause))}")
    post_ab = [r for r in post_pause if r.tier in ("A","B")]
    post_c = [r for r in post_pause if r.tier == "C"]
    print(f"  POST pause A/B (LEAK CHECK): {fmt(stats(post_ab))}")
    print(f"  POST pause C-tier (counterfactual): {fmt(stats(post_c))}")

    print("\n" + "=" * 78)
    print("SECTION G — Stocks invest mode deep dive (14d)")
    print("=" * 78)
    invest = [r for r in full if r.asset_class == "stocks" and r.mode == "invest" and r.created_at >= h14d]
    print(f"\nStocks invest A/B/C 14d: {fmt(stats(invest))}")
    print("\nBy tier:")
    for k, s in slice_by(invest, lambda r: r.tier):
        print(f"  {k:<3} {fmt(s)}")
    print("\nBy direction:")
    for k, s in slice_by(invest, lambda r: r.direction):
        print(f"  {k:<6} {fmt(s)}")
    print("\nETF vs single-name:")
    print(f"  ETF: {fmt(stats([r for r in invest if r.symbol in ETFS]))}")
    print(f"  single-name: {fmt(stats([r for r in invest if r.symbol not in ETFS]))}")
    print("\nValidity window (hours):")
    iw = Counter(round(r.validity_window_hours, 0) for r in invest)
    for k, v in sorted(iw.items()):
        print(f"  validity_window={k}h: n={v}")
    # check actual hold durations (entry_triggered_at -> last check)
    print("\nHold-time analysis (entry_triggered_at -> latest signal_outcomes.checked_at):")
    held = [r for r in invest if r.entry_triggered_at]
    if held:
        # Compute hours between trigger and checked
        from datetime import datetime
        durations = []
        for r in held:
            try:
                t0 = datetime.fromisoformat(r.entry_triggered_at.replace("Z","+00:00"))
                # checked_at would equal latest outcome row; we don't have it on Signal but
                # for invest signals, the latest check approximates "now" or expiry
                if r.expires_at:
                    t1 = datetime.fromisoformat(r.expires_at.replace("Z","+00:00"))
                    durations.append((t1 - t0).total_seconds() / 3600)
            except Exception:
                pass
        if durations:
            print(f"  trigger->expiry hours: n={len(durations)}, avg={sum(durations)/len(durations):.1f}h, "
                  f"min={min(durations):.1f}h, max={max(durations):.1f}h")
    print("\nInvest individual signals (latest 20):")
    for r in invest[:20]:
        print(f"  {r.created_at[:16]} {r.symbol:<6} {r.tier} sc{r.score:>4.0f} {r.direction:<6} "
              f"news={r.news_supported} -> {r.final_outcome or 'pending':<14} R={r.final_r if r.final_r is not None else '?'} "
              f"valid_h={r.validity_window_hours:.0f}")

    print("\n" + "=" * 78)
    print("SECTION H — Stocks intraday detail (post-pause window)")
    print("=" * 78)
    si = [r for r in full if r.asset_class == "stocks" and r.mode == "intraday"
          and r.created_at >= fix_p1_stocks and r.tier in ("A","B")]
    print(f"\nStocks intraday A/B since pause-date: {fmt(stats(si))}")
    print("\nBy direction:")
    for k, s in slice_by(si, lambda r: r.direction):
        print(f"  {k:<6} {fmt(s)}")
    print("\nBy tier:")
    for k, s in slice_by(si, lambda r: r.tier):
        print(f"  {k:<3} {fmt(s)}")
    print("\nBy symbol (top 12 by closed):")
    sym_stats = slice_by(si, lambda r: f"{r.symbol}|{r.direction}")
    for k, s in sym_stats[:15]:
        print(f"  {k:<14} {fmt(s)}")
    print("\nFor NVDA + SMCI longs specifically:")
    for sym in ("NVDA", "SMCI"):
        sub = [r for r in si if r.symbol == sym and r.direction == "long"]
        if sub:
            print(f"  {sym} long: {fmt(stats(sub))}")
        else:
            print(f"  {sym} long: no post-pause data")

    print("\n" + "=" * 78)
    print("SECTION I — Routing simulation: crypto scalp variants (A/B 14d)")
    print("=" * 78)
    scalp_all = [r for r in full if r.asset_class == "crypto" and r.mode == "scalp"
                 and r.tier in ("A","B") and r.created_at >= h14d]
    print(f"\nBaseline (A: keep): {fmt(stats(scalp_all))}")
    v_news = [r for r in scalp_all if r.news_supported == 1]
    v_trend = [r for r in scalp_all if "trend" in (r.market_regime or "").lower()
               and "danger" not in (r.market_regime or "").lower()]
    v_liquid = [r for r in scalp_all if r.symbol in liquid_majors
                or r.primary_exchange == "binance"]
    v_combo = [r for r in scalp_all if (
        r.news_supported == 1
        or "trend" in (r.market_regime or "").lower() and "danger" not in (r.market_regime or "").lower()
        or r.symbol in liquid_majors
    )]
    v_watchlist = []   # simulated: zero actionable
    print(f"\nVariant B — news/catalyst only:        {fmt(stats(v_news))}")
    print(f"Variant C — clean trend regime only:     {fmt(stats(v_trend))}")
    print(f"Variant D — liquid only (binance/major): {fmt(stats(v_liquid))}")
    print(f"Variant E — news OR trend OR liquid:     {fmt(stats(v_combo))}")
    print(f"Variant F — watchlist-only:              n=0 (all suppressed)")
    print("\nRemoved/Retained vs baseline:")
    base_s = stats(scalp_all)
    for label, sub in [
        ("B", v_news), ("C", v_trend), ("D", v_liquid), ("E", v_combo)
    ]:
        removed = base_s["n"] - len(sub)
        rem_wins = base_s["W"] - stats(sub)["W"]
        rem_loss = base_s["L"] - stats(sub)["L"]
        rem_r = base_s["netR"] - stats(sub)["netR"]
        print(f"  Variant {label}: removed n={removed} (W={rem_wins} L={rem_loss}) "
              f"removed_netR={rem_r:+.1f} -> kept_netR={stats(sub)['netR']:+.1f}")

    print("\n" + "=" * 78)
    print("SECTION J — Routing simulation: stocks invest variants (14d, all tiers)")
    print("=" * 78)
    inv_all = [r for r in full if r.asset_class == "stocks" and r.mode == "invest"
               and r.tier in ("A","B") and r.created_at >= h14d]
    print(f"\nBaseline (A: keep): {fmt(stats(inv_all))}")
    inv_news = [r for r in inv_all if r.news_supported == 1]
    inv_etf = [r for r in inv_all if r.symbol in ETFS]
    inv_single = [r for r in inv_all if r.symbol not in ETFS]
    inv_b = [r for r in inv_all if r.tier == "B"]
    print(f"\nVariant B — watchlist only:              n=0 (all suppressed)")
    print(f"Variant C — longer expiry sim:           {fmt(stats(inv_all))} (held = same set, "
          f"closure horizon would change outcome; cannot simulate cleanly without re-running tracker)")
    print(f"Variant D — news/earnings-supported:     {fmt(stats(inv_news))}")
    print(f"Variant E1 — ETF only:                    {fmt(stats(inv_etf))}")
    print(f"Variant E2 — single-name only:            {fmt(stats(inv_single))}")
    print(f"Variant F — B-tier only:                  {fmt(stats(inv_b))}")

    print("\n" + "=" * 78)
    print("SECTION K — Catalyst vs no-catalyst (crypto, all modes, 14d)")
    print("=" * 78)
    crypto_14d = [r for r in full if r.asset_class == "crypto" and r.tier in ("A","B") and r.created_at >= h14d]
    for mode in ("scalp","intraday","swing"):
        sub = [r for r in crypto_14d if r.mode == mode]
        n_cat = [r for r in sub if r.news_supported == 1]
        n_no = [r for r in sub if r.news_supported == 0]
        print(f"\n{mode}:")
        print(f"  catalyst:    {fmt(stats(n_cat))}")
        print(f"  no catalyst: {fmt(stats(n_no))}")

    db.close()


if __name__ == "__main__":
    main()
