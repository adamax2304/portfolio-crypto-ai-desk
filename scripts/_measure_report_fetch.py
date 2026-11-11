"""READ-ONLY diagnostic: measure crypto report FETCH stages in isolation.

Times rank_candidates + update_data (the network-heavy stages) with stage_timer
so per-source latencies land in logs/diagnostics/. Does NOT run daily_report →
NO signal registration, NO Telegram, NO report file. Safe to run between cycles.

Bounded by --cap to avoid overrunning into the next scheduler cycle.
"""
from __future__ import annotations
import sys, time
from src.cli import build_supervisor
from src.diagnostics import stage_timer as t
from src.data_collectors.multi_exchange_universe_collector import MultiExchangeUniverseCollector

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 20
MODE = sys.argv[2] if len(sys.argv) > 2 else "scalp"

sup = build_supervisor()
t.set_report(f"measure-{MODE}")
t.mark(f"==== MEASURE fetch path mode={MODE} cap={CAP} ====")

wall0 = time.monotonic()
# 1) universe ranking (broad HTTP)
with t.stage("rank_candidates", exchanges=len(sup.config.enabled_exchanges)):
    rows = MultiExchangeUniverseCollector(sup.config, sup.file_store).rank_candidates(
        mode=MODE, refresh=True
    )
selected = sup._selected_ranked_symbols(rows) or sup.config.symbols
selected = selected[:CAP]
tfs = sup._mode_timeframes(MODE)
print(f"ranked={len(rows)} selected(capped)={len(selected)} tfs={tfs}")

# 2) the full sequential fetch path (OHLCV x3 exchanges + derivs x3 + news + social)
with t.stage("update_data", symbols=len(selected), tfs=len(tfs or [])):
    sup.update_data(symbols=selected, timeframes=tfs)

total = time.monotonic() - wall0
t.mark(f"==== MEASURE total={total:.1f}s symbols={len(selected)} ====")
print(f"TOTAL fetch wall={total:.1f}s for {len(selected)} symbols")
