# Telegram Catalyst Context (PART 4)

**Date:** 2026-06-15 · Plain-text, additive. No scoring/TP/SL/routing change.

## What changed

A compact **3-line catalyst block** is now inserted into:
- `src/notifiers/setup_alert.py` (crypto + stocks setup alerts)
- `src/notifiers/paper_entry.py` (paper-entry alerts, long + short)

Block:
```
Catalyst: <fresh|recent|old> <source> — <headline>   |   Catalyst: none
Funding/OI: confirmed (<deriv>) | missing | conflicting (squeeze risk) | not available for stocks
Move type: catalyst-backed | technical momentum | chase risk
```

### Rendered examples (live, within budget)
Crypto catalyst-backed setup (557 chars):
```
[🟡 SETUP — WAITING FOR ENTRY]
CRYPTO ZEC/USDT LONG
...
Catalyst: recent(2.5h) reputable — ZEC listing
Funding/OI: confirmed (OI-up)
Move type: catalyst-backed
...
```
Technical crypto setup → `Catalyst: none` + `Move type: technical momentum`.
Stocks → `Funding/OI: not available for stocks`.

## Preserved (regression-checked)

- crypto scalp paper-entry `⚠️ LOW-CONFIDENCE SCALP` caution — kept
- no-news / no-deriv short caution — kept
- `System did NOT place a real order.` disclaimer — kept
- plain-text parse mode (`parse_mode=""`) — kept
- crypto scalp **setup** Telegram remains suppressed (untouched)
- close alerts unchanged

## Tests

`test_9` catalyst block shows catalyst-backed; `test_10` stocks "not available";
`test_11` setup includes block + header + "No paper entry yet."; `test_12` paper-entry
block + disclaimer; `test_13` technical shows "Catalyst: none". Plus the prior
38 telegram-standardization tests still pass (no-news/scalp cautions, plain text).

## Approval note

The user's task explicitly authorised Telegram message-text changes for this catalyst block, so it is implemented. (The earlier audit had listed it as "needs approval" — that approval is granted by this task's allowed-changes list.)
