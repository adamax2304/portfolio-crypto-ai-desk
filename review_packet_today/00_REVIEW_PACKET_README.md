# Review Packet — Today (2026-05-25)

**Generated at:** 2026-05-25 ~17:50 EEST (14:50 UTC)
**Project:** crypto-ai-desk
**Auditor model:** Claude (Opus 4.7)
**Scope:** Decision Quality Audit of today's crypto scalp, crypto intraday, and stocks intraday analyses.

---

## What this packet is

A read-only audit of the three analyses produced today:

1. **Crypto scalp** — `data/reports/scalp/2026-05-25_13-52_scalp_report.md`
2. **Crypto intraday** — `data/reports/intraday/2026-05-25_14-03_intraday_report.md`
3. **Stocks intraday** — `data/reports/stocks/intraday/2026-05-25_14-12_stocks_intraday_report.md`

The audit also inspects the LLM packets, signal registry, active signals, agent outputs, and protocol compliance.

**No code, configuration, or trading logic was changed.** This is a pure analysis/audit exercise.

---

## Suggested reading order

1. **`15_FINAL_EXTERNAL_REVIEW_SUMMARY.md`** — compact summary for the external reviewer.
2. **`01_DECISION_AUDIT_TODAY.md`** — the main audit with verdicts.
3. **`10_DATA_COVERAGE_AUDIT.md`** — what data was available vs missing.
4. **`13_SCORE_AND_RISK_AUDIT.md`** — whether scores are justified.
5. **`14_TECHNICAL_ANALYSIS_AUDIT.md`** — chart-level review of each idea.
6. Individual reports + packets — `02_…` through `07_…`.

---

## File index

| File | Purpose | Status |
|------|---------|--------|
| `00_REVIEW_PACKET_README.md` | This file | OK |
| `01_DECISION_AUDIT_TODAY.md` | Main audit | OK |
| `02_REPORT_CRYPTO_SCALP.md` | Latest crypto scalp report (16:52 EEST) | Copied verbatim |
| `03_REPORT_CRYPTO_INTRADAY.md` | Latest crypto intraday report (17:03 EEST) | Copied verbatim |
| `04_REPORT_STOCKS_INTRADAY.md` | Latest stocks intraday report (17:12 EEST) | Copied verbatim |
| `05_LLM_PACKET_CRYPTO_SCALP_OR_SHARED.md` | Crypto LLM packet | **STALE** — generated 2026-05-24, scalp/intraday today did not regenerate it |
| `06_LLM_PACKET_CRYPTO_INTRADAY_OR_SHARED.md` | Same file (shared crypto packet) | **STALE** — identical to 05 |
| `07_LLM_PACKET_STOCKS_INTRADAY.md` | Stocks LLM packet | **STALE** — generated 2026-05-25 02:00, refers to old AAPL/TSLA-only report |
| `08_SIGNAL_STATS_SNAPSHOT.md` | signal-stats + active-signals + track-signals output | OK |
| `09_AGENT_OUTPUTS_SUMMARY.md` | Which agents contributed what | OK |
| `10_DATA_COVERAGE_AUDIT.md` | Data inventory vs blindspots | OK |
| `11_PROTOCOL_COMPLIANCE_AUDIT.md` | A/B/C, asset_class, mode discipline | OK |
| `12_NEWS_TELEGRAM_OBSIDIAN_AUDIT.md` | External context usage | OK |
| `13_SCORE_AND_RISK_AUDIT.md` | Score justification + risk gates | OK |
| `14_TECHNICAL_ANALYSIS_AUDIT.md` | Chart/level review for each idea | OK |
| `15_FINAL_EXTERNAL_REVIEW_SUMMARY.md` | Compact summary | OK |
| `16_SIGNAL_TRACKING_PERFORMANCE_AUDIT.md` | Signal registry + tracker review | OK |

---

## Critical caveats

- The packets named `05_…` and `06_…` are the **same file**. The crypto desk does not split packets by scalp vs intraday; it shares one packet keyed by `--mode <scalp|intraday>`. The most recent generation (Sunday Weekend Mode) was for `intraday`, and **no fresh `prepare-analysis` was run today**, so the LLM packet that a fresh session would consume is stale.
- **Weekend Mode**: today is Monday in `Asia/Nicosia`. Weekend Mode is **OFF**. The stale crypto packet still references "Weekend Mode active" because it was generated on Sunday — be careful reading it.
- **`update-obsidian-context` is a TODO stub** — Obsidian's `Current_Context_For_LLM.md` remains a template, never auto-populated.
- **Telegram alerts**: B/A-tier auto-send is implemented and the two monitors (scalp + intraday) are running in the background, but no B/A crypto idea was produced today, so no Telegram alert was tested in this audit window.

---

## Commands that were run

```text
python -m src.cli intraday-report           # OK, saved 2026-05-25_14-03_intraday_report.md
python -m src.cli scalp-report              # OK, saved 2026-05-25_13-52_scalp_report.md
python -m src.cli stocks-intraday-report    # OK, saved 2026-05-25_14-12_stocks_intraday_report.md
python -m src.cli weekend-status            # OK, Weekend Mode = inactive
python -m src.cli signal-stats --asset-class crypto    # OK, sample=1 (anecdotal)
python -m src.cli signal-stats --asset-class stocks    # OK, sample=19 (weak)
python -m src.cli active-signals            # OK, 19 active (mostly stocks)
python -m src.cli track-signals --all       # OK, checked=19 updated=0 no_ohlcv=0
python -m src.cli active-signals --asset-class crypto  # FAIL — flag not supported
```

---

## Acceptance criteria — status

- review_packet_today/ exists: yes
- All required Markdown files exist: yes (16 + this README)
- Three latest reports included: yes (verbatim copies)
- Two crypto LLM packets + stocks LLM packet: included (crypto is shared, both stale)
- Signal stats snapshot: included
- Audits 10–16: included
- No code or trading logic changed: confirmed
- Missing data clearly documented: see `10_DATA_COVERAGE_AUDIT.md` and `12_NEWS_TELEGRAM_OBSIDIAN_AUDIT.md`

---

## Known missing files / gaps documented in the audit

- Fresh `prepare-analysis` LLM packets for today's scalp + intraday — **not generated today**.
- Fresh stocks LLM packet for today's 14:12 UTC report — **not regenerated**.
- Real stocks RSS feeds — disabled; only test_source items in pipeline.
- Earnings calendar — empty (`Earnings events tracked: 18` reported but lookups for SPY/QQQ/etc. all 404'd).
- Live Telegram/X/Discord crowd context — not connected (placeholder KOL only).
- Liquidation heatmaps, order book depth, on-chain whale flows, ETF flows, DXY/yields, token unlocks — not connected (acknowledged blindspots).
- `update-obsidian-context`, `log-idea-to-obsidian`, `log-news-to-obsidian`, `review-day` — all TODO stubs.

See `01_DECISION_AUDIT_TODAY.md` Section 9 for severity-tagged issue list.
