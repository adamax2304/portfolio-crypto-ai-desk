# Stock Swing Event RS Pullback V1 Research

> Research-only. No Paper/live/proposed_signals tables were changed.

- Run: `56ca07becee5fc7a`
- Split date: `2026-03-12`
- Local canonical stock events: `480`
- Reconstructed events: `22079`

## Data coverage

- Trade symbols loaded: `91` / `91`.
- Daily date range: `2021-09-07` to `2026-09-04`.
- SPY rows: `1255`; VIX rows: `1257`.

## Top technical variants

| Variant | Train closed | Train net | Train PF | Test closed | Test net | Test PF | Test WR | Top-symbol share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `imp050_ema21_stop15_tp20` | 41 | 232.19 | 2.4130 | 34 | 269.48 | 3.2087 | 0.6471 | 0.1090 |
| `imp050_ema21_stop15_tp15` | 41 | 244.23 | 2.7607 | 34 | 236.19 | 2.9359 | 0.6471 | 0.1038 |
| `imp050_ema21_stop12_tp20` | 41 | 193.18 | 1.9819 | 38 | 285.57 | 2.7345 | 0.5789 | 0.1016 |
| `imp050_ema21_stop12_tp15` | 41 | 235.72 | 2.6858 | 38 | 247.47 | 2.6022 | 0.6053 | 0.1020 |
| `imp025_ema21_stop15_tp20` | 116 | 459.27 | 1.8439 | 70 | 289.66 | 1.9540 | 0.5429 | 0.0857 |
| `imp035_ema21_stop15_tp20` | 91 | 388.29 | 1.9367 | 62 | 253.35 | 1.9295 | 0.5484 | 0.0966 |
| `imp035_fib618_stop15_tp20` | 147 | 740.58 | 2.0988 | 85 | 283.61 | 1.7658 | 0.5176 | 0.0743 |
| `imp035_ema21_stop12_tp15` | 97 | 347.21 | 1.8114 | 66 | 225.55 | 1.7647 | 0.5455 | 0.1027 |
| `imp025_ema21_stop15_tp15` | 117 | 475.30 | 1.9869 | 70 | 231.51 | 1.7633 | 0.5571 | 0.0885 |
| `imp050_fib50_stop12_tp20` | 85 | 358.89 | 1.8408 | 59 | 227.67 | 1.7590 | 0.5085 | 0.0863 |
| `imp050_hybrid_stop12_tp20` | 93 | 349.75 | 1.7232 | 63 | 234.48 | 1.7420 | 0.5079 | 0.0827 |
| `imp035_ema21_stop15_tp15` | 92 | 408.18 | 2.1244 | 62 | 201.13 | 1.7379 | 0.5484 | 0.0999 |

## News and ablation

