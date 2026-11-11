from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config

from .store import connect, ensure_tables, table_exists


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _book(values: list[float]) -> dict[str, Any]:
    wins = [value for value in values if value > 0]
    losses = [value for value in values if value < 0]
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    return {
        "n": len(values),
        "wins": len(wins),
        "losses": len(losses),
        "sum_r": round(sum(values), 4),
        "pf": round(gross_profit / gross_loss, 4) if gross_loss > 0 else None,
    }


def build_effectiveness_report(
    *, db: str | Path | None = None, lookback_days: int = 30,
) -> tuple[str, dict[str, Any]]:
    db_path = Path(db or load_config().db_path)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=max(1, lookback_days))).isoformat()
    with connect(db_path, timeout_seconds=30.0) as conn:
        ensure_tables(conn)
        run_rows = [dict(row) for row in conn.execute(
            "SELECT agent_name,COUNT(*) n,"
            "SUM(CASE WHEN status='ERROR' THEN 1 ELSE 0 END) errors,"
            "ROUND(AVG(latency_ms),3) avg_ms,ROUND(MAX(latency_ms),3) max_ms "
            "FROM quality_agent_runs WHERE completed_at>=? GROUP BY agent_name ORDER BY agent_name",
            (cutoff,),
        ).fetchall()]
        active_incidents = [dict(row) for row in conn.execute(
            "SELECT severity,incident_type,COUNT(*) n FROM quality_agent_execution_incidents "
            "WHERE status='ACTIVE' GROUP BY severity,incident_type ORDER BY severity DESC,incident_type"
        ).fetchall()]
        post_rows = [dict(row) for row in conn.execute(
            "SELECT source_book,primary_category,COUNT(*) n,ROUND(SUM(COALESCE(result_r,0)),3) sum_r,"
            "ROUND(SUM(COALESCE(result_usdt,0)),2) sum_usdt "
            "FROM quality_agent_post_trade_diagnostics WHERE created_at>=? "
            "GROUP BY source_book,primary_category ORDER BY source_book,sum_r",
            (cutoff,),
        ).fetchall()]
        llm_rows: list[dict[str, Any]] = []
        if table_exists(conn, "quality_agent_llm_assessments"):
            llm_rows = [dict(row) for row in conn.execute(
                "SELECT status,verdict,COUNT(*) n,ROUND(AVG(latency_ms),3) avg_ms,"
                "ROUND(MAX(latency_ms),3) max_ms "
                "FROM quality_agent_llm_assessments WHERE created_at>=? "
                "GROUP BY status,verdict ORDER BY status,verdict",
                (cutoff,),
            ).fetchall()]

        experiment_assignments: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        experiment_values: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: defaultdict(list)
        )
        if table_exists(conn, "quality_agent_experiment_assignments"):
            assignment_rows = [dict(row) for row in conn.execute(
                "SELECT experiment_name,cohort,COUNT(*) n "
                "FROM quality_agent_experiment_assignments WHERE assigned_at>=? "
                "GROUP BY experiment_name,cohort",
                (cutoff,),
            ).fetchall()]
            for row in assignment_rows:
                experiment_assignments[str(row["experiment_name"])][str(row["cohort"])] = int(
                    row["n"] or 0
                )
            if table_exists(conn, "paper_execution_outcomes"):
                outcome_rows = [dict(row) for row in conn.execute(
                    "SELECT a.experiment_name,a.cohort,o.paper_execution_r "
                    "FROM quality_agent_experiment_assignments a "
                    "JOIN paper_execution_outcomes o ON o.signal_id=a.signal_id "
                    "WHERE a.assigned_at>=? AND o.paper_execution_r IS NOT NULL",
                    (cutoff,),
                ).fetchall()]
                for row in outcome_rows:
                    value = _number(row.get("paper_execution_r"))
                    if value is not None:
                        experiment_values[str(row["experiment_name"])][str(row["cohort"])].append(value)

        effectiveness: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        verdict_rows: list[dict[str, Any]] = []
        if table_exists(conn, "paper_execution_outcomes"):
            verdict_rows = [dict(row) for row in conn.execute(
                "WITH latest AS ("
                " SELECT v.* FROM quality_agent_signal_verdicts v JOIN ("
                "  SELECT signal_id,agent_name,stage,MAX(rowid) rid "
                "  FROM quality_agent_signal_verdicts WHERE created_at>=? "
                "  GROUP BY signal_id,agent_name,stage"
                " ) x ON x.rid=v.rowid"
                ") SELECT l.agent_name,l.verdict,l.reason_codes_json,l.signal_id,"
                "o.paper_execution_r,o.close_reason "
                "FROM latest l JOIN paper_execution_outcomes o ON o.signal_id=l.signal_id "
                "WHERE l.stage IN ('live_capture','live_decision_insert') "
                "AND o.paper_execution_r IS NOT NULL",
                (cutoff,),
            ).fetchall()]
            for row in verdict_rows:
                value = _number(row.get("paper_execution_r"))
                if value is not None:
                    effectiveness[str(row["agent_name"])][str(row["verdict"])].append(value)

        reducer_rows: list[dict[str, Any]] = []
        if table_exists(conn, "paper_execution_outcomes"):
            reducer_rows = [dict(row) for row in conn.execute(
                "WITH latest AS ("
                " SELECT r.* FROM quality_agent_reducer_decisions r JOIN ("
                "  SELECT signal_id,stage,MAX(rowid) rid FROM quality_agent_reducer_decisions "
                "  WHERE created_at>=? GROUP BY signal_id,stage"
                " ) x ON x.rid=r.rowid"
                ") SELECT l.*,o.paper_execution_r FROM latest l "
                "JOIN paper_execution_outcomes o ON o.signal_id=l.signal_id "
                "WHERE l.stage IN ('live_capture','live_decision_insert') "
                "AND o.paper_execution_r IS NOT NULL",
                (cutoff,),
            ).fetchall()]
        would_block = [
            float(row["paper_execution_r"]) for row in reducer_rows
            if str(row.get("recommended_action")) == "BLOCK_HARD"
        ]
        would_half = [
            float(row["paper_execution_r"]) for row in reducer_rows
            if str(row.get("recommended_action")) == "ALLOW_HALF_SIZE"
        ]
        counterfactual = {
            "hard_block": {
                **_book(would_block),
                "saved_losers": sum(1 for value in would_block if value < 0),
                "missed_winners": sum(1 for value in would_block if value > 0),
                "net_delta_r_if_omitted": round(-sum(would_block), 4),
            },
            "half_size": {
                **_book(would_half),
                "net_delta_r_vs_full_size": round(-0.5 * sum(would_half), 4),
            },
        }

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lookback_days": lookback_days,
        "runs": run_rows,
        "active_incidents": active_incidents,
        "post_trade": post_rows,
        "llm_assessments": llm_rows,
        "llm_experiments": {
            name: {
                cohort: {
                    "assigned": count,
                    "closed": _book(experiment_values[name].get(cohort, [])),
                }
                for cohort, count in cohorts.items()
            }
            for name, cohorts in experiment_assignments.items()
        },
        "counterfactual": counterfactual,
        "effectiveness": {
            agent: {verdict: _book(values) for verdict, values in buckets.items()}
            for agent, buckets in effectiveness.items()
        },
    }
    lines = [
        "# Quality Agents Effectiveness",
        "",
        f"Generated: `{summary['generated_at']}` | lookback: `{lookback_days}d`",
        "",
        "All agents are measured point-in-time. `recommended_action` is counterfactual; "
        "`applied_action` remains `ALLOW` while the system is in shadow mode.",
        "",
        "## Runtime",
        "",
    ]
    if run_rows:
        for row in run_rows:
            error_rate = (int(row["errors"] or 0) / int(row["n"] or 1)) * 100.0
            lines.append(
                f"- `{row['agent_name']}`: n={row['n']}, errors={row['errors']} "
                f"({error_rate:.1f}%), avg={row['avg_ms']}ms, max={row['max_ms']}ms"
            )
    else:
        lines.append("- No runs yet.")
    lines.extend(["", "## Matched Outcomes", ""])
    if summary["effectiveness"]:
        for agent, buckets in summary["effectiveness"].items():
            for verdict, book in buckets.items():
                pf = "inf" if book["pf"] is None and book["sum_r"] > 0 else str(book["pf"])
                lines.append(
                    f"- `{agent}` / `{verdict}`: n={book['n']}, W/L={book['wins']}/{book['losses']}, "
                    f"sum={book['sum_r']:+.2f}R, PF={pf}"
                )
    else:
        lines.append("- No closed matched Paper outcomes yet.")
    hard = counterfactual["hard_block"]
    half = counterfactual["half_size"]
    lines.extend([
        "",
        "## Counterfactual",
        "",
        f"- Hard-block recommendations: n={hard['n']}, saved losers={hard['saved_losers']}, "
        f"missed winners={hard['missed_winners']}, net delta={hard['net_delta_r_if_omitted']:+.2f}R.",
        f"- Half-size recommendations: n={half['n']}, full-size sum={half['sum_r']:+.2f}R, "
        f"delta versus full size={half['net_delta_r_vs_full_size']:+.2f}R.",
        "",
        "## Active Incidents",
        "",
    ])
    lines.extend(
        f"- `{row['severity']}` `{row['incident_type']}`: {row['n']}"
        for row in active_incidents
    )
    if not active_incidents:
        lines.append("- None.")
    lines.extend(["", "## OpenRouter Advisory Cache", ""])
    if llm_rows:
        for row in llm_rows:
            verdict = str(row.get("verdict") or "none")
            lines.append(
                f"- `{row['status']}` / `{verdict}`: n={row['n']}, "
                f"avg={row['avg_ms']}ms, max={row['max_ms']}ms"
            )
    else:
        lines.append("- No cached LLM assessments yet.")
    lines.extend(["", "## LLM Paper Experiments", ""])
    if summary["llm_experiments"]:
        for experiment, cohorts in summary["llm_experiments"].items():
            for cohort, values in cohorts.items():
                book = values["closed"]
                pf = "inf" if book["pf"] is None and book["sum_r"] > 0 else str(book["pf"])
                lines.append(
                    f"- `{experiment}` / `{cohort}`: assigned={values['assigned']}, "
                    f"closed={book['n']}, W/L={book['wins']}/{book['losses']}, "
                    f"sum={book['sum_r']:+.2f}R, PF={pf}"
                )
    else:
        lines.append("- No experiment assignments yet.")
    lines.extend(["", "## Post-Trade Diagnostics", ""])
    lines.extend(
        f"- `{row['source_book']}` / `{row['primary_category']}`: n={row['n']}, "
        f"sum={float(row['sum_r'] or 0):+.2f}R, ${float(row['sum_usdt'] or 0):+.2f}"
        for row in post_rows
    )
    if not post_rows:
        lines.append("- No diagnostics yet.")
    lines.extend([
        "",
        "## Promotion Rule",
        "",
        "No news, event, or regime agent may become an enforced live gate until matched closed "
        "outcomes show positive net delta after missed winners, acceptable false-block rate, and "
        "stable error/latency metrics. Execution sanity may only enforce objective invariants.",
        "",
    ])
    return "\n".join(lines), summary


def write_effectiveness_report(
    *, db: str | Path | None = None, output: str | Path | None = None,
    lookback_days: int = 30,
) -> dict[str, Any]:
    text, summary = build_effectiveness_report(db=db, lookback_days=lookback_days)
    target = Path(output or (load_config().root / "reports" / "QUALITY_AGENTS_EFFECTIVENESS_LATEST.md"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    json_target = target.with_suffix(".json")
    json_target.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return {"status": "OK", "report": str(target), "json": str(json_target), **summary}


__all__ = ["build_effectiveness_report", "write_effectiveness_report"]
