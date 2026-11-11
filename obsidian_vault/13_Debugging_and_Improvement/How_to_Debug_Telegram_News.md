# How to Debug Telegram News

When Telegram-derived signals look wrong, follow this trail.

## Step 1 — Is the bridge available?

```python
from src.data_collectors.news_trader_bridge import NewsTraderBridge
b = NewsTraderBridge()
print(b.available, b.state_path, b.telemetry_path())
```

If `available = False`, the path is wrong or news_trader hasn't started. The default path is:

```
C:\Users\adama\Documents\zeph ai projects\news_trader\news_trader\state
```

To override, pass `state_path` to `NewsTraderBridge(...)`.

## Step 2 — Are signals coming in?

```python
pulse = b.macro_pulse(lookback_minutes=240)
print(pulse)
```

You should see `signal_count > 0`, top_sources populated. If `signal_count = 0`, news_trader is not writing to telemetry.

## Step 3 — Per-ticker view

```python
agg = b.aggregate(lookback_minutes=240, tickers_of_interest=["BTC", "ETH", "SOL"])
for ticker, att in agg.items():
    print(ticker, att.attention_score, att.net_sentiment, att.strong_tier_count, att.sources)
```

## Step 4 — Bridge snapshot file

`data/processed/news_trader_bridge_latest.json` is written each daily/intraday report. Compare to the live bridge call to see if the snapshot is fresh.

## Step 5 — Conversion to manual_social_notes

`bridge.to_manual_social_notes(agg)` produces the shape `CrowdAttentionAgent` expects. Inspect for:

- `verification: confirmed` only when a `tier=strong` signal was in the cluster.
- `sentiment` derived from net_sentiment.
- `confidence: high` only with strong tier.

## Step 6 — CrowdAttentionAgent input

The merged manual_social list goes into `CrowdAttentionAgent.run`. The output (`data/processed/agent_outputs/<latest>_crowd_attention_agent.json`) should reflect the headlines you saw.

## Step 7 — Score impact

Telegram does NOT directly feed scoring. To see indirect impact:

- Compare `attention_score` and `stage` per symbol between two runs (with and without bridge data).
- Compare warnings on rejected ideas (rumor-driven stage emits warnings).

## Common issues

- **Bridge unavailable** → wrong path; fix `state_path`.
- **Stale signals** → news_trader process is dead; restart it (out of scope here).
- **Wrong tickers** → cashtag regex in `_tickers_from_signal` may miss the symbol. Add to `CATEGORY_TICKER_MAP` or extend regex.
- **Missing sentiment** → headlines don't match `SENTIMENT_KEYWORDS`. Add new keywords.
- **Wrong verification** — verify `tier == "strong"` is present in news_trader's classifier for the cluster.

## Critical

**Never write to the news_trader directory.** The bridge is strictly read-only.

## Related

- [[Telegram_Integration]]
- [[Telegram_Message_Parsing]]
- [[Crowd_Attention_Agent]]

## Implemented status

- **Diagnostic guide**.
