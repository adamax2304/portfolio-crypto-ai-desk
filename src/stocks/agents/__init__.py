"""Stocks-specific agents. Mirror the layout of src/agents but stock-aware.

Stage 4 deliverables. The Supervisor wiring lives in Stage 5.
"""

from src.stocks.agents.base import StocksBaseAgent
from src.stocks.agents.company_news_agent import CompanyNewsAgent, StockNewsHit
from src.stocks.agents.earnings_risk_agent import EarningsRisk, EarningsRiskAgent
from src.stocks.agents.market_regime_agent import (
    IndexSnapshot,
    StocksMarketRegimeAgent,
    StocksRegime,
)
from src.stocks.agents.relative_strength_agent import (
    RSSnapshot,
    StockRelativeStrengthAgent,
)
from src.stocks.agents.risk_agent import StockRiskAgent, StockRiskAssessment
from src.stocks.agents.scoring_agent import StockScore, StockScoringAgent
from src.stocks.agents.sector_rotation_agent import SectorRotationAgent, SectorSnapshot
from src.stocks.agents.technical_agent import StockTechnicalAgent, TechnicalSetup
from src.stocks.agents.trade_idea_agent import StockTradeIdeaAgent

__all__ = [
    "StocksBaseAgent",
    "StocksMarketRegimeAgent",
    "StocksRegime",
    "IndexSnapshot",
    "SectorRotationAgent",
    "SectorSnapshot",
    "StockRelativeStrengthAgent",
    "RSSnapshot",
    "EarningsRiskAgent",
    "EarningsRisk",
    "CompanyNewsAgent",
    "StockNewsHit",
    "StockTechnicalAgent",
    "TechnicalSetup",
    "StockRiskAgent",
    "StockRiskAssessment",
    "StockScoringAgent",
    "StockScore",
    "StockTradeIdeaAgent",
]
