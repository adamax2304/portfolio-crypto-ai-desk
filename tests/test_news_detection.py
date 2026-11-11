from __future__ import annotations

from src.data_collectors.rss_news_collector import RSSNewsCollector
from src.data_collectors.social_collector import SocialCollector


def test_ticker_detection_avoids_plain_word_substrings() -> None:
    assert not RSSNewsCollector._mentions_ticker("price is near local resistance", "NEAR")
    assert not RSSNewsCollector._mentions_ticker("open this link for the chart", "LINK")
    assert not RSSNewsCollector._mentions_ticker("confidentially submits IPO filing", "SUI")
    assert RSSNewsCollector._mentions_ticker("$NEAR breaks out on volume", "NEAR")
    assert RSSNewsCollector._mentions_ticker("NEAR/USDT breaks out on volume", "NEAR")
    assert RSSNewsCollector._mentions_ticker("$SUI sees fresh flows", "SUI")


def test_social_ticker_detection_treats_ambiguous_words_carefully() -> None:
    assert not SocialCollector._mentions_ticker("near-term price action looks bad", "NEAR")
    assert not SocialCollector._mentions_ticker("drop your link below", "LINK")
    assert SocialCollector._mentions_ticker("$LINK getting discussed", "LINK")
    assert SocialCollector._mentions_ticker("BTC is the main topic", "BTC")
