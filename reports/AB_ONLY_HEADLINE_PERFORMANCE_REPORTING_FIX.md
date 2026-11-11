# A/B-only Headline Performance Reporting — Fix Report (R1)

**Date:** 2026-06-03
**Type:** **Reporting / statistics presentation only.** No scoring, thresholds,
signal registration, Telegram alert logic, strategy, or stored data changed.

## Why

The sector-gate simulation proved the actionable A/B stock signals are healthy
(A/B longs +120R, PF 2.62) while C-tier watchlist ideas are net-negative
(−21R, PF 0.68). The headline stat **mixed A/B + C**, so the desk's weekly
stocks PF read **1.49** when the actionable strategy was actually **~1.96–2.62**.
R1 makes the headline reflect actionable A/B only, with C-tier shown separately.

## PART 1 — Reporting surfaces touched

| Surface | File | Change |
|---|---|---|
| Shared "Recent Signal Performance" (crypto + stocks reports, both LLM packets via helper) | `src/signals/report_section.py` | headline A/B + C watchlist + tier split + all-tier diagnostic |
| `signal-stats` CLI | `src/cli.py` | HEADLINE (A/B) panel + C watchlist panel + overall relabelled "all-tier diagnostic"; JSON keys added |
| `review-signals` (Obsidian review + console) | `src/cli.py`, `src/signals/obsidian_export.py` | actionable A/B + C blocks lead; "Overall" relabelled all-tier diagnostic |
| Crypto LLM packet | `src/analysis/packet.py` | "HEADLINE actionable (A/B only)" + C line; weekly overall relabelled diagnostic |
| Stocks LLM packet | `src/stocks/llm_packet.py` | "Headline (A/B only)" + C-tier + all-tier diagnostic lines |
| Single source of truth | `src/signals/analytics.py` | new `headline_split()` |

Raw data / outcomes / `compute_breakdowns` math untouched. `review-day` is a
desk-output **count** summary (no PF metric) — nothing to fix; verified it
still runs.

## PART 2/3/4/5 — what each block now shows

- **Headline — Actionable Performance (A/B only):** sample, triggered, wins/
  losses, winrate, avg R, total R, **PF**, TP1/stop rate, active count.
- **C-tier Watchlist / Research Performance:** same metrics, with the note
  *"C-tier is watchlist/research quality, not Telegram-actionable. Excluded
  from the headline metric."*
- **Tier split:** per-tier A / B / C (n, total R, PF, winrate).
- **All-tier diagnostic (A/B/C — not the headline metric):** preserved,
  clearly labelled as diagnostic.

`headline_split()` recomputes PF/avg-R from the **raw R sums** of each slice
(not re-aggregated from rounded summaries), so the A/B headline PF is exact and
a negative C-tier can never bleed into it.

## PART 6 — Tests

New `tests/test_ab_headline_reporting.py` (6 tests, all green):
- headline excludes C-tier (A/B n=4, total R +5, PF 6.0; C n=3, total R −3);
- all-tier diagnostic still available (n=7, total R +2);
- A/B sample == A + B (by_tier);
- adding 5 more losing C-tier signals leaves headline PF/total R **unchanged**;
- rendered block has headline + separate C-tier + tier split + all-tier
  diagnostic, headline PF (6) not diluted, diagnostic carries the +2 total;
- reporting is read-only (row counts unchanged before/after).

Updated `tests/test_report_section_fix.py::test_block_sample_size_matches_signal_stats`
for the new schema: all-tier diagnostic carries the full sample (original
regression guard) **and** the headline carries the A/B sample.

Regression: reporting/signal/packet/obsidian/monitor suite → **all green**
(the one prior failure was this intentionally-updated test).

## PART 7 — Verification (live)

`signal-stats --asset-class stocks`:
```
HEADLINE — Actionable (A/B only): sample=335 wins=60 losses=53 PF=1.96 totalR=51
C-tier Watchlist / Research:      sample=171 wins=34 losses=45 PF=0.93 totalR=-3
all-tier diagnostic (NOT headline): sample=506 PF=1.49 totalR=48
```
→ headline PF **1.96** (actionable) vs the old mixed **1.49**. ✅

`signal-stats --asset-class crypto`: HEADLINE A/B PF 3.2 / totalR 11; C-tier
n=0; all-tier diagnostic shown. ✅

`review-signals`: renders "Headline — Actionable Performance (A/B only)" +
"C-tier Watchlist / Research" + "All-tier diagnostic". ✅
`review-day --write-obsidian`: exit 0 (count summary, no PF headline). ✅
`stocks-intraday-report` / `intraday-report`: regenerate; "Recent Signal
Performance" now shows the A/B headline + separate C block + LLM packets
refreshed. ✅ (see live run)

- No auto-trade. No Telegram logic touched. No DB writes from reporting.

## Safety checklist

- ✅ No scoring / thresholds / registration / Telegram / strategy change.
- ✅ Reporting/statistics presentation only.
- ✅ C-tier excluded from headline, shown separately; all-tier preserved as
  diagnostic.
- ✅ Read-only (test-proven); no stored outcomes modified.

## Files changed

- `src/signals/analytics.py` — `headline_split()` (+ `ACTIONABLE_TIERS`)
- `src/signals/report_section.py` — rewritten block + tier-aware active count
- `src/signals/obsidian_export.py` — `render_review` / `write_review_to_vault` optional headline
- `src/cli.py` — `signal-stats` panels + JSON; `review-signals` headline wiring
- `src/analysis/packet.py` — actionable headline line
- `tests/test_ab_headline_reporting.py` — NEW (6)
- `tests/test_report_section_fix.py` — updated one assertion to new schema

## Final answer

```
READY_AFTER_AB_ONLY_REPORTING_FIX
```
