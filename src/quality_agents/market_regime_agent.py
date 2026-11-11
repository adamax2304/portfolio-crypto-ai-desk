from __future__ import annotations

import json
import sqlite3
from datetime import timedelta

from .config import QualityAgentsConfig
from .helpers import make_verdict
from .schemas import AgentVerdict, SignalContext, Verdict, parse_utc
from .store import table_exists


class MarketRegimeAgent:
    name = "market_regime"
    version = "market_regime_quality_v1"

    def evaluate(
        self, conn: sqlite3.Connection, context: SignalContext, cfg: QualityAgentsConfig,
    ) -> AgentVerdict:
        if not table_exists(conn, "market_dashboard_snapshots"):
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.INSUFFICIENT_DATA,
                confidence=0.2, reason_codes=["MARKET_SNAPSHOT_MISSING"], evidence={},
                context=context, cfg=cfg,
            )
        rows = [dict(row) for row in conn.execute(
            "SELECT * FROM market_dashboard_snapshots ORDER BY id DESC LIMIT 30"
        ).fetchall()]
        selected = None
        snapshot_at = None
        for row in rows:
            at = parse_utc(row.get("timestamp") or row.get("created_at"))
            if at is not None and at <= context.decision_at:
                selected, snapshot_at = row, at
                break
        if selected is None or snapshot_at is None:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.INSUFFICIENT_DATA,
                confidence=0.25, reason_codes=["POINT_IN_TIME_MARKET_SNAPSHOT_MISSING"],
                evidence={}, context=context, cfg=cfg,
            )

        stock = context.asset_class in {"stocks", "stock", "stock_futures"}
        prefix = "stocks" if stock else "crypto"
        market_mode = str(selected.get(f"{prefix}_market_mode") or "unknown").lower()
        regime = str(selected.get(f"{prefix}_regime") or "unknown").lower()
        age_minutes = max(0.0, (context.decision_at - snapshot_at).total_seconds() / 60.0)
        try:
            raw = json.loads(selected.get("raw_json") or "{}")
        except (TypeError, json.JSONDecodeError):
            raw = {}
        evidence = {
            "snapshot_id": selected.get("id"),
            "snapshot_at": snapshot_at.isoformat(),
            "snapshot_age_minutes": round(age_minutes, 3),
            "market_mode": market_mode,
            "market_regime": regime,
            "confidence": selected.get("confidence"),
            "generated_by": selected.get("generated_by"),
            "spy_trend": selected.get("spy_trend"),
            "qqq_trend": selected.get("qqq_trend"),
            "vix": selected.get("vix"),
            "btc_trend": raw.get("btc_trend"),
        }
        max_age = float(cfg.get("market_snapshot_max_age_minutes", 90))
        if age_minutes > max_age:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.INSUFFICIENT_DATA,
                confidence=0.35, reason_codes=["MARKET_SNAPSHOT_STALE"], evidence=evidence,
                context=context, cfg=cfg,
            )
        combined = f"{market_mode} {regime}"
        bearish = any(token in combined for token in ("risk_off", "risk-off", "bearish", "danger", "panic"))
        bullish = any(token in combined for token in ("risk_on", "risk-on", "bullish", "uptrend"))
        choppy = any(token in combined for token in ("chop", "range", "transition", "neutral", "mixed"))
        conflict = (context.direction == "long" and bearish) or (context.direction == "short" and bullish)
        aligned = (context.direction == "long" and bullish) or (context.direction == "short" and bearish)
        if conflict:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.84, reason_codes=["MARKET_DIRECTION_CONFLICT"],
                evidence=evidence, context=context, cfg=cfg,
            )
        if choppy:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.CAUTION,
                confidence=0.7, reason_codes=["MARKET_REGIME_MIXED"],
                evidence=evidence, context=context, cfg=cfg,
            )
        if aligned:
            return make_verdict(
                name=self.name, version=self.version, verdict=Verdict.SUPPORT,
                confidence=0.8, reason_codes=["MARKET_DIRECTION_ALIGNED"],
                evidence=evidence, context=context, cfg=cfg,
            )
        return make_verdict(
            name=self.name, version=self.version, verdict=Verdict.PASS,
            confidence=0.55, reason_codes=["MARKET_REGIME_NEUTRAL"],
            evidence=evidence, context=context, cfg=cfg,
        )
