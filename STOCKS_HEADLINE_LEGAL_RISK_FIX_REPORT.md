# Stocks Headline / Legal-Risk Gate — Fix Report (PART 3)

**Date:** 2026-05-30. Scope: news-aware Telegram dispatch gate.
**Does NOT change scoring, thresholds, agents, strategy, or auto-trade.**

---

## What was broken

On 2026-05-29 cycle 2 the deterministic stocks pipeline rated **SMCI
A-tier (82.52, triggered)** purely on price/momentum. External research
(captured in `OPUS_ENRICHED_REVIEW_CYCLE2.md` §4) revealed:

* **Active federal indictment** (alleged illegal routing of NVIDIA AI
  servers to China via shell entity) — CNBC, Simply Wall St.
* **Multiple securities class-action lawsuits** filed in the prior week.
* **Ernst & Young auditor resignation** + delayed SEC filings.

The system has no agent that reads news headlines for **legal /
governance** risk categories. The score was numerically valid; the
verdict ("A-tier actionable") was uninvestable. A Telegram A-tier
SMCI alert with no headline awareness is a real money-loss risk.

The audit recommended adding a headline/legal-risk flag for stocks
A-tier — PART 3.

---

## What changed (code)

### `src/stocks/legal_risk.py` (NEW)

Tight, read-only pattern library + assessment.

* **Categories** (regex, case-insensitive):
  * `indictment` (federal/criminal indictment, exec arrest)
  * `sec_doj` (SEC charges/sues/probe; DOJ investigation/probe)
  * `securities_fraud` (securities/accounting fraud, misstatement)
  * `auditor` (auditor resignation/withdrawal/dismissal, Big-4 step-down, going concern, adverse opinion)
  * `class_action` (securities class-action, shareholder lawsuit, investor suits)
  * `going_concern` (going concern doubt, Ch 11/7 bankruptcy)
  * `restatement` (financial restatement, material weakness)
  * `delisting` (delisting, NASDAQ/NYSE noncompliance, trading halt)
* **Blocking categories** (suppress Telegram automatically):
  `indictment, sec_doj, securities_fraud, auditor, class_action, going_concern`.
  The other two (`restatement`, `delisting`) raise an advisory note but
  do NOT auto-block — they're more often routine.
* `detect_legal_risk(news_hits)` returns a `LegalRiskAssessment` with
  `categories`, `severity` (high/medium/none), `evidence` (first 3 hits
  per category, kept under 240 chars), `blocking`. Helper properties
  produce the marker string `ACTIVE_LEGAL_HEADLINE_RISK: <cats>`, the
  `cap_reason`, and a human-readable `counter_thesis`.
* `signal_has_legal_block(signal_row)` — read-only check of a
  `proposed_signals` row's `no_entry_conditions_json` for the marker.

### `src/stocks/agents/trade_idea_agent.py`

For every idea emitted:

* `detect_legal_risk(news_by_symbol[symbol])` is called.
* When **blocking**: the assessment's `counter_thesis` is added to
  `counterarguments`, `cap_reason` to `cap_reasons`, and the marker
  string to `avoid_conditions` (which the registry persists as
  `no_entry_conditions_json`).
* When **non-blocking but present** (e.g. restatement): the
  `counter_thesis` advisory note is added; no avoid marker.
* The structured assessment is always written to
  `idea.raw["legal_risk"]` for audit / Obsidian export.

**Score and tier are untouched.** The gate is hygiene, not scoring —
the report still surfaces the A/B verdict for human review, with the
counter-thesis explaining why Telegram was suppressed.

### `src/stocks/monitor.py`

* `MaterialImprovementChecker._classify` now calls
  `signal_has_legal_block(current)` right after the `tier in {A,B}` +
  `invalidation present` checks. When the marker is present, the
  decision short-circuits to `AlertDecision(False, "legal_block",
  "active legal headline risk — Telegram suppressed; verify report")`.
* `MonitorTickResult` gains `skipped_legal_block: int` so each tick can
  report how many A/B signals were suppressed by the gate.
* The block fires **before** the cooldown (a brand-new A-tier with
  legal risk never reaches Telegram, regardless of cooldown state).

### `tests/test_stocks_legal_risk.py` (NEW — 15 tests)

