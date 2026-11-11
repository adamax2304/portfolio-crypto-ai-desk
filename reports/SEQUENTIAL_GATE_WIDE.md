# Sequential Promotion Gate — SPRT early-stopping (wide, read-model, evaluation-only)

- db_path: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- generated_at: `2026-07-07T17:24:06.997141+00:00`  ·  **PERSISTED (read-model table written)**
- source: **WIDE (provisional)** — Move-3 deep-history lane, WITH-AVOIDED edge (every old-filled decision; new-logic SKIP books 0R = avoided trade). Bigger/faster sample; NOT the authoritative promotion evidence.
- matches persisted table: **true**
- test: paired per-signal edge d = B.net_r − A.net_r; H0 μ≤0 vs H1 μ≥0.1R; α=0.05 β=0.2; ACCEPT needs n≥20, REJECT needs n≥10, truncate at n=60
- fixed-gate fallback verdict (aggregate): **NOT_READY**

> **SEQ_ACCEPT is NOT auto-promotion** — it means the forward edge crossed the accept boundary EARLY and is ready for operator review sooner than the fixed 14d/60-trade window. Promotion still requires explicit operator sign-off. Backfill never counts; live locked.

| asset | mode | n pairs | mean edge R | ΣR | Σ$ | LLR | [lower, upper] | decision |
|---|---|--:|--:|--:|--:|--:|:--:|:--|
| crypto | intraday | 159 | +0.382 | +60.75 | +1519 | +4.24 | [-1.5581, 2.7726] | **SEQ_ACCEPT** |
| crypto | scalp | 155 | +0.429 | +66.55 | +1664 | +8.95 | [-1.5581, 2.7726] | **SEQ_ACCEPT** |
| crypto | swing | 125 | +0.282 | +35.31 | +883 | +2.07 | [-1.5581, 2.7726] | **TRUNCATED_NOT_READY** |

Legend: **SEQ_ACCEPT** edge confirmed early (→ operator review) · **SEQ_REJECT** no edge, stop early · **SEQ_CONTINUE** keep accumulating · **TRUNCATED_…** hit n_max, deferred to the fixed gate.