from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore
from src.utils.time import utc_now


class BaseAgent:
    name = "base_agent"

    def __init__(self, config: ProjectConfig, file_store: FileStore, db: SQLiteStore):
        self.config = config
        self.file_store = file_store
        self.db = db

    def save_output(self, payload: dict[str, Any]) -> Path:
        stamp = utc_now().strftime("%Y%m%d_%H%M%S")
        relative = Path("data") / "processed" / "agent_outputs" / f"{stamp}_{self.name}.json"
        path = self.file_store.save_json(relative, payload)
        self.db.save_agent_run(self.name, str(path), payload)
        return path