| Test | What it pins |
|------|--------------|
| `test_smci_headlines_detected_as_blocking_high_severity` | The exact SMCI case: indictment + class-action + auditor headlines → blocking, high severity, all three categories matched, marker/cap_reason/counter_thesis all populated |
| `test_routine_news_does_not_trigger_legal_risk` | AAPL/NVDA/LLY benign headlines → no categories, no marker, no block |
| `test_low_severity_news_is_advisory_not_blocking` | A standalone restatement → advisory only, `blocking=False`, no avoid_condition |
| `test_sec_charges_alone_is_blocking` | "SEC charges Acme with accounting fraud" → block |
| `test_doj_probe_is_blocking` | "DOJ launches investigation into Acme exec" → block (handles word gaps) |
| `test_going_concern_warning_is_blocking` | 10-Q going-concern disclosure → block |
| `test_blocking_categories_set_is_strict` | Pins the exact `BLOCKING_CATEGORIES` set to prevent silent expansion |
| `test_signal_has_legal_block_true_for_marker` | Marker round-trips through `no_entry_conditions_json` JSON |
| `test_signal_has_legal_block_false_without_marker` | Clean signal → no block |
| `test_signal_has_legal_block_handles_missing_field` | Defensive: no `no_entry_conditions_json` → no block |
| `test_signal_has_legal_block_handles_bad_json` | Garbage JSON → no block (fail-safe) |
| `test_smci_new_signal_is_blocked_by_legal_gate` | **SMCI regression**: A-tier new signal with marker → `should_send=False`, `alert_type="legal_block"` |
| `test_smci_tier_upgrade_is_blocked_by_legal_gate` | B→A upgrade on legally-flagged symbol → still blocked (bypasses cooldown bypass!) |
| `test_clean_a_tier_without_legal_flag_still_fires_new_signal` | Sanity: clean A-tier behaves normally |
| `test_trade_idea_agent_propagates_legal_marker_to_avoid_conditions` | End-to-end: `StockTradeIdeaAgent` consuming `scoring_payload + technical_payload + news_payload` → idea has marker in `avoid_conditions`, `cap_reasons` has `legal_headline_risk:`, `raw.legal_risk.blocking=True`, **tier/score unchanged** |

---

## Behavior summary

| Scenario | Tier in report | Telegram |
|----------|----------------|----------|
| SMCI A-tier with indictment news | **A (unchanged)** | **BLOCKED** (`legal_block`) |
| SMCI B-tier with class-action news | **B (unchanged)** | **BLOCKED** |
| Clean AAPL A-tier (no flagged news) | **A** | sent normally |
| LLY A-tier with mild restatement note | **A** | sent normally (advisory note in counter-thesis only) |
| SMCI suppression — auditor resigns later | report shows updated tier | block persists for as long as the news pattern matches recent hits |

The gate runs at **Telegram dispatch time** by reading the live
`proposed_signals.no_entry_conditions_json`. Re-running the pipeline
clears or re-applies the marker based on the news available at run time
— no manual reset needed.

---

## Tests

```
$ python -m pytest -q
.................................................................................. (146 passed in 3:01)
```

All 146 tests pass — including 15 new legal-risk regression tests.

---

## What this fix does NOT touch

- **No scoring/threshold change.** The same numeric score, the same
  tier, the same direction. Only `cap_reasons`, `counter_thesis`,
  `avoid_conditions`, and `raw.legal_risk` change.
- **No agent removed or refactored.** A new module + light hooks.
- **No auto-trade.** This is a Telegram suppression hygiene gate.
- **No crypto path.** Spec scoped to stocks; the helper is generic
  enough to reuse later if crypto news collection improves.
- **No paid news API.** Pattern-matches the existing
  `CompanyNewsAgent.hits_by_symbol` output (already from `news_items`,
  `test_source` filtered per QA fix #2).
- **No deletion of any data.**

---

## Operational impact

- **From the next stocks pipeline run on**: any A/B signal whose
  attached news mentions one of the six blocking categories is marked
  with the avoid_condition + cap_reason + structured `raw.legal_risk`.
- **From the next monitor tick on**: those signals do not generate
  Telegram alerts. The report and `proposed_signals` row remain so the
  human reviewer can see the tier+context.
- **Each suppressed tick** increments `MonitorTickResult.skipped_legal_block`
  and logs the reason; the per-decision entry in `result.decisions`
  has `alert_type="legal_block"`.

---

## Safety

- New module is pure regex + dataclass; no I/O.
- Trade-idea agent additions are append-only: no existing field is
  overwritten or removed.
- Monitor block runs BEFORE cooldown, so the suppression cannot be
  bypassed by a tier_upgrade race.
- Fails safe: bad JSON / missing field → `signal_has_legal_block=False`
  → normal alert behavior (we never block on parser errors).
- The marker string `ACTIVE_LEGAL_HEADLINE_RISK` is stable; tests pin it.
