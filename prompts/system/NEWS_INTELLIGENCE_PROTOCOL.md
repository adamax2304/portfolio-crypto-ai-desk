# News Intelligence Protocol

How to treat news + Telegram data. The single biggest source of false confidence in crypto.

---

## Sources the desk uses

1. **RSS news** (`src/data_collectors/rss_news_collector.py`)
   - Binance Announcements (`primary_source: true`)
   - CoinDesk, Cointelegraph, Decrypt (secondary)
   - Coinbase Blog (disabled — Cloudflare 403)
2. **Manual events** (`data/raw/events/manual_events.yaml`) — operator-curated.
3. **Manual social notes** (`data/manual/social_notes.yaml`, `data/manual/narrative_notes.yaml`).
4. **`news_trader_bridge`** (read-only) — tails `news_trader/news_trader/state/telemetry.jsonl` for pre-classified Telegram signals.

## Channel hierarchy (verification)

```
unverified rumor
  → unverified manual note
    → single-source RSS / Telegram
      → multiple sources (RSS + Telegram + manual)
        → primary source (exchange / project)
          → primary source + market confirmation (price + volume + OI)
```

Each step up unlocks more headroom. The desk caps unverified rumor-only catalysts at score 55.

## Classification taxonomy

Every notable item must be classified into exactly one bucket:

| Class | Definition |
|---|---|
| `Useful_News` | Created or confirmed a tradable setup |
| `Useless_News` | No measurable price reaction within 60 min |
| `Fake_or_Unverified_News` | No primary confirmation within 24h, or contradicted later |
| `Telegram_News` | Default landing for any Telegram item before classification |
| `Market_Moving_News` | ≥ 2% move within 60 min OR ≥ 5% within 24h, regardless of trade outcome |
| `Late_Or_Priced_In` | Verified but arrived after the move |
| `Watch_Only` | Interesting but not actionable today |

Folders under `obsidian_vault/12_News_Intelligence_Journal/`.

## Per-item evaluation checklist

When asked to evaluate a news item, run these gates in order:

1. **Source**
   - Type (Telegram channel / RSS / project blog / exchange page / operator note)
   - Reputation (primary / secondary / unknown)
   - News-trader tier (`strong` / `medium` / missing)
2. **Timestamp**
   - Fresh (< 30 min) / recent (30–120 min) / stale (> 120 min).
3. **Symbols + narrative**
   - Detected tickers; matching narrative from `config/watchlist.yaml.narratives`.
4. **Verification**
   - Primary source URL?
   - Multiple corroborating sources?
   - Single-source?
   - Rumor flag?
5. **Sentiment**
   - Bullish / bearish / macro_riskoff / macro_riskon (per `SENTIMENT_KEYWORDS`).
6. **Market reaction**
   - Price reaction at 5m / 15m / 1h / 4h.
   - Volume_ratio on news bars.
   - OI / funding shift.
   - Cross-exchange agreement.
7. **Trade relevance**
   - Created a new setup? Confirmed existing? Invalidated existing? Pure noise?
8. **Classification** per the taxonomy above.

## How news affects scoring

- **`catalyst_news` component** receives input from `CatalystAgent`. Higher when verified manual_event + news_mention present.
- **`narrative` component** is lifted when news mentions cluster on a configured narrative.
- **Telegram via `news_trader_bridge`** enters only through `CrowdAttentionAgent` — affects **attention staging**, never `catalyst_news` directly.
- **Rumor cap (55)** fires when any catalyst string contains "rumor" + verification ∈ {none, rumor, single_source} + no risk_events.

## Telegram-specific discipline

- Telegram message alone is **never a trade**.
- A `tier=strong` news_trader cluster maps to `verification = confirmed` for attention purposes only.
- A single-source Telegram message → attention only.
- A rumor-tagged manual note + attention ≥ 15 → `stage = rumor_driven` + 55 cap.
- Telegram hype + extreme funding + extended price = **euphoria / crowding warning**, not a buy signal.
- "Insider says X" / "reportedly" / "could be" → treat as rumor automatically.

## Useful vs useless heuristic

```
Useful if:
  appeared at or before the move
  + had market confirmation (price + volume)
  + helped identify a real setup
  + verification was primary or multi-source

Useless if:
  arrived after the move
  + no measurable price/volume reaction
  + generic re-post of older news
  + single-source with no follow-through
```

## Source reliability tracking

The desk does **not yet** weight by source reliability. Until that ships:

- Track manually in weekly `News_Reviews/YYYY-Www_Source_Reliability_Review.md`.
- For each source: count of items, market-moving %, useless %, fake %.
- Top 5 trustworthy sources → up-weight mentally.
- Bottom 5 → mute mentally.

Recommended improvement: per-source reliability map in `news_trader_bridge` config (see `Improvement_Backlog`).

## Confirmed catalyst promotion

When a Telegram rumor is later confirmed by a primary source:

1. Add an entry to `data/raw/events/manual_events.yaml`:
   ```yaml
   - date: 2026-05-23
     ticker: SOL
     event: "<short>"
     type: listing       # or partnership / mainnet / etc.
     source: "<primary URL>"
     importance: 3
   ```
2. Re-run `python -m src.cli update-data` to load it.
3. The next report applies `verification_status = manual_event` for that symbol.

This is the only way Telegram leads to `catalyst_news` lift.

## Filing actions

After classification, file the item:

- `obsidian_vault/12_News_Intelligence_Journal/Telegram_News/` — default landing.
- `Useful_News/` — after confirmed useful.
- `Useless_News/` — after confirmed noise.
- `Fake_or_Unverified_News/` — after exposed as fake or unverified > 24h.
- `Market_Moving_News/` — for the dataset (even if you didn't trade).

Use the matching template from `Templates/`.

## Anti-patterns

- Treating a Telegram channel as primary.
- Trading on "insider" rumors without primary confirmation.
- Sizing larger because "everyone is talking about it".
- Logging every Telegram message — only log items that affected the desk or a trade.
- Treating exchange-listing tweets as automatic catalysts — wait for the official page.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
- [[OBSIDIAN_MEMORY_PROTOCOL]]
- [[RISK_AND_SCORING_PROTOCOL]]