| Phase / scope | Variant | Closed | Net USD | PF | WR | Max DD | Avg hold |
|---|---|---:|---:|---:|---:|---:|---:|
| `ablation/no_recent_positive_news` | `imp025_ema21_stop15_tp20` | 180 | 752.97 | 1.9271 | 0.5222 | 67.51 | 15.56 |
| `ablation/positive_news_recent` | `imp025_ema21_stop15_tp20` | 6 | -4.0432 | 0.8868 | 0.3333 | 20.38 | 5.3300 |
| `ablation/no_recent_positive_news` | `imp035_ema21_stop12_tp15` | 157 | 572.84 | 1.8337 | 0.5414 | 71.84 | 12.75 |
| `ablation/positive_news_recent` | `imp035_ema21_stop12_tp15` | 6 | -0.0852 | 0.9976 | 0.3333 | 20.41 | 5.1700 |
| `ablation/no_recent_positive_news` | `imp035_ema21_stop15_tp20` | 147 | 645.69 | 1.9913 | 0.5306 | 82.99 | 15.59 |
| `ablation/positive_news_recent` | `imp035_ema21_stop15_tp20` | 6 | -4.0432 | 0.8868 | 0.3333 | 20.38 | 5.3300 |
| `ablation/no_recent_positive_news` | `imp035_fib618_stop15_tp20` | 226 | 1044.26 | 2.0322 | 0.5310 | 58.83 | 15.79 |
| `ablation/positive_news_recent` | `imp035_fib618_stop15_tp20` | 6 | -20.07 | 0.3849 | 0.1667 | 32.64 | 6.5000 |
| `ablation/no_recent_positive_news` | `imp050_ema21_stop12_tp15` | 75 | 467.86 | 2.7079 | 0.6267 | 38.55 | 13.40 |
| `ablation/positive_news_recent` | `imp050_ema21_stop12_tp15` | 4 | 15.32 | 1.7534 | 0.5000 | 10.19 | 6.0000 |
| `ablation/no_recent_positive_news` | `imp050_ema21_stop12_tp20` | 75 | 460.16 | 2.3492 | 0.5333 | 38.55 | 14.31 |
| `ablation/positive_news_recent` | `imp050_ema21_stop12_tp20` | 4 | 18.59 | 1.9140 | 0.5000 | 10.19 | 6.0000 |
| `ablation/no_recent_positive_news` | `imp050_ema21_stop15_tp15` | 71 | 470.39 | 2.9567 | 0.6479 | 38.49 | 15.23 |
| `ablation/positive_news_recent` | `imp050_ema21_stop15_tp15` | 4 | 10.03 | 1.4937 | 0.5000 | 10.19 | 6.2500 |
| `ablation/no_recent_positive_news` | `imp050_ema21_stop15_tp20` | 71 | 490.31 | 2.8431 | 0.6056 | 38.49 | 16.00 |
| `ablation/positive_news_recent` | `imp050_ema21_stop15_tp20` | 4 | 11.36 | 1.5590 | 0.5000 | 10.19 | 6.2500 |
| `local_real_news/all` | `imp025_ema21_stop15_tp20` | 4 | 4.1188 | 1.2021 | 0.5000 | 20.38 | 4.5000 |
| `local_real_news/all` | `imp035_ema21_stop12_tp15` | 4 | 6.6878 | 1.3277 | 0.5000 | 20.41 | 4.2500 |
| `local_real_news/all` | `imp035_ema21_stop15_tp20` | 4 | 4.1188 | 1.2021 | 0.5000 | 20.38 | 4.5000 |
| `local_real_news/all` | `imp035_fib618_stop15_tp20` | 8 | -12.76 | 0.5536 | 0.2500 | 28.00 | 7.6200 |
| `local_real_news/all` | `imp050_ema21_stop12_tp15` | 2 | 5.4588 | 1.5378 | 0.5000 | 10.15 | 4.0000 |
| `local_real_news/all` | `imp050_ema21_stop12_tp20` | 2 | 7.4574 | 1.7347 | 0.5000 | 10.15 | 4.0000 |
| `local_real_news/all` | `imp050_ema21_stop15_tp15` | 2 | 3.5605 | 1.3516 | 0.5000 | 10.13 | 4.5000 |
| `local_real_news/all` | `imp050_ema21_stop15_tp20` | 2 | 2.8898 | 1.2854 | 0.5000 | 10.13 | 4.5000 |
| `reconstructed_news/all` | `imp025_ema21_stop15_tp20` | 17 | 64.23 | 2.2577 | 0.7059 | 10.26 | 12.12 |
| `reconstructed_news/all` | `imp035_ema21_stop12_tp15` | 19 | 51.03 | 1.7154 | 0.6316 | 20.40 | 10.53 |
| `reconstructed_news/all` | `imp035_ema21_stop15_tp20` | 17 | 64.23 | 2.2577 | 0.7059 | 10.26 | 12.12 |
| `reconstructed_news/all` | `imp035_fib618_stop15_tp20` | 27 | 18.39 | 1.1871 | 0.5185 | 32.86 | 15.48 |
| `reconstructed_news/all` | `imp050_ema21_stop12_tp15` | 15 | 53.23 | 2.0458 | 0.6667 | 20.11 | 10.33 |
| `reconstructed_news/all` | `imp050_ema21_stop12_tp20` | 15 | 59.26 | 2.1642 | 0.6667 | 20.11 | 12.00 |
| `reconstructed_news/all` | `imp050_ema21_stop15_tp15` | 13 | 59.48 | 2.9411 | 0.7692 | 10.24 | 11.69 |
| `reconstructed_news/all` | `imp050_ema21_stop15_tp20` | 13 | 74.62 | 3.4352 | 0.7692 | 10.24 | 13.38 |
| `technical_skeleton/all` | `imp025_ema21_stop15_tp20` | 186 | 748.92 | 1.8833 | 0.5161 | 67.51 | 15.23 |
| `technical_skeleton/all` | `imp035_ema21_stop12_tp15` | 163 | 572.76 | 1.7923 | 0.5337 | 82.10 | 12.47 |
| `technical_skeleton/all` | `imp035_ema21_stop15_tp20` | 153 | 641.64 | 1.9339 | 0.5229 | 88.14 | 15.18 |
| `technical_skeleton/all` | `imp035_fib618_stop15_tp20` | 232 | 1024.19 | 1.9807 | 0.5216 | 58.83 | 15.55 |
| `technical_skeleton/all` | `imp050_ema21_stop12_tp15` | 79 | 483.19 | 2.6419 | 0.6203 | 38.55 | 13.03 |
| `technical_skeleton/all` | `imp050_ema21_stop12_tp20` | 79 | 478.75 | 2.3247 | 0.5316 | 38.55 | 13.89 |
| `technical_skeleton/all` | `imp050_ema21_stop15_tp15` | 75 | 480.42 | 2.8427 | 0.6400 | 38.49 | 14.75 |
| `technical_skeleton/all` | `imp050_ema21_stop15_tp20` | 75 | 501.67 | 2.7520 | 0.6000 | 38.49 | 15.48 |

