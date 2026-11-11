from __future__ import annotations

from datetime import datetime, timezone

from .config import QualityAgentsConfig
from .schemas import AgentVerdict, ReducedDecision, ReducerAction, Verdict


def _recommend(
    verdicts: list[tuple[str, AgentVerdict]], cfg: QualityAgentsConfig,
) -> tuple[ReducerAction, tuple[str, ...], tuple[str, ...]]:
    ids = tuple(verdict_id for verdict_id, _ in verdicts)
    all_codes = tuple(dict.fromkeys(
        code for _, verdict in verdicts for code in verdict.reason_codes
    ))
    hard = [
        code for _, verdict in verdicts if verdict.verdict == Verdict.BLOCK_HARD
        for code in verdict.reason_codes if code in cfg.hard_block_allowlist
    ]
    if hard:
        return ReducerAction.BLOCK_HARD, tuple(dict.fromkeys(hard)), ids
    cautions = [verdict for _, verdict in verdicts if verdict.verdict == Verdict.CAUTION]
    if any(verdict.agent_name in {"event_risk", "market_regime"} for verdict in cautions):
        return ReducerAction.ALLOW_HALF_SIZE, all_codes, ids
    if any(verdict.agent_name == "news_entity" for verdict in cautions):
        return ReducerAction.ALLOW_NO_CATALYST_BOOST, all_codes, ids
    if verdicts and all(
        verdict.verdict in {Verdict.INSUFFICIENT_DATA, Verdict.ERROR}
        for _, verdict in verdicts
    ):
        return ReducerAction.REVIEW_ONLY, all_codes, ids
    return ReducerAction.ALLOW, all_codes, ids


def reduce_verdicts(
    verdicts: list[tuple[str, AgentVerdict]], cfg: QualityAgentsConfig,
) -> ReducedDecision:
    recommended, reasons, ids = _recommend(verdicts, cfg)
    applied = ReducerAction.ALLOW
    if cfg.operation_mode == "enforced":
        enforceable = [
            item for item in verdicts if cfg.agent_mode(item[1].agent_name) == "enforced"
        ]
        if enforceable:
            applied, _, _ = _recommend(enforceable, cfg)
    return ReducedDecision(
        recommended_action=recommended,
        applied_action=applied,
        reason_codes=reasons,
        verdict_ids=ids,
        operation_mode=cfg.operation_mode,
        created_at=datetime.now(timezone.utc),
    )


__all__ = ["reduce_verdicts"]
