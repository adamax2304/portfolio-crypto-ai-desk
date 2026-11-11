# Test DB Isolation Fix — Report

**Date:** 2026-06-03
**Type:** Test-infrastructure fix only — **no** production/trading-logic change.
**Scope:** two test modules. No `src/` production code touched.

## Root cause

Two test modules ran against the **live production database**
(`db/crypto_ai_desk.sqlite`) instead of an isolated temp DB:

- `tests/stocks/test_stocks_news_tagging.py`
- `tests/test_stocks_monitor_alerts.py`

Both built their store from `load_config().db_path`, which resolves to the
production SQLite file. As the live desk kept running, the DB grew
(news_items 2624 → ~2987, signal_alerts 431, proposed_signals 1010). Two
failure modes followed:

1. **News tagging** — tests insert one fixture row and assert it is returned by
   `load_recent_news(limit=500)`. Once production held > 500 newer news rows,
   the freshly-inserted fixture fell outside the 500-row window
   (`ORDER BY published_at DESC LIMIT 500`) and the assertion failed.
2. **Monitor alerts** — `StocksMonitorSession.run_once()` reads **all** active
   signals and the `signal_alerts` ledger from the same DB. Accumulated
   production alerts polluted the cooldown / dedup / "already-alerted" state,
   so deterministic single-signal assertions (`tier_upgrade`,
   `score_improvement`, `dry_run` recording) became flaky/failed.

This is a **test-isolation bug**, not a logic bug: scoring, thresholds,
cooldown and alert logic are all correct — the tests just weren't hermetic.

## Fix — fixture-level dependency injection (no production code changed)

Added one **autouse** pytest fixture to each module that monkeypatches the
module-local `load_config` so every call returns a config whose
`settings["data"]["db_path"]` points at a **fresh per-test temp SQLite file**
under `tmp_path`.

Why this is sufficient and minimal:
- `ProjectConfig.db_path` returns `self.root / settings["data"]["db_path"]`;
  an **absolute** temp path on the right-hand side wins (pathlib join
  semantics), so the store location is cleanly redirected with zero production
  edits.
- Every consumer in the test resolves the DB the same way:
  - news module — the `_kit()` helper (`SQLiteStore(config.db_path)`) and the
    inline `sqlite3.connect(config.db_path)` cleanup calls;
  - monitor module — the `_make_store()` helper **and**
    `StocksMonitorSession(config, …)`, which internally does
    `SQLiteStore(config.db_path)` (monitor.py:378). Both now share the **same
    empty** temp DB, so cooldown/dedup is deterministic.
- `db.init_db()` (existing schema bootstrap) creates `news_items`,
  `proposed_signals`, `signal_alerts`, `watchlist_alerts`, etc. in the temp DB
  — no hand-rolled schema needed.
- `tmp_path` is unique per test and auto-cleaned by pytest → every test starts
  with empty `news_items` / `signal_alerts` / `proposed_signals`.

### Fixture (identical shape in both files)

```python
@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    db_file = tmp_path / "isolated_*.sqlite"
    def _patched_load_config(*args, **kwargs):
        cfg = _config_mod.load_config(*args, **kwargs)   # real loader
        cfg.settings.setdefault("data", {})["db_path"] = str(db_file)
        return cfg
    monkeypatch.setattr(sys.modules[__name__], "load_config", _patched_load_config)
    yield
```

`_config_mod` is `import src.config as _config_mod` (the genuine loader), so
there is no recursion — only the **test module's** `load_config` binding is
swapped, and only for the duration of each test.

## Files changed (tests only)

- `tests/stocks/test_stocks_news_tagging.py` — added `import sys`,
  `import pytest`, `import src.config as _config_mod`, and the `_isolated_db`
  autouse fixture. `_kit()` body unchanged.
- `tests/test_stocks_monitor_alerts.py` — added `import sys`,
  `import src.config as _config_mod`, and the `_isolated_db` autouse fixture.
  `_make_store()` / `_insert_ab_signal` / `_cleanup` bodies unchanged.

No file under `src/`, no config YAML, no scoring/threshold/strategy code, and
no production database were modified.

## Proof the production DB is not used

1. **Monitor signals never reach prod** — after the runs:
   ```
   prod proposed_signals symbol=QA_MON_UP    -> 0
   prod proposed_signals symbol=QA_MON_SCORE -> 0
   prod proposed_signals symbol=QA_MON_DRY   -> 0
   ```
2. **Isolated re-run does not write prod** — the news fixture URL
   `…/qa-fix-2-test-source-filter` existed in prod at **rowid 20785** (a
   leftover from the *old* non-isolated test design). Re-running the now-fixed
   test left prod **unchanged**:
   ```
   prod rows for url after re-run: [20785] (count=1)   # no new insert
   ```
   A non-isolated test would have inserted a second row; it did not.
3. The temp DB path is `tmp_path/"isolated_*.sqlite"` — pytest-managed,
   per-test, auto-removed.

### Pre-existing leftovers (left untouched per "do not delete production data")

5 `source='test_source'` news rows and 4 `signal_id LIKE 'sig_test_%'`
`signal_alerts` rows remain in prod from **earlier non-isolated runs** (before
this fix). They are **not** deleted (production-data safety rule) and are
harmless: production `load_recent_news` already drops `test_source` rows by
default, and the `sig_test_*` alerts reference signals that no longer exist.

## Tests run

| Command | Result |
|---|---|
| `pytest tests/stocks/test_stocks_news_tagging.py -q` | **6 passed** |
| `pytest tests/test_stocks_monitor_alerts.py -q` | **20 passed** |
| `pytest tests/stocks -q` | **39 passed** |
| `pytest tests/test_stocks_monitor_alerts.py tests/stocks/test_stocks_news_tagging.py -q` | **26 passed** |
| `pytest tests/test_stocks_monitor_cooldown.py -q` (related) | **11 passed** |

All six originally-failing tests now pass:
- `test_company_news_agent_falls_back_to_crypto_tagged_when_symbol_matches` ✅
- `test_test_source_filter_drops_by_default` ✅
- `test_load_recent_news_asset_class_filter` ✅
- `test_session_b_to_a_upgrade_sends_update_alert` ✅
- `test_session_score_improvement_sends_update_alert` ✅
- `test_session_records_dry_run_status_when_telegram_disabled` ✅

## Remaining failures

**None.** Full suite: `pytest -q` → **419 passed, 0 failed** in 95.5s
(previously 404 passed / **6 failed** — exactly the six listed above). No
unrelated failures remain.

## Safety checklist

- ✅ No scoring / threshold / strategy change.
- ✅ No production alert / cooldown / dedup logic change (logic unchanged; tests
  now exercise it against a clean DB).
- ✅ No production code changed (tests-only).
- ✅ No production DB writes by the fixed tests (proven above).
- ✅ No production data deleted.
- ✅ No auto-trade.
