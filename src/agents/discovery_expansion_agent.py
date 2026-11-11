"""Crypto signal expansion — parallel discovery surface.

Reads the outputs the existing pipeline already produced (momentum candidates,
catalysts, narrative baskets, derivatives features) and surfaces symbols that
fit one of the approved expansion playbooks but were NOT in the top-N setups
the trade-idea agent processed.

This module is **purely additive**:
- It does NOT modify scoring weights or thresholds.
- It does NOT register `proposed_signals`. The watchlist it produces is
  informational: rendered into reports + LLM packets to be reviewed manually.
- Newly discovered symbols are routed by default into the **shadow / C-tier
  manual-review lane** described in PART 4 of the spec.
- Crypto scalp playbook is explicitly **excluded** from expansion (PART 3).

See `reports/CRYPTO_SIGNAL_EXPANSION_PRECHECK.md` for the baseline and
`reports/STRATEGY_PLAYBOOK_AUDIT.md` for the playbook contract.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from src.signals.playbooks import (
    PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT,
    PLAYBOOK_CRYPTO_INTRADAY,
    PLAYBOOK_CRYPTO_RS_LEADER,
    PLAYBOOK_CRYPTO_SWING,
    label_for,
)


# Quality thresholds for the expansion shadow → A/B promotion gate.
# Conservative; do not lower without re-running PART 1 precheck.
MIN_QUOTE_VOLUME_24H_USD = 5_000_000.0     # below this we mark "thin_liquidity"
MIN_DEEP_VOLUME_RATIO = 0.5                # 0.5× 20-period avg
SQUEEZE_UPPER_WICK_ATR_MAX = 2.0           # above this → squeeze risk flag
EXTREME_NEGATIVE_FUNDING = -0.05           # −5% / 8h funding rate cap
TOP_RS_BTC_THRESHOLD = 2.5                 # RS-vs-BTC % over window
TOP_RS_ETH_THRESHOLD = 2.5
TOP_24H_MOMENTUM_THRESHOLD = 5.0           # 24h return %
TOP_7D_MOMENTUM_THRESHOLD = 12.0
RECOVERY_RS_BTC_THRESHOLD = 1.5            # weak market but symbol up
SHORT_BREAKDOWN_RS_BTC_THRESHOLD = -2.0    # weaker than BTC by this much
UNUSUAL_VOLUME_RATIO_THRESHOLD = 1.8       # volume_ratio over 1.8 = unusual

# Maximum entries to surface per discovery source (prevents flooding).
MAX_PER_SOURCE = 5
MAX_TOTAL_WATCHLIST = 25


@dataclass
class ExpansionCandidate:
    symbol: str
    discovery_source: str
    candidate_playbook: str
    direction_bias: str
    momentum_score: float | None
    return_24h: float | None
    return_7d: float | None
    rs_btc: float | None
    rs_eth: float | None
    volume_ratio: float | None
    quote_volume_24h_usd: float | None
    upper_wick_atr_max: float | None
    funding_rate: float | None = None
    derivatives_available: bool = False
    in_top_setups: bool = False
    quality_flags: list[str] = field(default_factory=list)
    promotion_blockers: list[str] = field(default_factory=list)
    why_not_ab_yet: str = ""
    what_would_promote: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "discovery_source": self.discovery_source,
            "candidate_playbook": self.candidate_playbook,
            "direction_bias": self.direction_bias,
            "momentum_score": self.momentum_score,
            "return_24h": self.return_24h,
            "return_7d": self.return_7d,
            "rs_btc": self.rs_btc,
            "rs_eth": self.rs_eth,
            "volume_ratio": self.volume_ratio,
            "quote_volume_24h_usd": self.quote_volume_24h_usd,
            "upper_wick_atr_max": self.upper_wick_atr_max,
            "funding_rate": self.funding_rate,
            "derivatives_available": self.derivatives_available,
            "in_top_setups": self.in_top_setups,
            "quality_flags": self.quality_flags,
            "promotion_blockers": self.promotion_blockers,
            "why_not_ab_yet": self.why_not_ab_yet,
            "what_would_promote": self.what_would_promote,
        }


@dataclass
class ExpansionResult:
    candidates: list[ExpansionCandidate] = field(default_factory=list)
    counts_by_source: dict[str, int] = field(default_factory=dict)
    skipped_scalp: int = 0
    skipped_in_top_setups: int = 0
    total_evaluated: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidates": [c.to_dict() for c in self.candidates],
            "counts_by_source": dict(self.counts_by_source),
            "skipped_scalp": self.skipped_scalp,
            "skipped_in_top_setups": self.skipped_in_top_setups,
            "total_evaluated": self.total_evaluated,
        }


def _candidate_features(c: Any) -> dict[str, Any]:
    """Tolerant accessor — supports pydantic MomentumCandidate or plain dict."""
    if isinstance(c, dict):
        return c
    return {
        "symbol": getattr(c, "symbol", ""),
        "direction_bias": getattr(c, "direction_bias", "watch"),
        "score": getattr(c, "score", 0.0),
        "return_24h": getattr(c, "return_24h", None),
        "return_7d": getattr(c, "return_7d", None),
        "relative_strength_btc": getattr(c, "relative_strength_btc", None),
        "relative_strength_eth": getattr(c, "relative_strength_eth", None),
        "volume_ratio": getattr(c, "volume_ratio", None),
        "atr_percentile": getattr(c, "atr_percentile", None),
        "reason_tags": getattr(c, "reason_tags", []) or [],
        "upper_wick_atr_max": getattr(c, "upper_wick_atr_max", None),
        "quote_volume_24h_usd": getattr(c, "quote_volume_24h_usd", None),
    }


def _playbook_for(direction: str, *, news_supported: bool, mode: str) -> str:
    """Map an expansion candidate to a playbook label string."""
    if direction == "short":
        return PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT
    if mode == "swing":
        return PLAYBOOK_CRYPTO_SWING
    if news_supported:
        return PLAYBOOK_CRYPTO_INTRADAY  # catalyst-backed
    if mode == "intraday":
        return PLAYBOOK_CRYPTO_INTRADAY
    return PLAYBOOK_CRYPTO_SWING


def _quality_gates(c: ExpansionCandidate, *, derivatives_required: bool) -> tuple[list[str], list[str]]:
    """Return (quality_flags_passed, promotion_blockers_present)."""
    flags: list[str] = []
    blockers: list[str] = []

    # Liquidity
    qv = c.quote_volume_24h_usd
    if qv is not None and qv >= MIN_QUOTE_VOLUME_24H_USD:
        flags.append("liquid_enough")
    else:
        blockers.append(
            f"thin_liquidity (24h quote_vol "
            f"{f'${qv/1e6:.1f}M' if qv else 'unknown'} < "
            f"${MIN_QUOTE_VOLUME_24H_USD/1e6:.0f}M)"
        )

    vr = c.volume_ratio
    if vr is not None and vr >= MIN_DEEP_VOLUME_RATIO:
        flags.append("active_volume")
    else:
        blockers.append("low_volume_ratio")

    # Squeeze guard for shorts
    if c.direction_bias == "short":
        if c.upper_wick_atr_max is not None and c.upper_wick_atr_max >= SQUEEZE_UPPER_WICK_ATR_MAX:
            blockers.append(
                f"squeeze_risk_upper_wick (avg upper-wick {c.upper_wick_atr_max:.1f}× ATR)"
            )
        if c.funding_rate is not None and c.funding_rate <= EXTREME_NEGATIVE_FUNDING:
            blockers.append(
                f"extreme_negative_funding ({c.funding_rate*100:.1f}%)"
            )
        if derivatives_required and not c.derivatives_available:
            blockers.append("derivatives_missing_for_short")
    else:
        if c.upper_wick_atr_max is not None and c.upper_wick_atr_max >= SQUEEZE_UPPER_WICK_ATR_MAX:
            flags.append("high_wick_extension (for longs: possible exhaustion)")

    # Derivatives availability (for short / catalyst paths)
    if derivatives_required and c.derivatives_available:
        flags.append("derivatives_ok")

    return flags, blockers


def _why_not_ab(c: ExpansionCandidate) -> str:
    if c.in_top_setups:
        return "Already in top-N deep setups — no separate watchlist entry needed"
    if c.candidate_playbook == "crypto_scalp_momentum_continuation":
        return "scalp playbook excluded from expansion (PART 3)"
    if c.promotion_blockers:
        return "; ".join(c.promotion_blockers[:3])
    return "Below current scoring threshold; manual review can promote with corroborating context"


def _what_promotes(c: ExpansionCandidate) -> str:
    if c.candidate_playbook == PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT:
        return "Confirm bearish HTF structure + derivatives data + clear stop above swing high; squeeze guard must remain clean."
    if c.candidate_playbook in (PLAYBOOK_CRYPTO_SWING, PLAYBOOK_CRYPTO_RS_LEADER):
        return "Confirm RS leadership + narrative basket membership + pullback into entry zone; chase risk if 24h move >30% without consolidation."
    if c.candidate_playbook == PLAYBOOK_CRYPTO_INTRADAY:
        return "Confirm fresh catalyst + RS not contradicting + entry structure on 15m–1h."
    return "Manual review and a corroborating thesis from another lane."


class DiscoveryExpansionAgent:
    """Surfaces expansion candidates beyond the top-N deep analysis cap.

    Read-only: takes already-computed pipeline outputs as inputs and produces
    a structured `ExpansionResult`. Does NOT modify candidates / setups / scoring
    / signals. Does NOT send Telegram. Does NOT register proposed_signals.
    """

    name = "discovery_expansion_agent"

    def run(
        self,
        *,
        candidates: Sequence[Any],
        narratives: dict[str, Any] | None = None,
        catalysts: dict[str, Any] | None = None,
        derivatives: dict[str, Any] | None = None,
        top_setup_symbols: Iterable[str] = (),
        mode: str = "intraday",
    ) -> ExpansionResult:
        narratives = narratives or {}
        catalysts = catalysts or {}
        derivatives = derivatives or {}
        top_setups = {s.upper() for s in top_setup_symbols}
        result = ExpansionResult()

        # Index candidates by symbol for cross-source lookup.
        by_symbol: dict[str, dict[str, Any]] = {}
        for raw in candidates:
            feats = _candidate_features(raw)
            sym = (feats.get("symbol") or "").upper()
            if not sym:
                continue
            by_symbol[sym] = feats

        # Index catalyst-tagged symbols.
        catalyst_symbols: set[str] = set()
        for sym_key, info in (catalysts.items() if isinstance(catalysts, dict) else []):
            if isinstance(info, dict) and (info.get("events") or info.get("recent_news") or info.get("score", 0) > 0):
                catalyst_symbols.add(str(sym_key).upper())
            elif info:
                catalyst_symbols.add(str(sym_key).upper())

        # Index narrative basket members.
        narrative_symbols: set[str] = set()
        if isinstance(narratives, dict):
            for nb_key, nb_val in narratives.items():
                if isinstance(nb_val, dict):
                    for sym in (nb_val.get("symbols") or nb_val.get("members") or []):
                        narrative_symbols.add(str(sym).upper())
                elif isinstance(nb_val, list):
                    for sym in nb_val:
                        narrative_symbols.add(str(sym).upper())

        # Walk sources and collect.
        added: set[tuple[str, str]] = set()  # (symbol, source) — avoid double-add

        def _add(symbol: str, source: str, direction: str, mode_hint: str,
                 news_supported: bool = False):
            sym = symbol.upper()
            key = (sym, source)
            if key in added:
                return
            if sym not in by_symbol:
                return
            feats = by_symbol[sym]
            playbook = _playbook_for(direction, news_supported=news_supported, mode=mode_hint)
            # PART 3: scalp expansion is explicitly forbidden.
            if playbook == "crypto_scalp_momentum_continuation":
                result.skipped_scalp += 1
                return
            deriv_record = (derivatives or {}).get(sym) or {}
            funding = deriv_record.get("funding_rate") if isinstance(deriv_record, dict) else None
            has_deriv = bool(deriv_record) and not deriv_record.get("error") if isinstance(deriv_record, dict) else bool(deriv_record)
            in_top = sym in top_setups
            if in_top:
                result.skipped_in_top_setups += 1
                # Still record (so the report shows visibility) but mark as "already in top"
            cand = ExpansionCandidate(
                symbol=sym,
                discovery_source=source,
                candidate_playbook=playbook,
                direction_bias=direction,
                momentum_score=feats.get("score"),
                return_24h=feats.get("return_24h"),
                return_7d=feats.get("return_7d"),
                rs_btc=feats.get("relative_strength_btc"),
                rs_eth=feats.get("relative_strength_eth"),
                volume_ratio=feats.get("volume_ratio"),
                quote_volume_24h_usd=feats.get("quote_volume_24h_usd"),
                upper_wick_atr_max=feats.get("upper_wick_atr_max"),
                funding_rate=funding,
                derivatives_available=has_deriv,
                in_top_setups=in_top,
            )
            derivatives_required = direction == "short" or news_supported
            flags, blockers = _quality_gates(cand, derivatives_required=derivatives_required)
            cand.quality_flags = flags
            cand.promotion_blockers = blockers
            cand.why_not_ab_yet = _why_not_ab(cand)
            cand.what_would_promote = _what_promotes(cand)
            result.candidates.append(cand)
            added.add(key)
            result.counts_by_source[source] = result.counts_by_source.get(source, 0) + 1

        # Source 1: top RS vs BTC (longs)
        rs_btc_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("relative_strength_btc") or -999)
             for feats in by_symbol.values()),
            key=lambda x: x[1], reverse=True,
        )
        for sym, rs in rs_btc_sorted[:MAX_PER_SOURCE]:
            if rs >= TOP_RS_BTC_THRESHOLD:
                _add(sym, "rs_btc_leader", "long", "swing")

        # Source 2: top RS vs ETH (longs)
        rs_eth_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("relative_strength_eth") or -999)
             for feats in by_symbol.values()),
            key=lambda x: x[1], reverse=True,
        )
        for sym, rs in rs_eth_sorted[:MAX_PER_SOURCE]:
            if rs >= TOP_RS_ETH_THRESHOLD:
                _add(sym, "rs_eth_leader", "long", "swing")

        # Source 3: 24h momentum leaders (longs)
        ret24_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("return_24h") or -999)
             for feats in by_symbol.values()),
            key=lambda x: x[1], reverse=True,
        )
        for sym, ret in ret24_sorted[:MAX_PER_SOURCE]:
            if ret >= TOP_24H_MOMENTUM_THRESHOLD:
                _add(sym, "momentum_24h_leader", "long",
                     "swing" if mode == "swing" else "intraday")

        # Source 4: 7d momentum leaders (longs, swing-biased)
        ret7d_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("return_7d") or -999)
             for feats in by_symbol.values()),
            key=lambda x: x[1], reverse=True,
        )
        for sym, ret in ret7d_sorted[:MAX_PER_SOURCE]:
            if ret >= TOP_7D_MOMENTUM_THRESHOLD:
                _add(sym, "momentum_7d_leader", "long", "swing")

        # Source 5: catalyst-backed names (intraday/swing — direction long by default)
        for sym in sorted(catalyst_symbols)[:MAX_PER_SOURCE * 2]:
            _add(sym, "catalyst_backed", "long",
                 "intraday" if mode != "swing" else "swing",
                 news_supported=True)

        # Source 6: narrative basket members (longs, swing-biased)
        for sym in sorted(narrative_symbols)[:MAX_PER_SOURCE]:
            _add(sym, "narrative_basket", "long", "swing")

        # Source 7: unusual volume expansion (long or short — direction from candidate bias)
        vol_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("volume_ratio") or 0)
             for feats in by_symbol.values()),
            key=lambda x: x[1], reverse=True,
        )
        for sym, vr in vol_sorted[:MAX_PER_SOURCE]:
            if vr >= UNUSUAL_VOLUME_RATIO_THRESHOLD:
                feats = by_symbol.get(sym, {})
                direction = "long" if (feats.get("direction_bias") in ("long", "watch")) else "short"
                _add(sym, "unusual_volume", direction,
                     "intraday" if mode != "swing" else "swing")

        # Source 8: short candidates — weak RS vs BTC + breakdown tags
        weak_rs_sorted = sorted(
            ((feats.get("symbol", ""), feats.get("relative_strength_btc") or 999)
             for feats in by_symbol.values()),
            key=lambda x: x[1],
        )
        for sym, rs in weak_rs_sorted[:MAX_PER_SOURCE]:
            if rs <= SHORT_BREAKDOWN_RS_BTC_THRESHOLD:
                _add(sym, "weak_rs_short", "short",
                     "intraday" if mode != "swing" else "swing")

        # Cap total to avoid flooding the report.
        result.total_evaluated = len(result.candidates)
        if len(result.candidates) > MAX_TOTAL_WATCHLIST:
            # Prefer entries with at least one promotion blocker resolved,
            # then by momentum_score.
            result.candidates.sort(
                key=lambda c: (
                    -len(c.quality_flags),
                    -(c.momentum_score or 0),
                )
            )
            result.candidates = result.candidates[:MAX_TOTAL_WATCHLIST]
        return result


def render_expansion_watchlist_markdown(result: ExpansionResult) -> str:
    """Render the expansion watchlist as a markdown section."""
    lines = [
        "## 7e. Crypto Expansion Watchlist",
        "",
        "_Discovered by `DiscoveryExpansionAgent` beyond the top-N deep "
        "analysis cap. **Informational — not a Telegram-actionable signal.** "
        "Routed to C-tier / shadow until a corroborating thesis lifts them._",
        "",
    ]
    if not result.candidates:
        lines.append("- _No expansion candidates this cycle._")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        f"_Evaluated: {result.total_evaluated} · "
        f"by source: {result.counts_by_source} · "
        f"skipped (scalp playbook): {result.skipped_scalp} · "
        f"already in top setups: {result.skipped_in_top_setups}_"
    )
    lines.append("")
    lines.append("| Symbol | Source | Playbook | Dir | Score | RS-BTC | Vol×| Status | Why not A/B | Promotes when |")
    lines.append("|---|---|---|---|---:|---:|---:|---|---|---|")
    for c in result.candidates:
        score = f"{c.momentum_score:.0f}" if c.momentum_score is not None else "—"
        rs = f"{c.rs_btc:+.1f}%" if c.rs_btc is not None else "—"
        vr = f"{c.volume_ratio:.1f}x" if c.volume_ratio is not None else "—"
        status = "in-top" if c.in_top_setups else ("shadow / C-tier" if c.promotion_blockers else "ready-for-promotion")
        why = c.why_not_ab_yet[:90]
        promotes = c.what_would_promote[:90]
        lines.append(
            f"| `{c.symbol}` | {c.discovery_source} | `{c.candidate_playbook}` | {c.direction_bias} | "
            f"{score} | {rs} | {vr} | {status} | {why} | {promotes} |"
        )
    lines.append("")
    lines.append("Source: `src/agents/discovery_expansion_agent.py` — read-only; "
                 "no proposed_signals written. See `reports/CRYPTO_SIGNAL_EXPANSION_REPORT.md`.")
    lines.append("")
    return "\n".join(lines)