## Recommendation

- Verdict: **PAPER_CANARY**.
- Candidate variant: `imp050_ema21_stop15_tp20`.
- Reason: Use technical skeleton as the entry engine; use news as score boost/blocker until the real-news sample reaches the configured minimum.

Paper V1 settings if enabled:

- Long-only.
- Entry mode: `EVENT_RS_PULLBACK`.
- Risk: `$10` full size, `$5` neutral/risk-reduced.
- Stop: structural pullback low/Fib invalidation plus ATR buffer; no artificial tight stop.
- News: canonical events are used point-in-time by `available_at`; reconstructed news is research-only.
- Live: disabled until at least 30 clean Paper closes.

Recommended Paper layout:

- Quality sleeve, 1x: `imp050_ema21_stop15_tp20`: impulse >= 5.0%, impulse >= 1.25 ATR, volume ratio >= 1.2, RS20 vs SPY >= 0.02, sector RS >= 0.00, pullback `ema21`, min stop 1.5 ATR, max stop 2.8 ATR / 15%, TP 2.0R/3.0R/runner, max hold 25d.
- Flow sleeve, 0.5x: `imp025_ema21_stop15_tp20`: impulse >= 2.5%, impulse >= 1.00 ATR, volume ratio >= 1.0, RS20 vs SPY >= 0.00, sector RS >= -0.03, pullback `ema21`, min stop 1.5 ATR, max stop 2.8 ATR / 15%, TP 2.0R/3.0R/runner, max hold 25d.
- Do not require a catalyst yet. Positive causal news may boost tier; negative legal/dilution/delisting/calendar-risk news blocks or downgrades.
- Record every candidate, rejected setup, news item `published_at/ingested_at/available_at`, impulse anchor, entry level, stop basis, MFE/MAE, and exit reason.