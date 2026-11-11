# Telegram Risk-Alert Format Check (PART 4)

**Date:** 2026-06-17 · **Verdict:** OK (no spam, no crash, SL preserved).

## Sample actionable B/A alert structure (from `paper_entry.py`)
1. Header (direction-colored) + `ASSET SYMBOL direction`
2. Entry / Time / Playbook / Tier-Score / Size
3. **Stop: …** ← SL line, always present (in the message body, never replaced)
4. TP1 / TP2 / TP3
5. Catalyst block (3 lines)
6. Why-now (≤2 bullets) + Risk (≤3 flags)
7. Manual-check disclaimer + signal_id + TradingView
8. Freshness line (appended)
9. **Diagnostic lines** (appended after freshness, only when applicable): circuit-breaker would-pause (deduped 1/asset/mode/day/level), risk-off context, carryover/revalidation, sector-cap would-bind, catalyst-backed, position advisor.

## Checks
- [x] **Stop/SL line still present** — built in the body; diagnostics are appended, never replace it.
- [x] **Freshness line present.**
- [x] **Diagnostics appended compactly** — each ≤1 line; non-applicable ones omitted.
- [x] **No markdown crash** — notifier sends `parse_mode=""` (plain text), so `$ _ + ( )` etc. don't break Telegram.
- [x] **No emoji/cp1252 console crash in production** — the emoji (⚠/ℹ) live in the UTF-8 Telegram payload; the only cp1252 issues seen were local `print()` in two scripts, since fixed (ASCII output).
- [x] **No spam** — circuit-breaker line deduped per asset/mode/day/level; other lines only when their condition holds.

## C-tier restriction labeling
A restricted stocks-intraday C-tier signal is already blocked upstream (`decide_paper_entry` → not actionable), so it never produces a pushed Telegram alert. The belt-and-suspenders shadow route would prefix `[SHADOW / REVIEW ONLY — C-TIER RESTRICTED]` if one ever reached the alert path.
