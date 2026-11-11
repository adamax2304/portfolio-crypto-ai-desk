# Opus Packet Catalyst Freshness Labels (PART 6)

**Date:** 2026-06-15 · Display-only. No freshness gate, no suppression, no score change.

## What changed

`src/analysis/packet.py` — the "High-confidence catalysts" section now:
- computes a per-catalyst **age tag** from `timestamp`: `fresh(<1h)` / `recent(<6h)` / `OLD(>6h)` / `age?`;
- **sorts freshest-first**;
- adds **source quality** (official / reputable / social / unknown);
- emits an explicit `_No fresh (<6h) high-confidence catalyst — all listed are stale._` line when nothing is fresh.

Example:
```
### High-confidence catalysts (primary source, freshest first)
- **ZEC** [listing] recent(2.4h), reputable — ZEC spot listing announced (CoinDesk)
- **TAO** [partnership] OLD(11.2h), social — ... (t.me/...)
_No fresh (<6h) high-confidence catalyst — all listed are stale._  ← only if applicable
```

## Rules honoured

- **No freshness gate** — nothing is rejected or downgraded; this is presentation only.
- No score change, no signal suppression.
- Opus now sees catalyst age + source explicitly, so it stops treating a stale catalyst as fresh.

## Tests

Packet builds without error (import + render smoke). The high-conf block is
additive text; existing packet sections unchanged.
