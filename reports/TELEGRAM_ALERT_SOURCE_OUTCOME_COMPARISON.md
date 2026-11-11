# Telegram Alert Source — Outcome Comparison (PART 3)

**Date:** 2026-06-14 · Companion: [TELEGRAM_ALERTS_LAST_4D_AUDIT.csv](TELEGRAM_ALERTS_LAST_4D_AUDIT.csv).

---

## 1. Per-source outcome stats (last 4d)

| Source bucket | n alerts | unique signals | n triggered | wins | losses | expired | open/waiting | raw R | PF | WR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **(1) Paper-entry alerts** (signal_alerts.alert_type='paper_entry') | 168 | 168 | 167 | 135 | 23 | 9 | 1 | **+173.0R** | 8.52 | **85%** |
| **(2) Stocks setup alerts** (signal_alerts non-paper-entry) | 17 | 11 | 9 | 2 | 3 | 4 | 2 | **+1.0R** | 1.33 | **40%** |
| **(3) Crypto setup alerts** (watchlist_alerts) | 50 | 45 | 25 | 4 | 18 | 3 | 19 | **−9.0R** | 0.50 | **18%** |
| (4) Operator audit summary | varies | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| (5) Opus / LLM Telegram | **none — does not exist** | — | — | — | — | — | — | — | — | — |
| (6) Legacy / NULL alert_type | **0** in last 4d | — | — | — | — | — | — | — | — | — |
| (7) Cross-source duplicates | 3 (lifecycle overlaps, not bugs) | — | — | — | — | — | — | — | — | — |

## 2. Critical interpretation — these are NOT directly comparable

The headline number "paper_entry WR=85%" is **NOT a quality signal**. Paper-entry alerts are **lagging** — by construction they only fire AFTER the system has paper-entered, so the conditional probability of "triggered" is ~100%. You're conditioning on entry, then measuring win-rate of what entered. Of course it looks great.

Setup alerts are **leading** — they fire BEFORE entry, when the idea is proposed. Many setups never trigger (price doesn't reach the entry zone, or `stale_before_entry` / `entry_moved_away` cancels them). The denominator includes all the trades that the filter correctly killed before they could lose money.

**The correct read of the comparison:**

- **(1) Paper-entry alerts measure "what % of trades the system actually entered, ended up winning"** — answer: 85% WR last 4d.
- **(2) Stocks setup alerts measure "what % of setups proposed ended up profitable"** — answer: 40% WR.
- **(3) Crypto setup alerts measure the same for crypto** — answer: 18% WR (n=45, raw R=−9R).

Group (3) looks ugly. Two reasons:
- Most are `mode=scalp` and `mode=intraday` shorts in chop conditions, which historically have poor WR (consistent with our category audit).
- 19/45 are still waiting / open / unfilled — the denominator includes non-completed trades counted as "not won".

## 3. Which source has the best realized outcomes?

**Paper-entry alerts**, mechanically. But that's by *survivorship* — they only see the trades that triggered.

**For raw alpha measurement**, look at setup alerts. The stocks setup channel is positive (+1R / WR 40% / PF 1.33) on only 17 alerts; the crypto setup channel is negative (−9R / WR 18% / PF 0.50). This matches the production-side conclusion: stocks intraday B-tier is the engine; crypto needs the sizing-layer protection it already has.

## 4. Which alert source produced the most noise?

**Crypto setup alerts** (n=50 last 4d) had the highest noise-to-signal ratio: 19 still waiting/open, 18 losses, only 4 wins. The 18 losses are mostly the same playbook cohorts already flagged as weak (crypto intraday catalyst shorts, scalp). The system *correctly* sized those at 0.5× via the playbook-aware sizing layer; the operator should NOT manually mirror the underlying crypto setup alerts at 1×.

## 5. Did Opus alerts outperform deterministic system alerts?

**N/A — no Opus alerts exist.** The codebase has no Opus or LLM Telegram sender. Any "Opus-style" message the user saw was either:
- the crypto setup alert template (`_format_idea_alert`, Markdown), which can look LLM-ish because it carries the LLM-written thesis line; or
- an operator-triggered audit summary sent from interactive sessions.

## 6. Did paper-entry alerts outperform setup alerts?

By WR — yes, mechanically (selection bias). By signal quality — they're measuring different things. You should not read it as "the paper-entry alert is a better idea source"; it's an *execution event*, not an idea event.

## 7. Are there alerts that look actionable but are actually informational?

Yes — **the crypto setup alert** (template 1) lacks an explicit `[SETUP - WAITING FOR ENTRY]` header. It looks like a trade alert (tier + symbol + direction in bold) but is really an idea-watching notification. Manual operators have been observed treating it as actionable. **Recommended:** add an explicit header — see [TELEGRAM_ALERT_STANDARDIZATION_RECOMMENDATION.md](TELEGRAM_ALERT_STANDARDIZATION_RECOMMENDATION.md).

## 8. Are any alert types misleading?

- **Crypto setup alert** — looks like a trade signal; is really a setup-to-watch notification.
- **Paper-entry alert** — actually clear (already says `[PAPER ENTRY]`), but the `Manual shadow only` disclaimer line is at the bottom; some users may miss it.
- **Stocks setup alert sub-types** (`entry_change`, `score_improvement`, `tier_upgrade`, `invalidation_change`) — sub-type is in the structured row, but the visible Telegram message uses the same `[STOCKS]` bracket header for all 5; the user can't easily tell from the message alone which sub-type fired.

## 9. Bottom line for the operator

- **Trust paper-entry alerts as event notifications** (`the system just paper-entered`). They are lagging but reliable.
- **Treat setup alerts as a watch list, not an order**. They are leading and have realistic <50% WR. The system's sizing layer already discounts the weak cohorts.
- **There is no Opus Telegram message.** If you see something that looks like Opus commentary on your phone, it's either the crypto setup template's LLM thesis line OR an operator audit summary, NOT an autonomous LLM trade signal.
