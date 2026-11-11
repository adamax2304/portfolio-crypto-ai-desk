"""Idempotently copy canonical intelligence tables out of the trading DB."""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from src.config import load_config
from src.data_collectors import market_intelligence_store as mi


TABLES = (
    "derivative_snapshots",
    "funding_rate_events",
    "liquidation_events",
    "intelligence_source_health",
    "asset_contract_registry",
    "onchain_metric_snapshots",
    "token_security_snapshots",
    "holder_concentration_snapshots",
    "wallet_flow_events",
)


def migrate(source: str | Path | None = None, target: str | Path | None = None) -> dict:
    source_path = Path(source or load_config().db_path).resolve()
    target_path = Path(target or mi.default_db_path()).resolve()
    if source_path == target_path:
        raise ValueError("source and target intelligence databases must differ")
    result = {"source": str(source_path), "target": str(target_path), "tables": {}}
    with mi.connect(target_path) as conn:
        conn.execute("ATTACH DATABASE ? AS legacy", (str(source_path),))
        try:
            source_tables = {r[0] for r in conn.execute(
                "SELECT name FROM legacy.sqlite_master WHERE type='table'"
            ).fetchall()}
            for table in TABLES:
                before = conn.execute(f"SELECT COUNT(*) FROM main.{table}").fetchone()[0]
                if table not in source_tables:
                    result["tables"][table] = {"before": before, "after": before, "copied": 0}
                    continue
                source_cols = [r[1] for r in conn.execute(f"PRAGMA legacy.table_info({table})")]
                target_cols = {r[1] for r in conn.execute(f"PRAGMA main.table_info({table})")}
                cols = [col for col in source_cols if col in target_cols]
                if not cols:
                    continue
                names = ",".join(f'"{col}"' for col in cols)
                verb = "INSERT OR REPLACE" if table == "intelligence_source_health" else "INSERT OR IGNORE"
                conn.execute(
                    f"{verb} INTO main.{table}({names}) SELECT {names} FROM legacy.{table}"
                )
                after = conn.execute(f"SELECT COUNT(*) FROM main.{table}").fetchone()[0]
                result["tables"][table] = {
                    "before": before, "after": after, "copied": max(0, after - before)
                }
            conn.commit()
        finally:
            conn.execute("DETACH DATABASE legacy")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--target")
    args = parser.parse_args()
    result = migrate(args.source, args.target)
    print(f"source={result['source']}")
    print(f"target={result['target']}")
    for table, stats in result["tables"].items():
        print(f"{table}: {stats}")


if __name__ == "__main__":
    main()
