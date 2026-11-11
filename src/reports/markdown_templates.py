from __future__ import annotations

from src.models import TradeIdea
from src.signals.playbooks import label_from_trade_idea
from src.utils.formatting import bullet_list, fmt_float


def trade_idea_markdown(index: int, idea: TradeIdea) -> str:
    setup = idea.raw.get("setup", {})
    score = idea.raw.get("score", {})
    components = score.get("components", {})
    chart_path = idea.raw.get("chart_path")
    chart_block = f"\n**Chart**\n\n![{idea.symbol} setup chart]({chart_path})\n" if chart_path else ""
    # 2026-06-09: annotate every idea with its named playbook so the report
    # reader (and Opus) can reason by strategy, not just by tier/score. The
    # block is rendered just above the score breakdown.
    playbook_block = label_from_trade_idea(idea).to_markdown_block(heading_level=4)
    return f"""### Trade Idea #{index} - {idea.direction.upper()} {idea.symbol}

Score: {idea.score}/100
Confidence: {idea.confidence}
Trade Type: {idea.timeframe}
Risk: {idea.risk_level}

{playbook_block}

**Thesis**
{idea.thesis}

**Evidence**
{bullet_list(idea.evidence)}

**Score Breakdown**
{bullet_list([f"{key}: {value}" for key, value in components.items()] + [f"Risk penalty: -{score.get('risk_penalty', 'n/a')}"])}

**Entry Plan**
{idea.entry_plan}

**Invalidation**
{idea.invalidation}

**Targets**
{bullet_list(idea.targets)}

**Counter-Thesis**
{bullet_list(idea.counterarguments)}

**Conditions To Avoid**
{bullet_list(idea.avoid_conditions)}

**What To Monitor**
{bullet_list(idea.what_to_monitor)}

**Desk Notes**
- Current price: {fmt_float(setup.get("current_price"))}
- ATR: {fmt_float(setup.get("atr"))}
- Support: {fmt_float(setup.get("support"))}
- Resistance: {fmt_float(setup.get("resistance"))}
{chart_block}
"""
