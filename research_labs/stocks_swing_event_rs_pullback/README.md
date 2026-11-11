# Stock Swing Event RS Pullback V1 Research

Research-only harness for a future Paper strategy. It does not write production
Paper, live, signal, or ledger tables.

Phases:

1. Technical skeleton: price, relative strength, pullback, structural stop.
2. Local real-news window: only canonical events with causal `available_at`.
3. Reconstructed news: optional Finnhub historical pulls with conservative
   simulated availability.
4. Ablation: compare news-required, news-boost, no-news, and blocker-only views.

Run:

```powershell
python .\research_labs\stocks_swing_event_rs_pullback\run_backtest.py --phase all
```
