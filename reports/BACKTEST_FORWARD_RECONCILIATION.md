# Backtest ↔ Forward Reconciliation (read-model, evaluation-only)

- db_path: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- generated_at: `2026-07-07T17:26:35.109154+00:00`  ·  **PERSISTED (read-model table written)**
- matches persisted table: **true**
- FORWARD = live rolling-cache lane · BACKTEST = deep-history lane · new_logic_shadow filled in BOTH
- TRACKS if mean |Δnet_r| ≤ 0.35 AND sign-agreement ≥ 0.7 (min n=20)

> A mode that **TRACKS** may EARN a shorter forward window (its backtest predicts forward). **DIVERGES** → keep the full forward gate; the backtest must not shorten testing there. This module only reports trust — it changes no gate and promotes nothing.

| asset | mode | n | mean|Δ|R | median|Δ|R | sign-agree | corr | fwd ΣR | bt ΣR | verdict |
|---|---|--:|--:|--:|--:|--:|--:|--:|:--|
| crypto | intraday | 8 | 0.00 | 0.00 | 1.00 | +1.00 | -3.7 | -3.7 | **NEED_MORE_DATA** |
| crypto | swing | 19 | 0.03 | 0.00 | 1.00 | +0.99 | -1.3 | -1.9 | **NEED_MORE_DATA** |