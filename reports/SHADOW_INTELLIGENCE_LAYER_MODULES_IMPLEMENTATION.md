# Shadow Intelligence Layer — Modules Implementation (PARTS 1–6)

**Date:** 2026-06-18 · **Type:** shadow/diagnostic/add-only. **No trade-math / routing / live change.**
All modules fail open; the alert path reads only pre-computed caches (no network/LLM); heavy compute runs in background scripts.

## Store
`src/intelligence/store.py` → `data/intelligence/intelligence.sqlite` (tables: timeline_events, deriv_cache, phase_cache, phase_history, onchain_cache). Separate from the trading DB + rolling OHLCV cache. RO connection helper for the alert path.

## PART 1 — Symbol Timeline Memory (`src/intelligence/symbol_timeline.py`)
Append-only event log (9 event types) + compact summary. `record_symbol_event` (idempotent via dedupe_key), `get_symbol_timeline_summary`, `compact_timeline_for_payload`, `cleanup_old_events(90d)`, `timeline_health_report`. Live: **594 events / 31 symbols** bootstrapped. **Verdict: SYMBOL_TIMELINE_MEMORY_READY.**

## PART 2 — Derivatives Trajectory (`src/intelligence/derivatives_trajectory.py`)
Price slopes from the OHLCV archive (work now) + funding peak/turning from timeline + latest funding JSON. **Funding/OI numeric history is sparse in this project**, so slope/zscore degrade to None with `derivatives_data_confidence` reflecting it (price→low, +funding→medium). Contextual labels only (`derivatives_context`, `squeeze_risk_context`, `derivatives_warning`) — never a long/short action. Cached for 31 symbols. **Verdict: DERIVATIVES_TRAJECTORY_READY (price-primary; funding/OI accumulate forward).**

## PART 3 — Squeeze Phase Classifier (`src/intelligence/squeeze_phase.py`)
phase_0..5 from price structure (distance-to-local-high, 24h/7d/6h change) + derivatives + catalyst. Outputs phase, confidence, reason codes, distribution/peak/unwind risk scores, `no_chase_warning`, `phase_changed_since_last_seen`. History tracked in phase_history. **No auto-short / routing / score change.** Cached for 31 symbols. **Verdict: SQUEEZE_PHASE_CLASSIFIER_READY.**

## PART 4 — Thesis / Invalidation Formatter (`src/intelligence/thesis_formatter.py`)
Deterministic template (NO LLM/network). Compact line: *"Thesis: [setup] [dir] because [reasons]. Invalid if [stop]. Risk: [top risk]."* + full report block (WHY NOW / INVALIDATION / ENTRY / TARGETS / RISKS / CONFIDENCE / MISSING). SL/stop line never altered. **Verdict: THESIS_FORMATTER_READY.**

## PART 5 — On-chain Risk Layer (`src/intelligence/onchain_risk.py` + `scripts/onchain_risk_update.py`)
Interface + scorer (`score_from_security`, pure) + cache reader. **No contract addresses / API config exist in this project**, so it runs in unknown mode and reports `INTERFACE_READY_CONFIG_MISSING`. Background-only, TTL/timeout/rate-limit ready when `config/onchain.yaml` (api_provider/api_key + contracts) is added. Never blocks the alert path; never a trade command. **Verdict: ONCHAIN_RISK_LAYER_INTERFACE_READY_CONFIG_MISSING.**

## PART 6 — Aggregator (`src/intelligence/intelligence_layer.py`)
`assemble_intelligence_fields` reads cached summaries + runs the pure thesis, with a time budget (`timeout_partial` if exceeded), per-submodule fail-open, and metrics (`intelligence_layer_status`, `intelligence_runtime_ms`, `intelligence_cache_hit_ratio`, `intelligence_data_freshness_sec`). `intelligence_telegram_lines` returns **≤3** compact lines. Wired into `paper_entry.send_paper_entry_alert` via `payload.setdefault` (never overwrites) + appended to the actionable message after the risk-guard lines; SL line preserved. **Verdict: INTELLIGENCE_LAYER_SHADOW_READY.**

## Performance (100-signal cached enrichment)
p50 **47ms** · p95 **63ms** · p99 **78ms** · max 78ms — within the <100ms p95 target and <300ms hard cap. No network/LLM in the alert path (asserted by a socket-block test).
