# REGIME UNKNOWN FIX — REPORT (PART 8)

**Scope:** trading-desk-control read-model. Date: 2026-06-24. PAPER/display.

## Root cause
`proposed_signals.market_regime` is **free text** from the detector/LLM. Distribution:
`bullish` 1235, `chop` 256, **`''` empty 223**, `risk_off` 222, `bullish trend` 215,
`risk_on` 126, `bearish trend` 42, `range/chop` 33, `transition` 15,
`high-volatility danger` 3. The app showed **"unknown"** for the empty string and any
value it couldn't map → most "unknown" were the 223 empty rows + unmapped free-text, not
genuinely missing data.

## Fix
`backend/app/regime.py → normalize_regime(raw)` maps free-text → a canonical enum with a
readable label, source, and confidence:
`trend_up · trend_down · range · chop · transition · risk_off · risk_on ·
high_volatility · unknown`. Substring rules (first-match): `bearish trend→trend_down`,
`bullish→trend_up`, `range/chop→range`, `high-volatility danger→high_volatility`, etc.
**"unknown" only when the field is genuinely empty** (`source:none`); unmapped non-empty
text → unknown with low confidence + reason so it's diagnosable.

Wired into the lifecycle read-model (`regime` object: regime, label, source, confidence,
reason). Trade detail now shows the readable label (e.g. ETH short → **Trend ↓**,
MSTR → **Chop**) instead of "unknown".

## Tests
`backend/tests/test_execution_ui.py`: empty→unknown(source none); bullish→trend_up;
bearish trend→trend_down; range/chop→range; high-volatility danger→high_volatility;
unmapped→unknown low-confidence.

## Verdict
**REGIME_UNKNOWN_REDUCED_AND_EXPLAINED**
