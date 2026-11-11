# Telegram Signal Source — Final Decision Report (PART 8)

**Date:** 2026-06-14

## Final verdict

```
TELEGRAM_ALERTS_WORKING_BUT_NEED_STANDARDIZATION
```

The system's Telegram alerts are **functionally correct and not broken**. Every alert is traceable to a source module; every actionable alert has a `signal_id`; no legacy or orphan rows exist. The user's confusion comes from **inconsistent headers and missing type signals in the message body**, not from a misbehaving sender.

## 1. What Telegram signal types exist?

Three production templates plus one operator template:

| # | Name | Source | DB table | Visible header today |
|---|---|---|---|---|
| 1 | Crypto setup alert | `supervisor._format_idea_alert` | `watchlist_alerts` | `*B-tier* LONG *ZEC/USDT*` (no header) |
| 2 | Stocks setup alert | `stocks_monitor.format_stocks_alert` | `signal_alerts` | `[STOCKS] LONG AAPL ...` (no sub-type) |
| 3 | Paper-entry alert | `paper_entry.send_paper_entry_alert` | `signal_alerts` (alert_type='paper_entry') | `[PAPER ENTRY] STOCKS AAPL LONG` ✅ |
| 4 | Operator audit summary | direct `notifier.send()` from interactive scripts | none | `[TP/STOP CATEGORY AUDIT]` etc. |

A fifth category — "Opus / LLM Telegram sender" — **does not exist in the codebase.**

## 2. What is the difference between Opus alerts and system alerts?

**There are no Opus alerts.** Opus (the LLM trade-idea agent) produces JSON ideas that flow into `proposed_signals`. The downstream deterministic supervisor / monitor then renders a Telegram template. The LLM never sends a Telegram message. If the user sees a message that looks like Opus, it is either:
- the crypto setup template (#1), which includes an LLM-written thesis line in its body, OR
- an operator audit summary (#4), which I send directly from this session via `notifier.send()`.

## 3. Does Opus create trades or only review/enrich them?

**Opus creates trade ideas (the raw setup), but does not create Telegram alerts and does not change tier/score/routing.** The scoring agent and tier rules are deterministic Python.

## 4. Which alerts mean actual paper entry?

**Only `[PAPER ENTRY]` (template #3).** That is the lagging event: the system's tracker detected the candle that triggered the entry zone. Every other Telegram template is either pre-entry (setup) or post-trade (operator commentary).

## 5. Which alerts are only setup/watchlist/commentary?

- Template #1 (crypto setup) — **idea waiting for entry**, not an actual entry.
- Template #2 (stocks setup) — same, plus sub-types for zone/tier/score changes.
- Template #4 (operator summary) — pure commentary.

## 6. Which source has better outcomes over the last 3-4 days?

| Source | n | raw R | WR | Notes |
|---|---:|---:|---:|---|
| Paper-entry (lagging, post-entry) | 168 | +173R | 85% | Selection-biased. Measures "of trades that entered, what % won". |
| Stocks setup (leading, pre-entry) | 17 | +1R | 40% | Real WR for the stocks scanner channel. |
| Crypto setup (leading, pre-entry) | 50 | −9R | 18% | Crypto setup channel had a rough 4 days; consistent with sized-down cohorts. |

**Direct WR comparison is misleading.** Paper-entry's 85% is mechanical (entered → measured). Setup channel WRs (40% / 18%) are the real alpha measurement. Both sets sum to the same portfolio you've been auditing.

## 7. Which alert type is most useful for manual live shadow?

**Paper-entry (#3).** It is the only template that says "the system just entered" and gives the operator a 30-60 minute window to optionally mirror the trade manually. Setup alerts (#1, #2) are too early — many never trigger.

## 8. Which alert type is noisy/misleading?

**Crypto setup (#1).** It looks like a trade alert (tier + symbol + direction in bold) but is really an idea-watch notification. The header is missing the `[SETUP — WAITING FOR ENTRY]` qualifier; that's the single biggest cause of operator confusion.

**Operator summaries (#4)** can also confuse if not clearly labeled — recommended prefix `[OPERATOR SUMMARY — NOT A TRADE]`.

## 9. Are alerts currently working correctly?

**Yes**, mechanically. No orphans (`alert_type=NULL` is 0). No `signal_id=NULL` (is 0). No legacy untracked rows. Dedup works (only 2 expected `entry_change` repeats; 0 paper-entry duplicates). Delivery success rate on real (non-dry-run) paper-entry sends: 56/56 = 100%.

## 10. What should be changed in wording/format, if anything?

Recommended (NOT implemented yet):
1. **Prefix crypto setup with `[SETUP — WAITING FOR ENTRY]`** — eliminates the biggest confusion source.
2. **Prefix stocks setup sub-types** explicitly: `[SETUP — NEW SIGNAL]`, `[SETUP — ENTRY CHANGE]`, etc.
3. **Tag operator summaries** `[OPERATOR SUMMARY — NOT A TRADE]`.
4. **Add a `[CLOSE — TP1/TP2/STOP/EXPIRED]` template** — fills the missing post-trade notification gap.

See [TELEGRAM_ALERT_STANDARDIZATION_RECOMMENDATION.md](TELEGRAM_ALERT_STANDARDIZATION_RECOMMENDATION.md) for full templates.

## 11. Should any alert type be disabled, renamed, or downgraded?

| Type | Action |
|---|---|
| Crypto setup (#1) | **Rename**: prefix `[SETUP — WAITING FOR ENTRY]`. Do NOT disable. |
| Stocks setup (#2) | **Standardize sub-type headers**. Do NOT disable. |
| Paper-entry (#3) | **Keep as-is** — already standard-compliant. |
| Operator summary (#4) | **Tag explicitly** `[OPERATOR SUMMARY — NOT A TRADE]`. |
| Opus / LLM Telegram | n/a — doesn't exist |

None should be disabled. The system needs both setup (early heads-up) and paper-entry (event confirmation) for the operator to maintain a live shadow correctly.

## 12. Should the user trust paper-entry alerts more than setup/Opus commentary?

**Yes for the purpose of mirroring trades.** Paper-entry means the system has determined the price hit the entry — it is the closest the operator gets to "the trade is happening now". Setup alerts are watch-list entries; many never trigger. Operator summaries are commentary, not signals.

That said — the operator should NOT auto-mirror every paper-entry. The `[PAPER ENTRY]` template already includes risk flags, size weight, and a manual-check list precisely so the operator filters at decision time.

---

## Action items (priority order)

| Priority | Action | Effort | Risk |
|---|---|---|---|
| 1 | Add `[SETUP — WAITING FOR ENTRY]` header to crypto setup template (`supervisor._format_idea_alert`) | 30 min | low |
| 2 | Add sub-type prefix to stocks setup template (`stocks_monitor.format_stocks_alert`) | 30 min | low |
| 3 | Add `[OPERATOR SUMMARY — NOT A TRADE]` prefix to scripts that send Telegram directly | 30 min | none |
| 4 | Implement `[CLOSE — TP1/STOP/EXPIRED]` template + tracker hook (analogous to paper-entry) | 4 hours | medium |
| 5 | Add `signal_id:` footer to paper-entry visible body (already in payload) | 10 min | none |

None implemented in this audit. Operator should decide priority order.

---

## Final answer

```
TELEGRAM_SIGNAL_SOURCE_AUDIT_COMPLETE
```

The system's Telegram alerts are working and traceable; the gap is in **header clarity and a missing close-event notification**. Recommended standardization is documented; no production change in this pass.
