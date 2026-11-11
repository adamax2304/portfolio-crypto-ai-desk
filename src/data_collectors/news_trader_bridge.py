"""Read-only bridge to the news_trader project.

news_trader runs a Telethon scraper across 50+ public crypto/macro Telegram
channels (lookonchain, whale_alert, BinanceListings, BWEnews, WalterBloomberg,
zachxbt, ...) and an aggregator that classifies + scores each signal. The
classified signals land in two places under
``news_trader/state/``:

- ``telemetry.jsonl`` — structured event stream (bus_publish, aggregator_emit,
  aggregator_drop, executor_*) with ts_iso + symbol + category + tier + score
  + source + headline.
- ``dedup_seen.json`` — recent raw signal keys for dedup.

This bridge:

1. Tails the telemetry file (last N MB) so we read in seconds even when the
   file is 60 MB.
2. Parses lines into ``NewsTraderSignal`` records.
3. Aggregates by ticker → attention score, sentiment counts, fresh top
   headlines, source list, latest_strong_tier flag.

CRITICAL: this module is strictly read-only. It NEVER writes to the
news_trader directory. Path is resolved through config (so the user can move
news_trader without breaking this bridge), but defaults to the known location.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

from src.logger import get_logger


# Heuristic mapping from news_trader category symbols (BTC, ETH, GOLD, ...)
# to canonical /USDT pairs we trade in crypto-ai-desk.
CATEGORY_TICKER_MAP: dict[str, str] = {
    "GOLD": "PAXG",
    "OIL": "USOON",
    "XAU": "PAXG",
    "WTI": "USOON",
    "BRENT": "USOON",
}


SENTIMENT_KEYWORDS: dict[str, list[str]] = {
    "bullish": [
        "approval", "approved", "etf inflow", "etf launch", "listing", "list",
        "buy", "accumulation", "partnership", "integration", "upgrade", "mainnet",
        "rally", "surge", "soars", "all-time high", "breakout", "moon",
    ],
    "bearish": [
        "hack", "exploit", "rug", "drained", "lawsuit", "ban", "delisting",
        "delist", "dump", "crash", "drops", "tumble", "lawsuit", "sec sues",
        "bankruptcy", "rugpull", "outage", "exit scam",
    ],
    "macro_riskoff": [
        "war", "attack", "strike", "missile", "sanction", "escalat", "rate hike",
        "fed hawkish", "yields surge", "tariff", "recession",
    ],
    "macro_riskon": [
        "rate cut", "dovish", "ceasefire", "agreement signed", "easing",
        "stimulus", "etf inflow",
    ],
}

# Maximum bytes we'll read from the tail of telemetry.jsonl. 5 MB ≈ last hour
# of events even under heavy load. We do not load the full 60 MB stream.
DEFAULT_TAIL_BYTES = 5 * 1024 * 1024


@dataclass
class NewsTraderSignal:
    """A single classified signal from news_trader."""

    ts: datetime
    source: str
    source_name: str
    symbol: str | None
    category: str | None
    tier: str | None
    score: float | None
    direction: str | None
    headline: str
    raw_event: str  # "aggregator_emit" / "bus_publish" / "executor_signal_received"

    @property
    def age_minutes(self) -> float:
        return (datetime.now(timezone.utc) - self.ts).total_seconds() / 60

    @property
    def is_telegram(self) -> bool:
        return (self.source or "").lower() == "telegram" or "t.me/" in (self.source_name or "")


@dataclass
class TickerAttention:
    """Aggregated attention/sentiment per canonical ticker."""

    ticker: str
    mention_count: int = 0
    telegram_mention_count: int = 0
    strong_tier_count: int = 0
    bullish_count: int = 0
    bearish_count: int = 0
    riskoff_count: int = 0
    riskon_count: int = 0
    sources: list[str] = field(default_factory=list)
    top_headlines: list[str] = field(default_factory=list)
    latest_ts: datetime | None = None
    direction_votes: Counter = field(default_factory=Counter)
    categories: Counter = field(default_factory=Counter)

    @property
    def net_sentiment(self) -> str:
        if self.bullish_count > self.bearish_count + 1:
            return "bullish"
        if self.bearish_count > self.bullish_count + 1:
            return "bearish"
        if self.bullish_count == 0 and self.bearish_count == 0:
            return "neutral"
        return "mixed"

    @property
    def attention_score(self) -> float:
        """0..100 attention score combining volume + tg-weight + strong tier."""
        score = 0.0
        score += min(self.mention_count, 12) * 5
        score += min(self.telegram_mention_count, 8) * 4
        score += min(self.strong_tier_count, 4) * 8
        score += min(self.riskoff_count + self.riskon_count, 4) * 3
        return min(round(score, 1), 100.0)

    def age_minutes(self) -> float | None:
        if self.latest_ts is None:
            return None
        return (datetime.now(timezone.utc) - self.latest_ts).total_seconds() / 60


class NewsTraderBridge:
    """Read-only access to news_trader state files.

    Pass the absolute path to ``news_trader/news_trader/state`` (the inner
    state folder). If not provided, falls back to the known default.
    """

    DEFAULT_PATH = Path(r"C:\Users\adama\Documents\zeph ai projects\news_trader\news_trader\state")

    def __init__(
        self,
        state_path: Path | None = None,
        tail_bytes: int = DEFAULT_TAIL_BYTES,
    ):
        self.state_path = Path(state_path) if state_path else self.DEFAULT_PATH
        self.tail_bytes = int(tail_bytes)
        self.logger = get_logger(self.__class__.__name__)

    @property
    def available(self) -> bool:
        return self.state_path.exists() and (self.state_path / "telemetry.jsonl").exists()

    def telemetry_path(self) -> Path:
        return self.state_path / "telemetry.jsonl"

    def tail_lines(self) -> Iterator[str]:
        """Yield JSON lines from the end of telemetry.jsonl.

        Reads at most ``tail_bytes`` bytes from EOF. Skips the (likely
        truncated) first line in that window. UTF-8 with errors=replace so a
        corrupt byte never crashes the bridge.
        """
        path = self.telemetry_path()
        if not path.exists():
            return
        try:
            size = path.stat().st_size
        except OSError:
            return
        with path.open("rb") as handle:
            if size > self.tail_bytes:
                handle.seek(size - self.tail_bytes)
                handle.readline()  # discard partial line
            for raw in handle:
                yield raw.decode("utf-8", errors="replace")

    def iter_signals(self, lookback_minutes: int = 240) -> Iterator[NewsTraderSignal]:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=lookback_minutes)
        # We accept aggregator_emit (classified, scored), and bus_publish on
        # the "enriched" topic. aggregator_drop is noise (rejected by news_trader).
        accepted_events = {"aggregator_emit", "bus_publish", "executor_signal_received"}
        for raw in self.tail_lines():
            raw = raw.strip()
            if not raw or not raw.startswith("{"):
                continue
            try:
                record = json.loads(raw)
            except Exception:
                continue
            event = str(record.get("event") or "")
            if event not in accepted_events:
                continue
            if event == "bus_publish" and record.get("topic") != "enriched":
                continue
            ts_iso = record.get("ts_iso")
            if not ts_iso:
                continue
            try:
                ts = datetime.fromisoformat(str(ts_iso).replace("Z", "+00:00"))
            except Exception:
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts < cutoff:
                continue
            yield NewsTraderSignal(
                ts=ts,
                source=str(record.get("source") or ""),
                source_name=str(record.get("source_name") or ""),
                symbol=record.get("symbol"),
                category=record.get("category"),
                tier=record.get("tier"),
                score=record.get("score"),
                direction=record.get("direction"),
                headline=str(record.get("headline") or "")[:400],
                raw_event=event,
            )

    def aggregate(
        self,
        lookback_minutes: int = 240,
        tickers_of_interest: Iterable[str] | None = None,
    ) -> dict[str, TickerAttention]:
        watch = {str(t).upper().split("/")[0] for t in (tickers_of_interest or [])}
        per_ticker: dict[str, TickerAttention] = {}
        seen_keys: set[tuple[str, str]] = set()
        for signal in self.iter_signals(lookback_minutes=lookback_minutes):
            tickers = self._tickers_from_signal(signal)
            if not tickers:
                continue
            for ticker in tickers:
                if watch and ticker not in watch:
                    continue
                # Dedup the same (event, source+headline) for the same ticker.
                key = (ticker, signal.raw_event + "|" + signal.headline[:120])
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                attention = per_ticker.setdefault(ticker, TickerAttention(ticker=ticker))
                attention.mention_count += 1
                if signal.is_telegram:
                    attention.telegram_mention_count += 1
                if signal.tier == "strong":
                    attention.strong_tier_count += 1
                if signal.direction:
                    attention.direction_votes[signal.direction] += 1
                if signal.category:
                    attention.categories[signal.category] += 1
                self._tag_sentiment(signal, attention)
                src = signal.source_name or signal.source
                if src and src not in attention.sources:
                    attention.sources.append(src)
                if signal.headline and signal.headline not in attention.top_headlines:
                    attention.top_headlines.append(signal.headline)
                if attention.latest_ts is None or signal.ts > attention.latest_ts:
                    attention.latest_ts = signal.ts
        # Trim long lists.
        for attention in per_ticker.values():
            attention.sources = attention.sources[:8]
            attention.top_headlines = attention.top_headlines[:6]
        return per_ticker

    @staticmethod
    def _tickers_from_signal(signal: NewsTraderSignal) -> list[str]:
        out: list[str] = []
        if signal.symbol:
            raw = str(signal.symbol).upper().replace("/", "").replace("USDT", "")
            if raw in CATEGORY_TICKER_MAP:
                raw = CATEGORY_TICKER_MAP[raw]
            if raw and raw.isalnum():
                out.append(raw)
        # Also detect tickers in the headline as $TAG / #TAG / cashtag.
        if signal.headline:
            for token in re.findall(r"[#$]([A-Z]{2,10})\b", signal.headline.upper()):
                if token in {"USDT", "USD", "USDC", "BTC"} and token in out:
                    continue
                if token in CATEGORY_TICKER_MAP:
                    token = CATEGORY_TICKER_MAP[token]
                if token not in out:
                    out.append(token)
        return out

    @staticmethod
    def _tag_sentiment(signal: NewsTraderSignal, attention: TickerAttention) -> None:
        text = (signal.headline or "").lower()
        if not text:
            return
        for label, keywords in SENTIMENT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                if label == "bullish":
                    attention.bullish_count += 1
                elif label == "bearish":
                    attention.bearish_count += 1
                elif label == "macro_riskoff":
                    attention.riskoff_count += 1
                elif label == "macro_riskon":
                    attention.riskon_count += 1

    def macro_pulse(self, lookback_minutes: int = 240) -> dict[str, Any]:
        """Quick macro signal scan: how many recent strong/medium signals?

        Returns a small dict the report can consume directly.
        """
        signal_count = 0
        strong_count = 0
        per_category: Counter = Counter()
        per_source: Counter = Counter()
        for signal in self.iter_signals(lookback_minutes=lookback_minutes):
            signal_count += 1
            if signal.tier == "strong":
                strong_count += 1
            if signal.category:
                per_category[str(signal.category)] += 1
            if signal.source_name:
                per_source[str(signal.source_name)] += 1
        return {
            "available": self.available,
            "lookback_minutes": lookback_minutes,
            "signal_count": signal_count,
            "strong_count": strong_count,
            "top_categories": per_category.most_common(8),
            "top_sources": per_source.most_common(8),
        }

    @staticmethod
    def to_manual_social_notes(
        per_ticker: dict[str, TickerAttention],
        max_per_ticker: int = 3,
    ) -> list[dict[str, Any]]:
        """Convert TickerAttention into the shape CrowdAttentionAgent expects.

        Each headline becomes one note. Verification is set based on whether
        any signal was tier=strong from news_trader (already validated).
        """
        out: list[dict[str, Any]] = []
        for ticker, attention in per_ticker.items():
            for headline in attention.top_headlines[:max_per_ticker]:
                stance = attention.net_sentiment
                if stance == "bullish":
                    sentiment = "bullish"
                elif stance == "bearish":
                    sentiment = "bearish"
                else:
                    sentiment = "neutral"
                confidence = "high" if attention.strong_tier_count else "medium"
                verification = "confirmed" if attention.strong_tier_count else "single_source"
                ts = attention.latest_ts.isoformat() if attention.latest_ts else ""
                out.append(
                    {
                        "ticker": ticker,
                        "narrative": ", ".join(c for c, _ in attention.categories.most_common(2)),
                        "source": "news_trader_bridge",
                        "note": headline,
                        "timestamp": ts,
                        "sentiment": sentiment,
                        "confidence": confidence,
                        "verification": verification,
                    }
                )
        return out
