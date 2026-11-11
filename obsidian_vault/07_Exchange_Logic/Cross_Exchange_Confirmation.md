# Cross-Exchange Confirmation

`ExchangeFusionAgent` computes per-symbol confirmation. The output is a key driver of `data_confidence` and trade scoring caps.

## Confirmation score (0–100)

Base 30, plus:

- +30 if anchor (binance) listed.
- +20 if derivatives venue (bybit) listed.
- +8 if discovery venue (mexc) listed and not high-risk-only.
- +10 if listed on ≥3 venues; +5 if ≥2.
- +10 × price_consistency (0..1).
- +6 × volume_consistency (0..1).
- Min(score, 55) if `high_risk_only` is True.

Clamped 0..100.

## Price / volume consistency

```python
spread = max(values) - min(values)
rel = abs(spread) / max(abs(avg), tolerance)
consistency = clamp(1.0 - min(rel, 1.5), 0.0, 1.0)
```

- `price_consistency < 0.5` → `price_divergence_across_exchanges` risk flag.
- `volume_consistency` is informational; not gated.

## Suggested focus exchange

`_pick_focus_exchange`:

1. anchor if listed.
2. derivative venue (e.g. bybit).
3. any non-high-risk venue.
4. any venue.

## What goes into trade idea

`TradeIdea.exchange_focus = confirmation.suggested_exchange_focus` and `exchanges_confirmed = confirmation.exchanges_listed`. These are surfaced in the report and in Telegram alerts.

## Operator rules

- Trade on `suggested_exchange_focus`. Trading on a different venue means you're not matching the structure the desk read.
- `confirmation_score ≥ 70` is healthy.
- `confirmation_score < 50` means thin confirmation — reduce size.
- `price_divergence_across_exchanges` flag is a clear "do not chase" signal; one venue is lagging or being manipulated.

## Related

- [[Exchange_Overview]]
- [[Exchange_Fusion_Agent]]
- [[Score_Caps]]
- [[Exchange_Data_Confidence]]

## Implemented status

- **Implemented**.
