"""Entity-alias matcher — maps news headlines / titles to crypto tickers.

Driven by ``config/crypto_entity_aliases.yaml``. The matcher honours the
false-positive safety rules:

* Aliases that are ALL UPPERCASE and ≤ 4 chars are matched
  **case-sensitively** (`re.search` without `IGNORECASE`). This means
  common English words like "near", "one", "link", "flow" do NOT
  collide with their tickers; only an explicit uppercase "NEAR" /
  "ONE" / "LINK" / "FLOW" hits.
* Aliases with a space OR length ≥ 5 are matched **case-insensitively**
  ("Bitcoin", "Binance Coin", "Cardano").
* Longer aliases are tried before shorter ones, so "BNB Chain" wins
  over a bare "BNB" when both could match — only one ticker emitted
  either way, but the longer match is recorded first.

The matcher is **pure-string**. No HTTP, no LLM, no I/O beyond the
one-time YAML load.

Public API:

    matcher = EntityAliasMatcher.load(project_root)
    matcher.detect("BNB Chain exploit drains $7.3M from DxSale")
    # → ['BNB/USDT']

    matcher.detect("Cardano Foundation cancels annual conference")
    # → ['ADA/USDT']

    matcher.detect("Stay near the entry zone")
    # → []   (lowercase 'near' does NOT trigger NEAR)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class EntityAlias:
    """One compiled alias pattern bound to its ticker."""

    ticker: str
    alias: str
    pattern: re.Pattern[str]
    case_sensitive: bool


@dataclass
class EntityAliasMatcher:
    """Compiled set of crypto entity aliases.

    Use :py:meth:`load` to construct from the project's YAML file or
    :py:meth:`from_dict` for tests.
    """

    by_ticker: dict[str, dict[str, Any]] = field(default_factory=dict)
    _compiled: list[EntityAlias] = field(default_factory=list)

    # PART 19 — `suffix` lets the same matcher serve both crypto (where the
    # legacy contract appends ``/USDT`` to every returned ticker so the
    # caller can match symbols stored in ``BTC/USDT`` form) and stocks
    # (bare tickers — ``SMCI``, ``AAPL`` — with no suffix).
    suffix: str = "/USDT"

    @classmethod
    def load(cls, project_root: Path) -> "EntityAliasMatcher":
        return cls._load_yaml(
            Path(project_root) / "config" / "crypto_entity_aliases.yaml",
            suffix="/USDT",
        )

    @classmethod
    def load_stocks(cls, project_root: Path) -> "EntityAliasMatcher":
        """PART 19 — load the stocks entity-alias YAML (bare tickers)."""
        return cls._load_yaml(
            Path(project_root) / "config" / "stocks_entity_aliases.yaml",
            suffix="",
        )

    @classmethod
    def _load_yaml(cls, config_path: Path, *, suffix: str) -> "EntityAliasMatcher":
        if not config_path.exists():
            return cls(suffix=suffix)
        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return cls(suffix=suffix)
        if not isinstance(data, dict):
            return cls(suffix=suffix)
        out = cls.from_dict(data)
        out.suffix = suffix
        return out

    @classmethod
    def from_dict(cls, mapping: dict[str, dict[str, Any]]) -> "EntityAliasMatcher":
        compiled: list[EntityAlias] = []
        normalized: dict[str, dict[str, Any]] = {}
        for ticker, info in mapping.items():
            ticker_norm = str(ticker).strip().upper()
            if not ticker_norm:
                continue
            info = info or {}
            aliases = list(info.get("aliases") or [])
            normalized[ticker_norm] = {
                "canonical_name": info.get("canonical_name", ticker_norm),
                "aliases": aliases,
                # Opt-in resolver-only aliases.  They are intentionally not
                # compiled into the general text matcher: the news resolver
                # applies them only to vetted stock headlines.
                "headline_aliases": list(info.get("headline_aliases") or []),
                "headline_context_terms": list(info.get("headline_context_terms") or []),
                "tags": list(info.get("tags") or []),
            }
            for alias in aliases:
                a = str(alias).strip()
                if not a:
                    continue
                case_sensitive = _is_strict_ticker(a)
                pattern = _compile_alias(a, case_sensitive=case_sensitive)
                compiled.append(EntityAlias(
                    ticker=ticker_norm,
                    alias=a,
                    pattern=pattern,
                    case_sensitive=case_sensitive,
                ))
        # Sort by alias length descending so longer phrases beat short
        # ones on greedy first-pass (irrelevant for set output but
        # keeps the audit log readable when we record the WINNING alias).
        compiled.sort(key=lambda e: -len(e.alias))
        return cls(by_ticker=normalized, _compiled=compiled)

    def detect(self, text: str, *, return_pairs: bool = False) -> list[str]:
        """Return tickers (with `/USDT` suffix) found in *text*.

        Order: deterministic — sorted alphabetically. Each ticker
        appears once regardless of how many aliases matched.
        """

        if not text or not self._compiled:
            return []
        hits: dict[str, str] = {}
        for entry in self._compiled:
            if entry.ticker in hits:
                continue
            try:
                if entry.pattern.search(text):
                    hits[entry.ticker] = entry.alias
            except re.error:
                continue
        if return_pairs:
            return [
                (f"{t}{self.suffix}", alias) for t, alias in sorted(hits.items())
            ]
        return [f"{t}{self.suffix}" for t in sorted(hits.keys())]

    def tags_for(self, ticker: str) -> list[str]:
        """Sector / narrative tags configured for a ticker."""

        t = ticker.upper().split("/")[0]
        info = self.by_ticker.get(t, {})
        return list(info.get("tags") or [])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


# Aliases we explicitly REFUSE to match case-insensitively because the
# token doubles as an everyday English word. They MUST appear as the
# exact uppercase ticker.
_COMMON_WORD_STRICTS = frozenset({
    "NEAR", "ONE", "LINK", "FLOW", "ANY", "PEN", "FOR", "SUN", "RUN",
    "ARB", "OP", "AAVE", "INJ", "ADA",
})


def _is_strict_ticker(alias: str) -> bool:
    """Return True iff *alias* should be matched case-sensitively.

    Rules (in order):
    1. Multi-word alias → always case-insensitive (returns False).
    2. Length ≥ 5 → case-insensitive (returns False).
    3. Otherwise (short, single-word) → case-sensitive (returns True).

    The strict path catches all ≤4-char tickers (BTC, ETH, BNB, ADA,
    SUI, …) so that "near", "ada", "btc" inside lowercase prose does
    NOT trigger a hit; only "NEAR", "ADA", "BTC" as proper tickers do.
    """

    if " " in alias:
        return False
    if len(alias) >= 5:
        return False
    return True


def _compile_alias(alias: str, *, case_sensitive: bool) -> re.Pattern[str]:
    """Word-boundary regex for one alias.

    * Embedded dots (e.g. "Fetch.ai") are escaped and then preserved.
    * Spaces become `\\s+` so "BNB Chain" matches "BNB  Chain" (double
      space) and "BNB\\tChain".
    """

    escaped = re.escape(alias).replace(r"\ ", r"\s+")
    # Build word-boundary pattern. \b doesn't work well for tokens that
    # END in punctuation, so we use a custom boundary that accepts
    # start/end of string OR non-alphanumeric neighbours.
    pattern = rf"(?:(?<=^)|(?<=[^A-Za-z0-9]))" + escaped + r"(?:(?=$)|(?=[^A-Za-z0-9]))"
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(pattern, flags)


@lru_cache(maxsize=4)
def get_matcher(project_root: str) -> EntityAliasMatcher:
    """Cached factory for the crypto matcher (production callers)."""

    return EntityAliasMatcher.load(Path(project_root))


@lru_cache(maxsize=4)
def get_stocks_matcher(project_root: str) -> EntityAliasMatcher:
    """PART 19 — cached factory for the stocks entity matcher.

    Returns bare tickers (``SMCI``, ``AAPL``, ...) — no suffix — so the
    output drops straight into the stocks news pipelines which already
    use bare tickers in ``detected_symbols``.
    """

    return EntityAliasMatcher.load_stocks(Path(project_root))
