"""Base class for stocks agents.

Mirrors src/agents/base_agent.py but carries the stocks_config and writes
agent_runs rows with asset_class='stocks' so analytics can segregate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.stocks.configs.loader import StocksConfig
from src.utils.time import utc_now


class StocksBaseAgent:
    name = "stocks_base_agent"
    asset_class = "stocks"

    def __init__(
        self,
        config: ProjectConfig,
        stocks_config: StocksConfig,
        file_store: FileStore,
        db: SQLiteStore,
    ):
        self.config = config
        self.stocks_config = stocks_config
        self.file_store = file_store
        self.db = db

    def save_output(self, payload: dict[str, Any]) -> Path:
        stamp = utc_now().strftime("%Y%m%d_%H%M%S")
        relative = (
            Path("data")
            / "processed"
            / "agent_outputs"
            / f"{stamp}_stocks_{self.name}.json"
        )
        path = self.file_store.save_json(relative, payload)
        self.db.save_agent_run(
            self.name, str(path), payload, asset_class=self.asset_class
        )
        return path
