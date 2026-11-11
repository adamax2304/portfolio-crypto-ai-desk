# News Source Monitor Implementation

Date: 2026-07-13

## Scope

This pass changes only news ingest observability and enrichment. It does not
change strategy rules, scoring weights, paper PnL, signal outcomes, final_r,
actionability, or live state.

## Implemented

- RSS descriptions and Telegram message bodies are stored in `news_items`.
- Ingest timestamps, first-seen timestamps, content fingerprints, Telegram
  message identifiers, and channel categories are stored additively.
- Old `news_items` schemas migrate with additive `ALTER TABLE` operations.
- Exact repeated payloads from one RSS publisher in a batch and from one
  Telegram channel during one process window are suppressed. Different
  publishers remain independent corroboration.
- Macro tags use word boundaries; substrings such as `Warsh`, `awards`, and
  `warnings` no longer create a false `war` event tag.
- RSS requests retry once and record per-source transport status.
- EDGAR records API success/empty/error status.
- Telegram records per-channel resolution, heartbeat, catch-up, and
  disconnect status, plus a whole-listener status.
- A scheduler step `news-health-monitor --send-telegram` runs fail-open after
  current-cycle ingest. It records transition incidents in
  `data/diagnostics/news_source_errors.jsonl` and sends one `[NEWS HEALTH]`
  alert on failure plus one recovery alert. It does not send trade alerts.
- Alert state is persisted in `news_source_alert_state`; repeated cycles do
  not spam the operator.
- The confirmed Reuters 404 endpoint is disabled explicitly rather than left
  as a known-broken active source. Stock coverage remains active through CNBC,
  Yahoo Finance, MarketWatch, Benzinga, Motley Fool, GlobeNewswire, PR
  Newswire, Business Wire, and SEC EDGAR.

## Verification snapshot

- 18/18 enabled RSS endpoints returned HTTP 200 during the live probe.
- 29/29 configured Telegram channels resolved with the active Telethon session.
- EDGAR refresh: 19 filings saved for 28 tickers; 7 universe ETF tickers have
  no CIK mapping and remain an explicit advisory warning.
- Health after refresh: `OK 37`, `STALE 12`, `ERROR 0`, `DEAD 0`.
- `STALE` means the source had no fresh publication in the window; it is not
  treated as a transport incident unless an explicit error/disconnect is
  recorded.
- Targeted regression: 101 tests passed; Python compile sweep passed.

## Operational commands

```text
python -m src.cli news-source-health
python -m src.cli news-health-monitor --no-send-telegram
python -m src.cli news-health-monitor --send-telegram
```

