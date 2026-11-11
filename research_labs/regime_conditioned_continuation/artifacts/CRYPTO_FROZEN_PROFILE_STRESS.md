# Frozen crypto profile: execution-cost stress

Profile: `v01` / `cf89424a1ef4143655eb5a500ef907fdd85b4e7cf88772a5f8c5e11b0413c1cf`.
The historical simulator stored 15 bps slippage. The table below holds fills,
fees and funding fixed and restates net USD at 10/15/20/25 bps. This is a cost
sensitivity diagnostic, not a new parameter search.

| Stage | Direction | Trades | 10 bps net/PF | 15 bps net/PF | 20 bps net/PF | 25 bps net/PF |
|---|---:|---:|---:|---:|---:|---:|
| Development | all | 58 | +$352.86 / 1.749 | +$172.83 / 1.307 | -$7.19 / 0.989 | -$187.22 / 0.757 |
| Development | long | 37 | +$187.48 / 1.573 | +$71.13 / 1.184 | -$45.22 / 0.901 | -$161.58 / 0.693 |
| Development | short | 21 | +$165.38 / 2.151 | +$101.71 / 1.576 | +$38.03 / 1.181 | -$25.64 / 0.894 |
| Validation | all | 31 | +$315.31 / 3.087 | +$220.11 / 2.163 | +$124.92 / 1.533 | +$29.72 / 1.106 |
| Validation | long | 20 | +$105.51 / 1.734 | +$41.29 / 1.235 | -$22.94 / 0.892 | -$87.16 / 0.648 |
| Validation | short | 11 | +$209.80 / 30.079 | +$178.83 / 14.370 | +$147.85 / 7.587 | +$116.88 / 4.457 |
| Known audit | all | 49 | +$736.50 / 5.538 | +$556.27 / 3.621 | +$376.04 / 2.355 | +$195.81 / 1.546 |
| Known audit | long | 15 | -$24.17 / 0.768 | -$81.75 / 0.380 | -$139.33 / 0.168 | -$196.91 / 0.061 |
| Known audit | short | 34 | +$760.67 / 14.075 | +$638.02 / 8.929 | +$515.37 / 5.684 | +$392.72 / 3.640 |

## Interpretation

- The aggregate profile is viable at the preregistered 15 bps in validation and
  the known audit, but development loses its edge at 20 bps.
- Long trades are execution-fragile and negative in the fresh known audit. Short
  trades carry almost all recent performance and remain positive at 25 bps.
- Direction was not a tuned parameter. Disabling long after seeing this split
  would be post-hoc optimization, so the frozen forward scanner records both and
  reports them separately.
- Paper/Live remain ineligible. Forward promotion requires at least 60 clean
  closed decisions, 42 days, both directions represented, PF >= 1.25, acceptable
  drawdown, p90 decision latency <= 60 seconds and observed MEXC execution quality.

Forward collection is active under `forward_shadow.py`; the first completed scan
evaluated 45/45 symbols with zero transport errors and no eligible setup at that
bar boundary. Zero trades is a valid observation, not a synthetic fill.
