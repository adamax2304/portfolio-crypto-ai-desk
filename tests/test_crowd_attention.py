from __future__ import annotations

from pathlib import Path

import yaml

from src.agents.crowd_attention_agent import CrowdAttentionAgent
from src.config import load_config
from src.data_collectors.manual_notes_loader import (
    load_manual_narrative_notes,
    load_manual_social_notes,
)
from src.models import DerivativesSummary, MomentumCandidate, SocialAttentionSummary
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


def _kit():
    config = load_config()
    return config, FileStore(config), SQLiteStore(config.db_path)


def _candidate(
    symbol: str = "SOL/USDT",
    *,
    score: float = 70,
    return_24h: float = 4.0,
    volume_ratio: float = 1.4,
    distance: float = 0.7,
) -> MomentumCandidate:
    return MomentumCandidate(
        symbol=symbol,
        direction_bias="long",
        score=score,
        return_24h=return_24h,
        return_7d=12,
        relative_strength_btc=2.0,
        volume_ratio=volume_ratio,
        atr_percentile=55,
        distance_from_ema20_atr=distance,
        reason_tags=["volume_expansion"],
    )


def test_silent_stage_when_no_attention_and_low_momentum() -> None:
    config, store, db = _kit()
    agent = CrowdAttentionAgent(config, store, db)
    candidate = _candidate(score=30, return_24h=0.5, volume_ratio=0.6)
    out = agent.run([candidate])
    assert out["SOL/USDT"].stage == "silent"


def test_euphoria_when_high_attention_and_extended_price_and_high_funding() -> None:
    config, store, db = _kit()
    agent = CrowdAttentionAgent(config, store, db)
    candidate = _candidate(score=85, return_24h=18, volume_ratio=2.0, distance=2.5)
    social = {
        "SOL/USDT": SocialAttentionSummary(
            symbol="SOL/USDT", mention_count=12, attention_score=88, sources=["Reddit"], top_mentions=[]
        )
    }
    derivatives = {
        "SOL/USDT": DerivativesSummary(
            symbol="SOL/USDT",
            data_available=True,
            funding_rate=0.0015,
            open_interest=1_000_000,
            oi_change_pct=18,
            crowding_risk="elevated",
            squeeze_potential="unknown",
            alignment_score=0.8,
            interpretation="crowded",
        )
    }
    out = agent.run([candidate], social, [], derivatives)
    assert out["SOL/USDT"].stage == "euphoria"
    assert out["SOL/USDT"].crowding_risk >= 50


def test_rumor_driven_stage_when_manual_note_is_rumor() -> None:
    config, store, db = _kit()
    agent = CrowdAttentionAgent(config, store, db)
    candidate = _candidate(score=60, return_24h=2, volume_ratio=1.2)
    manual = [
        {
            "ticker": "SOL",
            "narrative": "ecosystem",
            "source": "X / anonymous",
            "note": "rumor of partnership",
            "timestamp": "2026-05-22T08:00:00Z",
            "sentiment": "rumor",
            "confidence": "high",
            "verification": "rumor",
        }
    ]
    out = agent.run([candidate], None, manual)
    assert out["SOL/USDT"].stage == "rumor_driven"


def test_manual_notes_loader_round_trip(tmp_path: Path) -> None:
    project_root = tmp_path
    (project_root / "data" / "manual").mkdir(parents=True)
    social_yaml = project_root / "data" / "manual" / "social_notes.yaml"
    narrative_yaml = project_root / "data" / "manual" / "narrative_notes.yaml"
    social_yaml.write_text(
        yaml.safe_dump(
            {
                "notes": [
                    {
                        "ticker": "TAO",
                        "narrative": "AI",
                        "source": "X / kol",
                        "note": "fresh AI rotation",
                        "timestamp": "2026-05-22T08:00:00Z",
                        "sentiment": "bullish",
                        "confidence": "medium",
                        "verification": "single_source",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    narrative_yaml.write_text(
        yaml.safe_dump(
            {
                "notes": [
                    {
                        "narrative": "AI",
                        "stage": "growing_hype",
                        "note": "broad AI strength",
                        "confidence": "medium",
                        "timestamp": "2026-05-22T08:00:00Z",
                        "representative_symbols": ["TAO", "FET"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    social_notes = load_manual_social_notes(project_root)
    narrative_notes = load_manual_narrative_notes(project_root)
    assert len(social_notes) == 1
    assert social_notes[0]["ticker"] == "TAO"
    assert social_notes[0]["sentiment"] == "bullish"
    assert len(narrative_notes) == 1
    assert narrative_notes[0]["stage"] == "growing_hype"
    assert "TAO" in narrative_notes[0]["representative_symbols"]
