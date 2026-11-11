"""Watchlist monitor: re-evaluate watchlist symbols on a tight cadence.

After a report leaves C-tier / watchlist names, the user wants to know
*the moment* one of them flips to a tradable B/A tier. Running a full
``intraday-report`` every 10 minutes is wasteful (>5 minutes of work). This
module does a minimal re-evaluation:

1. Load last known tiers from ``data/processed/agent_outputs/<latest>_trade_idea_agent.json``.
2. Refresh OHLCV (only mode timeframes) + derivatives for those symbols.
3. Re-run MarketRegime, Momentum, TechnicalSetup, Scoring, TradeIdea on
   the small subset.
4. Diff new vs previous tier. C → B/A (or rejected → B/A) emits an alert.

The diff and alert is persisted to ``watchlist_alerts`` for dedup; an alert
for the same symbol won't repeat within ``cooldown_minutes``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.agents.catalyst_agent import CatalystAgent
from src.agents.critic_agent import CriticAgent
from src.agents.derivatives_agent import DerivativesAgent
from src.agents.exchange_fusion_agent import ExchangeFusionAgent
from src.agents.market_regime_agent import MarketRegimeAgent
from src.agents.momentum_scanner_agent import MomentumScannerAgent
from src.agents.narrative_agent import NarrativeAgent
from src.agents.news_agent import NewsAgent
from src.agents.risk_agent import RiskAgent
from src.agents.scoring_agent import ScoringAgent
from src.agents.technical_setup_agent import TechnicalSetupAgent
from src.agents.trade_idea_agent import TradeIdeaAgent
from src.config import ProjectConfig
from src.agents.crowd_attention_agent import CrowdAttentionAgent
from src.agents.social_attention_agent import SocialAttentionAgent
from src.data_collectors.binance_collector import BinanceOHLCVCollector
from src.data_collectors.binance_derivatives_collector import BinanceDerivativesCollector
from src.data_collectors.manual_notes_loader import load_manual_social_notes
from src.data_collectors.multi_exchange_derivatives_collector import MultiExchangeDerivativesCollector
from src.data_collectors.news_trader_bridge import NewsTraderBridge
from src.logger import get_logger
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.utils.validation import model_to_dict


TIER_RANK = {"rejected": 0, "C": 1, "B": 2, "A": 3}


@dataclass
class WatchlistTick:
    symbol: str
    previous_tier: str
    new_tier: str
    score: float
    direction: str
    mode: str
    payload: dict[str, Any] = field(default_factory=dict)
    upgraded: bool = False

    @property
    def is_actionable(self) -> bool:
        # An upgrade FROM watchlist/rejected INTO B or A, with direction long/short.
        return (
            self.upgraded
            and self.new_tier in {"A", "B"}
            and self.direction in {"long", "short"}
        )

    @property
    def is_armed_watch_candidate(self) -> bool:
        """Whether this is a directional candidate worth persisting for revalidation.

        A C-tier idea is not actionable and must not create an entry alert, but
        it is still useful to retain as an Armed Watch when it has a complete
        setup.  The registry performs the final entry/stop geometry validation.
        Rejected/no-direction outputs remain research-only and never enter the
        watch lifecycle.
        """

        return (
            self.new_tier in {"A", "B", "C"}
            and self.direction in {"long", "short"}
        )


class WatchlistMonitor:
    def __init__(self, config: ProjectConfig, file_store: FileStore, db: SQLiteStore):
        self.config = config
        self.file_store = file_store
        self.db = db
        self.logger = get_logger(self.__class__.__name__)

    # ---------- Loading prior state ----------

    def latest_trade_idea_payload(self) -> dict[str, Any]:
        agent_dir = self.config.processed_dir / "agent_outputs"
        if not agent_dir.exists():
            return {}
        files = sorted(
            agent_dir.glob("*_trade_idea_agent.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not files:
            return {}
        try:
            with files[0].open("r", encoding="utf-8") as handle:
                return json.load(handle) or {}
        except Exception:
            return {}

    def baseline_tiers(self) -> tuple[dict[str, str], dict[str, dict[str, Any]], str]:
        payload = self.latest_trade_idea_payload()
        mode = str(payload.get("mode") or "intraday")
        per_symbol: dict[str, str] = {}
        per_idea: dict[str, dict[str, Any]] = {}
        for idea in payload.get("ideas", []) or []:
            symbol = str(idea.get("symbol"))
            tier = str(idea.get("tier") or "C")
            per_symbol[symbol] = tier
            per_idea[symbol] = idea
        for rejected in payload.get("rejected", []) or []:
            symbol = str(rejected.get("symbol"))
            if symbol not in per_symbol:
                per_symbol[symbol] = "rejected"
                per_idea[symbol] = rejected
        return per_symbol, per_idea, mode

    def watch_symbols(self) -> list[str]:
        """Symbols worth re-checking — C-tier watchlist + rejected with structure."""
        baselines, _, _ = self.baseline_tiers()
        return [
            symbol
            for symbol, tier in baselines.items()
            if tier in {"C", "rejected"}
        ]

    # ---------- Re-evaluation ----------

    def re_evaluate(self, symbols: list[str] | None = None) -> list[WatchlistTick]:
        baselines, baseline_ideas, mode = self.baseline_tiers()
        candidates = symbols or [s for s, t in baselines.items() if t in {"C", "rejected"}]
        if not candidates:
            return []
        # Always include BTC + ETH so MarketRegimeAgent works.
        watch_universe = list(dict.fromkeys(["BTC/USDT", "ETH/USDT", *candidates]))
        timeframes = self._mode_timeframes(mode)

        self.logger.info("Re-evaluating %d watchlist symbols (mode=%s)", len(candidates), mode)
        # 1. Refresh OHLCV (only anchor exchange — fast).
        BinanceOHLCVCollector(self.config, self.file_store).fetch(
            symbols=watch_universe, timeframes=timeframes
        )
        # 2. Refresh derivatives (Binance funding/OI + Bybit/OKX snapshot).
        try:
            BinanceDerivativesCollector(self.config, self.file_store).fetch(symbols=watch_universe)
        except Exception as exc:
            self.logger.warning("Binance derivatives refresh failed: %s", exc)
        try:
            MultiExchangeDerivativesCollector(self.config, self.file_store).fetch(symbols=watch_universe)
        except Exception as exc:
            self.logger.warning("Bybit/OKX derivatives refresh failed: %s", exc)

        # 3. Load market data + run lightweight pipeline.
        market_data = self.file_store.load_market_data(
            self.config.exchange_id, watch_universe, self.config.timeframes
        )
        if not market_data:
            self.logger.warning("No market data after refresh; aborting tick.")
            return []

        regime = MarketRegimeAgent(self.config, self.file_store, self.db).run(market_data)
        momentum = MomentumScannerAgent(self.config, self.file_store, self.db).run(
            market_data, symbols=list(market_data.keys())
        )
        derivatives_records = self._load_json(
            Path("data") / "raw" / "open_interest" / "binance_futures_latest.json"
        ).get("records", {})
        derivatives = DerivativesAgent(self.config, self.file_store, self.db).run(
            market_data, derivatives_records
        )
        news_rows = self.db.load_news_window(hours=48, limit=2000, asset_class="crypto")
        news_output = NewsAgent(self.config, self.file_store, self.db).run(news_rows)
        events = self.db.load_events(limit=100)
        catalysts = CatalystAgent(self.config, self.file_store, self.db).run(
            list(market_data.keys()), events, news_output
        )
        narratives = NarrativeAgent(self.config, self.file_store, self.db).run(
            momentum, news_output, catalysts
        )
        fused_payload = self._load_json(
            Path("data") / "processed" / "candidates" / "universe_ranked_candidates.json"
        )
        exchange_confirmations = ExchangeFusionAgent(self.config, self.file_store, self.db).run(
            fused_payload.get("candidates") or [],
            (self._load_json(Path("data") / "processed" / "exchange_symbol_map.json") or {}).get("by_symbol", {}),
        )
        setups = TechnicalSetupAgent(self.config, self.file_store, self.db).run(
            momentum, market_data, regime, limit=len(momentum)
        )
        # Pull fresh telegram + macro context from news_trader (read-only).
        # Crowd attention combines this with social_attention so a fresh
        # Telegram strong-tier signal can flip C → B during a monitor tick.
        try:
            bridge = NewsTraderBridge()
            bridge_notes: list[dict[str, Any]] = []
            if bridge.available:
                aggregated = bridge.aggregate(
                    lookback_minutes=180,
                    tickers_of_interest=[c.symbol for c in momentum],
                )
                bridge_notes = bridge.to_manual_social_notes(aggregated)
        except Exception as exc:
            self.logger.warning("news_trader bridge unavailable: %s", exc)
            bridge_notes = []
        combined_social = load_manual_social_notes(self.config.root) + bridge_notes
        # We don't re-run NewsAgent here — too heavy — so social_attention is
        # the simpler Reddit/manual stream. Re-using empty dict avoids the cost.
        social_attention: dict[str, Any] = {}
        CrowdAttentionAgent(self.config, self.file_store, self.db).run(
            momentum, social_attention, combined_social, derivatives
        )

        risks = RiskAgent(self.config, self.file_store, self.db).run(
            setups, momentum, regime, derivatives, catalysts
        )
        critiques = CriticAgent(self.config, self.file_store, self.db).run(
            setups, momentum, regime, derivatives, catalysts, risks
        )
        scores = ScoringAgent(self.config, self.file_store, self.db).run(
            setups,
            momentum,
            regime,
            derivatives,
            catalysts,
            risks,
            critiques,
            narratives,
            exchange_confirmations=exchange_confirmations,
            mode=mode,
        )
        # --- Weekend Mode overlay (safe: no-op when not active or on failure) ---
        try:
            from src.analysis import weekend_mode as _weekend_mode

            weekend_cfg = _weekend_mode.load_config(self.config.root)
            weekend_status = _weekend_mode.current_status(weekend_cfg, self.config.settings)
            _weekend_mode.apply_overlay(
                scores=scores,
                setups=setups,
                status=weekend_status,
                mode=mode,
                candidates=momentum,
            )
        except Exception as exc:  # pragma: no cover - overlay never breaks tick
            self.logger.warning("Weekend Mode overlay failed: %s", exc)

        ideas = TradeIdeaAgent(self.config, self.file_store, self.db).run(
            setups,
            momentum,
            scores,
            regime,
            derivatives,
            catalysts,
            risks,
            critiques,
            narratives,
            exchange_confirmations=exchange_confirmations,
            mode=mode,
        )

        # 4. Diff vs baselines.
        ticks: list[WatchlistTick] = []
        new_by_symbol = {idea.symbol: idea for idea in ideas}
        for symbol in candidates:
            new_idea = new_by_symbol.get(symbol)
            if new_idea is None:
                continue
            previous_tier = baselines.get(symbol, "rejected")
            new_tier = new_idea.tier
            upgraded = TIER_RANK.get(new_tier, 0) > TIER_RANK.get(previous_tier, 0)
            ticks.append(
                WatchlistTick(
                    symbol=symbol,
                    previous_tier=previous_tier,
                    new_tier=new_tier,
                    score=float(new_idea.score),
                    direction=new_idea.direction,
                    mode=mode,
                    payload=model_to_dict(new_idea),
                    upgraded=upgraded,
                )
            )
        return ticks

    # ---------- Helpers ----------

    def _mode_timeframes(self, mode: str) -> list[str]:
        block = (self.config.universe.get("modes") or {}).get(mode) or {}
        timeframes = [str(tf) for tf in block.get("timeframes", [])]
        if mode == "scalp" and "1h" not in timeframes:
            timeframes.append("1h")
        return timeframes or self.config.timeframes

    def _load_json(self, relative_path: Path) -> dict[str, Any]:
        payload = self.file_store.read_json(relative_path)
        return payload if isinstance(payload, dict) else {}

    @staticmethod
    def format_alert(tick: WatchlistTick) -> str:
        idea = tick.payload
        setup = (idea.get("raw") or {}).get("setup") or {}
        entry_low = setup.get("entry_low")
        entry_high = setup.get("entry_high")
        sl = setup.get("sl") or setup.get("invalidation")
        tp1 = setup.get("tp1")
        tp2 = setup.get("tp2")
        score = tick.score
        lines = [
            f"{tick.symbol} tier {tick.previous_tier} -> {tick.new_tier} ({tick.direction.upper()})",
            f"score {score:.1f} | mode {tick.mode} | confidence {idea.get('confidence')}",
        ]
        # Mode-Viability-Audit (2026-06-09): crypto scalp stays actionable
        # but is flagged low-confidence on the Telegram alert line so the
        # user sees the audit context next to the entry price.
        if tick.mode == "scalp" and (idea.get("asset_class") or "crypto") == "crypto":
            lines.append(
                "low confidence (mode audit) - entry edge OK, "
                "TP1/2h horizon mismatch caps capture; re-audit at 20 closed"
            )
        if entry_low and entry_high:
            lines.append(f"entry {entry_low} - {entry_high}")
        if sl:
            lines.append(f"SL: {sl}")
        if tp1:
            lines.append(f"TP1 {tp1} / TP2 {tp2}")
        thesis = idea.get("thesis")
        if thesis:
            lines.append("")
            lines.append(thesis[:400])
        cap_reasons = idea.get("cap_reasons") or []
        if cap_reasons:
            lines.append("")
            lines.append("caps: " + ", ".join(cap_reasons[:3]))
        return "\n".join(lines)

    def register_armed_watch_candidates(
        self,
        ticks: list[WatchlistTick],
        *,
        regime_label: str = "",
        report_id: str | None = None,
    ) -> dict[str, str]:
        """Persist every complete directional candidate as an Armed Watch.

        The persisted state is ``waiting_for_entry``.  This does *not* send a
        Telegram entry alert, trigger a paper position, or route anything to
        execution.  A/B promotion still controls alerting; C-tier candidates
        are retained quietly so the next revalidation can promote, invalidate,
        or expire a concrete setup instead of rediscovering it from scratch.

        Returns a map ``{symbol: signal_id}`` for ticks that registered
        successfully. The CLI uses the A/B subset of this map to gate Telegram
        setup alerts.
        """

        from src.models import TradeIdea
        from src.signals.config import load_signal_tracking_config
        from src.signals.registry import build_signal_from_idea, register_ideas

        candidates = [t for t in ticks if t.is_armed_watch_candidate]
        if not candidates:
            return {}
        try:
            config = load_signal_tracking_config(self.config.root)
        except Exception as exc:
            self.logger.warning("signal tracking config load failed: %s", exc)
            return {}
        if not config.enabled:
            return {}

        weekend_active = False
        try:
            from src.analysis import weekend_mode

            weekend_status = weekend_mode.current_status(
                weekend_mode.load_config(self.config.root),
                self.config.settings,
            )
            weekend_active = bool(getattr(weekend_status, "active", False))
        except Exception:
            weekend_active = False

        effective_report_id = report_id or (
            f"watchlist-monitor-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        )

        ideas: list[TradeIdea] = []
        for tick in candidates:
            payload = dict(tick.payload or {})
            # The payload was produced by ``model_to_dict(new_idea)`` — it
            # already matches the TradeIdea schema. If reconstruction fails
            # (schema drift, missing field), skip rather than alert without
            # tracking.
            try:
                idea = TradeIdea(**payload)
            except Exception as exc:
                self.logger.warning(
                    "watchlist register: rebuild TradeIdea failed for %s: %s",
                    tick.symbol,
                    exc,
                )
                continue
            ideas.append(idea)

        try:
            register_ideas(
                self.db,
                ideas,
                config=config,
                report_id=effective_report_id,
                market_regime=regime_label,
                weekend_mode_active=weekend_active,
            )
        except Exception as exc:
            self.logger.warning("watchlist register_ideas failed: %s", exc)
            return {}

        # Derive symbol → signal_id from the deterministic builder.
        symbol_to_signal: dict[str, str] = {}
        for idea in ideas:
            try:
                signal = build_signal_from_idea(
                    idea,
                    config=config,
                    report_id=effective_report_id,
                    market_regime=regime_label,
                    weekend_mode_active=weekend_active,
                )
            except Exception:
                signal = None
            if signal is not None:
                symbol_to_signal[idea.symbol] = signal.signal_id
        return symbol_to_signal

    def register_actionable_ticks(
        self,
        ticks: list[WatchlistTick],
        *,
        regime_label: str = "",
        report_id: str | None = None,
    ) -> dict[str, str]:
        """Compatibility wrapper for older callers.

        The lifecycle contract is now broader than the former name: all
        complete A/B/C directional candidates are Armed Watches, while only
        A/B upgrades are alert-eligible.
        """

        return self.register_armed_watch_candidates(
            ticks,
            regime_label=regime_label,
            report_id=report_id,
        )

    def should_alert(self, tick: WatchlistTick, cooldown_minutes: int) -> bool:
        if not tick.is_actionable:
            return False
        last = self.db.last_alert_for(tick.symbol)
        if last is None:
            return True
        try:
            sent_at = datetime.fromisoformat(str(last["sent_at"]).replace("Z", "+00:00"))
        except Exception:
            return True
        if sent_at.tzinfo is None:
            sent_at = sent_at.replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - sent_at).total_seconds() / 60
        if age < cooldown_minutes and last.get("new_tier") == tick.new_tier:
            return False
        return True
