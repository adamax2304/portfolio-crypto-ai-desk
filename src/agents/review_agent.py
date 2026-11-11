from __future__ import annotations

import json

import pandas as pd

from src.agents.base_agent import BaseAgent
from src.utils.formatting import fmt_float


class ReviewAgent(BaseAgent):
    name = "review_agent"

    def run(self, market_data: dict[str, dict[str, pd.DataFrame]]) -> str:
        ideas = self.db.load_open_ideas()
        if not ideas:
            return "# Crypto AI Desk Review\n\nNo open ideas found in SQLite yet.\n"

        deduped: list[dict] = []
        seen: set[tuple[str, str]] = set()
        for idea in ideas:
            key = (str(idea["symbol"]), str(idea["direction"]))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(idea)

        lines = ["# Crypto AI Desk Review", "", "Review of saved ideas using candles that closed after idea creation.", ""]
        if len(deduped) < len(ideas):
            lines.extend(
                [
                    f"Deduped {len(ideas)} saved open/watchlist rows down to {len(deduped)} latest symbol-direction ideas.",
                    "",
                ]
            )

        for idea in deduped:
            raw = json.loads(idea["raw_json"])
            setup = raw.get("raw", {}).get("setup", {})
            symbol = idea["symbol"]
            direction = idea["direction"]
            frame = market_data.get(symbol, {}).get(setup.get("timeframe", "1h"))
            latest_price = float(frame["close"].iloc[-1]) if frame is not None and not frame.empty else None
            status = "unknown"
            notes = "No current price available."
            mfe = None
            mae = None

            if latest_price is not None:
                window = self._post_idea_window(frame, str(idea["created_at"]))
                if direction in {"long", "short"}:
                    result = self._evaluate_active_idea(idea, direction, window, latest_price)
                    status = result["status"]
                    mfe = result["mfe"]
                    mae = result["mae"]
                    notes = result["notes"]
                else:
                    status = "watchlist"
                    notes = self._watchlist_notes(idea, setup, window, latest_price)

            self.db.add_idea_check(
                int(idea["id"]),
                latest_price,
                status,
                round(mfe, 2) if mfe is not None else None,
                mae,
                notes,
            )
            lines.extend(
                [
                    f"## {symbol} - {direction}",
                    f"- Previous score: {idea['score']}/100",
                    f"- Status: {status}",
                    f"- {notes}",
                    f"- MFE: {fmt_float(mfe, 2)}% | MAE: {fmt_float(mae, 2)}%",
                    "",
                ]
            )

        output = "\n".join(lines).strip() + "\n"
        self.save_output({"reviewed": len(deduped), "open_rows_seen": len(ideas)})
        return output

    @staticmethod
    def _post_idea_window(frame: pd.DataFrame, created_at: str) -> pd.DataFrame:
        if frame is None or frame.empty:
            return pd.DataFrame()
        output = frame.copy()
        output["timestamp"] = pd.to_datetime(output["timestamp"], utc=True)
        created = pd.to_datetime(created_at, utc=True)
        return output[output["timestamp"] >= created]

    def _evaluate_active_idea(
        self,
        idea: dict,
        direction: str,
        window: pd.DataFrame,
        latest_price: float,
    ) -> dict[str, object]:
        entry_low = self._float_or_none(idea.get("entry_low"))
        entry_high = self._float_or_none(idea.get("entry_high"))
        invalidation = self._float_or_none(idea.get("invalidation"))
        tp1 = self._float_or_none(idea.get("tp1"))
        tp2 = self._float_or_none(idea.get("tp2"))
        tp3 = self._float_or_none(idea.get("tp3"))

        if window.empty or entry_low is None or entry_high is None:
            return {
                "status": "unknown",
                "mfe": None,
                "mae": None,
                "notes": f"Latest cached price: {fmt_float(latest_price)}. No closed post-idea candles yet.",
            }

        touched = self._entry_touched(direction, window, entry_low, entry_high)
        if touched.empty:
            return {
                "status": "not triggered",
                "mfe": None,
                "mae": None,
                "notes": f"Latest cached price: {fmt_float(latest_price)}. Entry zone was not touched.",
            }

        eval_window = window[window["timestamp"] >= touched["timestamp"].iloc[0]]
        entry_ref = (entry_low + entry_high) / 2
        if direction == "long":
            max_high = float(eval_window["high"].max())
            min_low = float(eval_window["low"].min())
            mfe = (max_high / entry_ref - 1) * 100
            mae = (min_low / entry_ref - 1) * 100
            hit_tp = self._highest_long_target(max_high, tp1, tp2, tp3)
            invalidated = invalidation is not None and min_low <= invalidation
        else:
            min_low = float(eval_window["low"].min())
            max_high = float(eval_window["high"].max())
            mfe = (entry_ref / min_low - 1) * 100 if min_low > 0 else None
            mae = (entry_ref / max_high - 1) * 100 if max_high > 0 else None
            hit_tp = self._highest_short_target(min_low, tp1, tp2, tp3)
            invalidated = invalidation is not None and max_high >= invalidation

        if invalidated and hit_tp:
            status = f"ambiguous: {hit_tp} and invalidation both touched"
            note_extra = "OHLC cannot tell which happened first inside the candle sequence."
        elif invalidated:
            status = "invalidated"
            note_extra = "Invalidation touched after entry."
        elif hit_tp:
            status = hit_tp
            note_extra = f"{hit_tp} touched after entry."
        else:
            status = "open"
            note_extra = "Entry touched; no target or invalidation touched yet."

        return {
            "status": status,
            "mfe": round(mfe, 2) if mfe is not None else None,
            "mae": round(mae, 2) if mae is not None else None,
            "notes": (
                f"Latest cached price: {fmt_float(latest_price)}. "
                f"Entry touched at {touched['timestamp'].iloc[0]}. {note_extra}"
            ),
        }

    def _watchlist_notes(
        self,
        idea: dict,
        setup: dict,
        window: pd.DataFrame,
        latest_price: float,
    ) -> str:
        setup_direction = setup.get("direction")
        entry_low = self._float_or_none(idea.get("entry_low"))
        entry_high = self._float_or_none(idea.get("entry_high"))
        if setup_direction not in {"long", "short"} or window.empty or entry_low is None or entry_high is None:
            return f"Latest cached price: {fmt_float(latest_price)}. No closed post-idea candles yet."
        touched = self._entry_touched(setup_direction, window, entry_low, entry_high)
        if touched.empty:
            return (
                f"Latest cached price: {fmt_float(latest_price)}. "
                "Conditional entry zone has not been touched."
            )
        return (
            f"Latest cached price: {fmt_float(latest_price)}. "
            f"Conditional entry zone touched at {touched['timestamp'].iloc[0]}, but idea remains watchlist-only."
        )

    @staticmethod
    def _entry_touched(
        direction: str, window: pd.DataFrame, entry_low: float, entry_high: float
    ) -> pd.DataFrame:
        if direction == "long":
            return window[(window["low"] <= entry_high) & (window["high"] >= entry_low)]
        return window[(window["high"] >= entry_low) & (window["low"] <= entry_high)]

    @staticmethod
    def _highest_long_target(
        max_high: float, tp1: float | None, tp2: float | None, tp3: float | None
    ) -> str | None:
        if tp3 is not None and max_high >= tp3:
            return "TP3 hit"
        if tp2 is not None and max_high >= tp2:
            return "TP2 hit"
        if tp1 is not None and max_high >= tp1:
            return "TP1 hit"
        return None

    @staticmethod
    def _highest_short_target(
        min_low: float, tp1: float | None, tp2: float | None, tp3: float | None
    ) -> str | None:
        if tp3 is not None and min_low <= tp3:
            return "TP3 hit"
        if tp2 is not None and min_low <= tp2:
            return "TP2 hit"
        if tp1 is not None and min_low <= tp1:
            return "TP1 hit"
        return None

    @staticmethod
    def _float_or_none(value: object) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None
