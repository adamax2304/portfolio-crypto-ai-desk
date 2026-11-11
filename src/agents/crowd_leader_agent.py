from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.base_agent import BaseAgent
from src.models import CrowdWatchSummary
from src.utils.symbols import symbol_to_ticker
from src.utils.validation import model_to_dict


class CrowdLeaderAgent(BaseAgent):
    name = "crowd_leader_agent"

    def run(self, mentions: list[dict[str, Any]]) -> CrowdWatchSummary:
        config = self._load_yaml(self.config.root / "config" / "kol_watchlist.yaml")
        configured_sources = [
            str(item.get("name"))
            for item in config.get("sources", [])
            if isinstance(item, dict) and item.get("name")
        ]
        tracked_accounts = [
            str(item.get("name"))
            for item in config.get("tracked_accounts", [])
            if isinstance(item, dict) and item.get("name")
        ]
        manual = [item for item in mentions if item.get("type") == "manual_social_note"]
        active_signals = [
            f"{item.get('source')}: {item.get('title')} ({item.get('stance', 'unclear')})"
            for item in manual
        ][:10]
        symbols = sorted(
            {
                symbol_to_ticker(str(symbol))
                for item in manual
                for symbol in item.get("symbols", [])
                if symbol
            }
        )
        warnings = []
        if not manual:
            warnings.append("No manual KOL/crowd notes found; X/Telegram/Discord context is not live yet.")
        if tracked_accounts and tracked_accounts == ["example_account"]:
            warnings.append("KOL watchlist still contains the placeholder account; replace it with trusted sources.")

        summary = CrowdWatchSummary(
            signal_count=len(manual),
            configured_sources=configured_sources + tracked_accounts,
            active_signals=active_signals,
            symbols=symbols,
            warnings=warnings,
        )
        self.save_output(model_to_dict(summary))
        return summary

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
