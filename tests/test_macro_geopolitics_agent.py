from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from src.agents.macro_geopolitics_agent import MacroGeopoliticsAgent


NOW = datetime(2026, 7, 14, 15, 30, tzinfo=timezone.utc)
KEYWORDS = {
    "risk_off": ["war", "attack", "blockade", "strait of hormuz", "missile"],
    "risk_on": ["rate cut", "dovish"],
    "neutral_watch": ["fed", "cpi", "oil"],
}


class _DB:
    def __init__(self, path):
        self.path = path

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn


def _agent(tmp_path, monkeypatch):
    path = str(tmp_path / "macro.sqlite")
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE news_canonical_events (title TEXT,source TEXT,published_at TEXT,event_type TEXT,"
        "source_quality TEXT,confidence REAL,risk_action TEXT,corroboration_count INTEGER,"
        "independent_non_social_count INTEGER,expires_at TEXT,is_cluster_primary INTEGER)"
    )
    conn.commit(); conn.close()
    cfg = SimpleNamespace(sources={"macro_keywords": KEYWORDS})
    agent = MacroGeopoliticsAgent(cfg, None, _DB(path))
    monkeypatch.setattr(agent, "save_output", lambda payload: None)
    return agent, path


def _insert(path, *, title, source="Reuters", quality="reputable", event_type="geopolitical_risk",
            risk_action="risk_warning", published_at=None, expires_at=None):
    published_at = published_at or (NOW - timedelta(minutes=10)).isoformat()
    expires_at = expires_at or (NOW + timedelta(hours=6)).isoformat()
    conn = sqlite3.connect(path)
    conn.execute(
        "INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?,?,?,?,1)",
        (title, source, published_at, event_type, quality, 0.8, risk_action, 2, 1, expires_at),
    )
    conn.commit(); conn.close()


def test_fresh_canonical_geopolitical_event_outranks_generic_top_news(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    _insert(path, title="Iran blockade escalates at Strait of Hormuz after missile attack")
    news = {"top_news": [{"title": "Routine crypto product update", "source": "Blog",
                           "published_at": NOW.isoformat()}]}

    out = agent.run(news, now=NOW)

    assert out.headlines[0].startswith("Iran blockade")
    assert out.risk_score >= 65
    assert out.btc_bias == "risk-off headwind"
    assert "geopolitical_risk" in out.themes
    assert "canonical event" in out.explanation


def test_expired_canonical_event_is_not_selected(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    _insert(path, title="Old war headline", published_at=(NOW - timedelta(hours=13)).isoformat(),
            expires_at=(NOW - timedelta(hours=1)).isoformat())

    out = agent.run({"top_news": []}, now=NOW)

    assert out.headlines == []
    assert out.risk_score == 25
    assert "No macro/geopolitical" in out.warnings[0]


def test_duplicate_social_relay_cannot_create_high_risk_by_itself(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    for _ in range(12):
        _insert(path, title="Iran blockade at Strait of Hormuz", source="t.me/Relay",
                quality="social", event_type="macro_headline", risk_action="none")

    out = agent.run({"top_news": []}, now=NOW)

    assert len(out.headlines) == 1
    assert out.risk_score < 65


def test_differently_worded_same_hour_relay_keeps_best_source(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    _insert(path, title="Trump announces blockade at Strait of Hormuz", source="t.me/Relay",
            quality="social")
    _insert(path, title="Shipping halted as Iran Hormuz blockade expands", source="Reuters",
            quality="reputable")

    out = agent.run({"top_news": []}, now=NOW)

    blockade = [h for h in out.headlines if "blockade" in h.lower()]
    assert blockade == ["Shipping halted as Iran Hormuz blockade expands"]


def test_warsh_name_is_not_a_war_keyword_and_cooling_inflation_is_risk_on(tmp_path, monkeypatch):
    agent, _ = _agent(tmp_path, monkeypatch)
    news = {"top_news": [
        {"title": "Warsh speaks to Congress", "source": "CNBC",
         "published_at": NOW.isoformat()},
        {"title": "US inflation cools below expectations", "source": "Reuters",
         "published_at": NOW.isoformat()},
    ]}

    out = agent.run(news, now=NOW)

    assert "war" not in out.themes
    assert "disinflation" in out.themes
    assert out.risk_score < 30


def test_corporate_war_metaphor_is_not_selected_as_geopolitical(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    _insert(path, title="Business declares war on Pentagon stock buyback and dividend restrictions")

    out = agent.run({"top_news": []}, now=NOW)

    assert out.headlines == []


def test_gaming_attack_product_language_is_not_geopolitical(tmp_path, monkeypatch):
    agent, _ = _agent(tmp_path, monkeypatch)
    news = {"top_news": [{
        "title": "New gaming keyboard launches rapid attack mode",
        "source": "Company blog", "published_at": NOW.isoformat(),
    }]}

    out = agent.run(news, now=NOW)

    assert out.headlines == []
    assert out.risk_score == 25


def test_war_college_and_corporate_oil_day_are_not_macro_evidence(tmp_path, monkeypatch):
    agent, path = _agent(tmp_path, monkeypatch)
    _insert(path, title="Defense innovation report released at U.S. Army War College",
            source="PR Newswire", quality="company_pr")
    _insert(path, title="Retail portfolio grows after July Oil Day sales event",
            source="PR Newswire", quality="company_pr", event_type="macro_headline")

    out = agent.run({"top_news": []}, now=NOW)

    assert out.headlines == []
    assert out.risk_score == 25


def test_lowest_cpi_and_soft_inflation_are_directionally_risk_on(tmp_path, monkeypatch):
    agent, _ = _agent(tmp_path, monkeypatch)
    news = {"top_news": [
        {"title": "US CPI reaches its lowest level since 2020", "source": "Reuters",
         "published_at": NOW.isoformat()},
        {"title": "Markets rise after soft inflation data", "source": "CNBC",
         "published_at": NOW.isoformat()},
    ]}

    out = agent.run(news, now=NOW)

    assert "disinflation" in out.themes
    assert "inflation" not in out.themes
    assert out.risk_score < 25
