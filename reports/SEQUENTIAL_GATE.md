# Sequential Promotion Gate — SPRT early-stopping (primary, read-model, evaluation-only)

- db_path: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- generated_at: `2026-11-11T20:24:26.081620+00:00`  ·  **PERSISTED (read-model table written)**
- source: **PRIMARY** — authoritative live rolling-cache lane, executed-vs-executed pairs
- matches persisted table: **true**
- test: paired per-signal edge d = B.net_r − A.net_r; H0 μ≤0 vs H1 μ≥0.1R; α=0.05 β=0.2; ACCEPT needs n≥20, REJECT needs n≥10, truncate at n=60
- fixed-gate fallback verdict (aggregate): **READY**

> **SEQ_ACCEPT is NOT auto-promotion** — it means the forward edge crossed the accept boundary EARLY and is ready for operator review sooner than the fixed 14d/60-trade window. Promotion still requires explicit operator sign-off. Backfill never counts; live locked.

| asset | mode | n pairs | mean edge R | ΣR | Σ$ | LLR | [lower, upper] | decision |
|---|---|--:|--:|--:|--:|--:|:--:|:--|
| crypto | swing | 181 | +0.359 | +64.99 | +1625 | +3.33 | [-1.5581, 2.7726] | **SEQ_ACCEPT** |
| crypto | intraday | 64 | +0.040 | +2.56 | +64 | -0.10 | [-1.5581, 2.7726] | **TRUNCATED_READY** |

Legend: **SEQ_ACCEPT** edge confirmed early (→ operator review) · **SEQ_REJECT** no edge, stop early · **SEQ_CONTINUE** keep accumulating · **TRUNCATED_…** hit n_max, deferred to the fixed gate.