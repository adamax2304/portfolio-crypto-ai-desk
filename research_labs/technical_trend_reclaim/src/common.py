from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import yaml


LAB_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = LAB_ROOT / "research.sqlite"


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else stable_json(value).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parameter_grid(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    dimensions = cfg.get("parameter_dimensions") or {}
    keys = list(dimensions)
    values = [list(dimensions[key] or []) for key in keys]
    rows: list[dict[str, Any]] = []
    for index, combo in enumerate(itertools.product(*values), start=1):
        row = {key: value for key, value in zip(keys, combo)}
        row["variant_id"] = f"v{index:02d}"
        row["parameter_hash"] = digest(row)
        rows.append(row)
    return rows


def archive_path(source: str = "binance", timeframe: str = "15m", symbol: str | None = None,
                 *, root: str | Path | None = None) -> Path:
    base = Path(root) if root else PROJECT_ROOT / "data" / "history" / "ohlcv" / source / timeframe
    if symbol is None:
        return base
    return base / f"{symbol.replace('/', '_').upper()}.csv"


def load_symbols_from_project() -> tuple[list[str], list[str]]:
    config_path = PROJECT_ROOT / "config" / "crypto_invest_universe.yaml"
    if config_path.exists():
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        selected = (payload.get("crypto_invest_universe") or {}).get("selected_symbols") or []
        crypto = [str(value).strip().upper() for value in selected if str(value).strip()]
        if crypto:
            return crypto, []
    folder = archive_path("binance", "15m")
    crypto = sorted(path.stem.replace("_", "/") for path in folder.glob("*_USDT.csv"))
    return crypto, []

