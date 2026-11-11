# Crypto Scalp — Telegram Noise Audit (PART 3)

**Date:** 2026-06-15 · Read-only.

## Scalp alert volume vs value

### SETUP alerts (`watchlist_alerts`, mode=scalp)

| Window | setup alerts sent | triggered | wins | losses | expired |
|---|---:|---:|---:|---:|---:|
| 48h | 77 | 45 | 7 | 4 | 34 |
| 7d | 97 | 51 | 7 | 5 | 39 |
| 14d | **152** | 77 | **7** | 9 | 61 |

### PAPER-ENTRY alerts (`signal_alerts`, alert_type=paper_entry, mode=scalp)

| Window | paper-entry alerts |
|---|---:|
| 14d | 21 |

### CLOSE alerts (scalp)

| Total close alerts (scalp, all-time) | 22 |

## The noise verdict

- **152 scalp SETUP alerts over 14 days produced 7 wins.** That is a ~5% useful-message rate. Most (61) referenced signals that triggered then expired flat; ~half never triggered at all.
- Setup-alert count (152) is **7× the paper-entry count (21)** — the setup channel is the dominant source of scalp Telegram noise.
- Setup alerts repeat per cycle for the same signal (152 alerts > 125 distinct scalp signals all-time), compounding the noise.

## Should the user receive scalp SETUP alerts at all?

**No — not as immediate Telegram trade-style messages.** They are high-volume, low-conversion, and the setup→entry→profit funnel is dominated by flat expiries. The operator cannot act on a scalp setup faster than the system paper-fills it anyway.

**Paper-entry alerts SHOULD stay** — they are the actual event ("system entered now"), low-volume (21/14d), and already carry the LOW-CONFIDENCE SCALP warning. Close alerts (22) are also low-volume and useful.

## Recommendation

Route crypto scalp SETUP alerts to **Obsidian + journal + (optional) digest** instead of immediate Telegram. Keep scalp paper-entry + close alerts on Telegram. Implemented as a notification-only change — see [CRYPTO_SCALP_ALERT_NOISE_REDUCTION_REPORT.md](CRYPTO_SCALP_ALERT_NOISE_REDUCTION_REPORT.md).
