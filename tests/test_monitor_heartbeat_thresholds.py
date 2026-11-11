from datetime import datetime, timezone

from scripts import monitor_heartbeat


def test_oversized_worker_log_is_compressed_and_retained(tmp_path):
    import gzip

    log = tmp_path / "worker.log"
    payload = ("repeated diagnostic line\n" * 200).encode()
    log.write_bytes(payload)

    archive = monitor_heartbeat._rotate_process_log(log, max_bytes=100)

    assert archive is not None and archive.exists()
    assert not log.exists()
    with gzip.open(archive, "rb") as handle:
        assert handle.read() == payload


def test_latest_append_only_timestamp_uses_primary_key_order(tmp_path):
    import sqlite3

    db = tmp_path / "health.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE events(id INTEGER PRIMARY KEY, received_at TEXT)")
        conn.execute("INSERT INTO events(received_at) VALUES('2099-01-01T00:00:00+00:00')")
        conn.execute("INSERT INTO events(received_at) VALUES('2026-08-30T00:00:00+00:00')")
    assert monitor_heartbeat._db_latest(
        db, "events", "received_at"
    ) == "2026-08-30T00:00:00+00:00"


def test_preus_review_health_detects_missing_structured_handoff(tmp_path, monkeypatch):
    import sqlite3
    from datetime import datetime, timezone

    db = tmp_path / "preus.sqlite"
    conn = sqlite3.connect(db)
    conn.executescript("""
      CREATE TABLE stocks_preus_review_health (
        session_date TEXT PRIMARY KEY, checked_at TEXT, eligible_count INTEGER,
        reviewed_count INTEGER, missing_count INTEGER, status TEXT, reason TEXT
      );
      INSERT INTO stocks_preus_review_health VALUES (
        '2026-08-18','2026-08-18T13:05:00+00:00',3,0,3,'REVIEW_MISSING',
        'no_fresh_structured_preus_review'
      );
    """)
    conn.commit(); conn.close()
    monkeypatch.setattr(monitor_heartbeat, "_preus_llm_review_enabled", lambda: True)
    now = datetime(2026, 8, 18, 14, 0, tzinfo=timezone.utc)  # 10:00 ET
    status = monitor_heartbeat.preus_review_health(db=db, now=now)
    assert status["expected"] is True
    assert status["status"] == "REVIEW_MISSING"
    assert status["overnight_plan_count"] == 3
    assert status["missing_count"] == 3


def test_preus_review_health_accepts_ready_current_session_handoff(tmp_path, monkeypatch):
    import sqlite3
    from datetime import datetime, timezone

    db = tmp_path / "preus.sqlite"
    conn = sqlite3.connect(db)
    conn.executescript("""
      CREATE TABLE stocks_preus_review_health (
        session_date TEXT PRIMARY KEY, checked_at TEXT, eligible_count INTEGER,
        reviewed_count INTEGER, missing_count INTEGER, status TEXT, reason TEXT
      );
      INSERT INTO stocks_preus_review_health VALUES (
        '2026-08-18','2026-08-18T13:04:00+00:00',2,2,0,'READY',NULL
      );
    """)
    conn.commit(); conn.close()
    monkeypatch.setattr(monitor_heartbeat, "_preus_llm_review_enabled", lambda: True)
    now = datetime(2026, 8, 18, 14, 0, tzinfo=timezone.utc)
    assert monitor_heartbeat.preus_review_health(db=db, now=now)["status"] == "READY"


def test_preus_llm_review_health_is_not_expected_when_disabled(tmp_path, monkeypatch):
    import sqlite3

    db = tmp_path / "preus.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE stocks_preus_review_health ("
            "session_date TEXT PRIMARY KEY, checked_at TEXT, eligible_count INTEGER,"
            "reviewed_count INTEGER, missing_count INTEGER, status TEXT, reason TEXT)"
        )
    monkeypatch.setattr(monitor_heartbeat, "_preus_llm_review_enabled", lambda: False)
    now = datetime(2026, 8, 18, 14, 0, tzinfo=timezone.utc)

    status = monitor_heartbeat.preus_review_health(db=db, now=now)

    assert status["expected"] is False
    assert status["status"] == "NOT_DUE"


def test_preus_baseline_window_is_new_york_based(tmp_path, monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "ROOT", tmp_path)
    now = datetime(2026, 8, 18, 12, 52, tzinfo=timezone.utc)  # 08:52 ET

    status = monitor_heartbeat.ensure_preus_baseline(now=now, auto_start=False)

    assert status["session_date"] == "2026-08-18"
    assert status["in_window"] is True
    assert status["action"] == "pending_window"


def test_derived_refresh_sla_exceeds_mid_cycle_watchdog_window():
    assert monitor_heartbeat.DERIVED_GRACE_MIN > monitor_heartbeat.GRACE_MIN
    assert (
        monitor_heartbeat.INTERVAL_MIN + monitor_heartbeat.DERIVED_GRACE_MIN
    ) == 210


def test_mexc_canary_heartbeat_window_allows_normal_api_retry_stalls():
    assert monitor_heartbeat.MEXC_CANARY_HEARTBEAT_GRACE_SEC == 120


def test_new_monitor_gets_startup_grace_before_replacement(monkeypatch):
    monkeypatch.setattr(
        monitor_heartbeat, "_monitor_startup_age_seconds", lambda _status: 45.0
    )
    assert monitor_heartbeat._monitor_is_starting({"pids": [123]}) is True


def test_old_monitor_does_not_hide_behind_startup_grace(monkeypatch):
    monkeypatch.setattr(
        monitor_heartbeat, "_monitor_startup_age_seconds", lambda _status: 600.0
    )
    assert monitor_heartbeat._monitor_is_starting({"pids": [123]}) is False


def test_mexc_canary_autostart_does_not_duplicate_live_monitor(monkeypatch):
    from src.live_execution import config as mexc_config

    class DummyCfg:
        execution_mode = "live"
        submission_enabled = True

    monkeypatch.setattr(mexc_config, "load_live_canary_config", lambda: DummyCfg())
    monkeypatch.setattr(
        monitor_heartbeat,
        "mexc_canary_monitor_status",
        lambda: {"alive": True, "pids": [123, 456]},
    )
    monkeypatch.setattr(
        monitor_heartbeat.subprocess,
        "Popen",
        lambda *_, **__: (_ for _ in ()).throw(AssertionError("must not start duplicate")),
    )

    started, message = monitor_heartbeat.start_mexc_canary_monitor()

    assert started is False
    assert message == "MEXC monitor already running pid=123,456"


def test_mexc_stale_live_process_is_replaced_before_restart(monkeypatch):
    status = {"alive": True, "pids": [123], "heartbeat_age_seconds": 999}
    monkeypatch.setattr(
        monitor_heartbeat, "_stop_exact_monitor_processes",
        lambda pids, marker: [123] if pids == [123] and marker == "mexc-canary-monitor" else [],
    )
    monkeypatch.setattr(monitor_heartbeat, "_orphan_monitor_lock", lambda *_: None)
    monkeypatch.setattr(monitor_heartbeat, "_wait_for_processes_stopped", lambda *_: True)
    monkeypatch.setattr(
        monitor_heartbeat, "start_mexc_canary_monitor",
        lambda: (True, "started MEXC canary standby pid=456"),
    )

    started, message = monitor_heartbeat.restart_mexc_canary_monitor(status)

    assert started is True
    assert message.endswith("pid=456")


def test_mexc_restart_waits_for_old_pid_to_disappear(monkeypatch):
    status = {"alive": True, "pids": [123], "heartbeat_age_seconds": 999}
    monkeypatch.setattr(
        monitor_heartbeat, "_stop_exact_monitor_processes", lambda *_: [123]
    )
    monkeypatch.setattr(
        monitor_heartbeat, "_wait_for_processes_stopped", lambda *_: False
    )
    monkeypatch.setattr(
        monitor_heartbeat,
        "start_mexc_canary_monitor",
        lambda: (_ for _ in ()).throw(AssertionError("must wait before replacement")),
    )

    started, message = monitor_heartbeat.restart_mexc_canary_monitor(status)

    assert started is False
    assert "still terminating" in message


def test_mexc_duplicate_cleanup_preserves_verified_leader(monkeypatch):
    status = {"pids": [101, 202, 303], "leader_pid": 202}
    monkeypatch.setattr(
        monitor_heartbeat,
        "_stop_exact_monitor_processes",
        lambda pids, marker: pids if pids == [101, 303] and marker == "mexc-canary-monitor" else [],
    )

    result = monitor_heartbeat.prune_mexc_canary_duplicates(status)

    assert result["status"] == "OK"
    assert result["leader_pid"] == 202
    assert result["stopped"] == [101, 303]
    assert result["remaining"] == [202]


def test_duplicate_cleanup_refuses_without_verified_leader(monkeypatch):
    monkeypatch.setattr(
        monitor_heartbeat,
        "_stop_exact_monitor_processes",
        lambda *_: (_ for _ in ()).throw(AssertionError("must not kill unverified processes")),
    )

    result = monitor_heartbeat.prune_mexc_canary_duplicates(
        {"pids": [101, 202], "leader_pid": 999}
    )

    assert result["status"] == "SKIPPED_NO_VERIFIED_LEADER"
    assert result["stopped"] == []


def test_derivatives_duplicate_cleanup_preserves_lock_owner(monkeypatch):
    status = {"pids": [11, 22], "leader_pid": 22}
    monkeypatch.setattr(
        monitor_heartbeat,
        "_stop_exact_monitor_processes",
        lambda pids, marker: [11]
        if pids == [11] and marker == "scripts.derivatives_monitor" else [],
    )

    result = monitor_heartbeat.prune_derivatives_monitor_duplicates(status)

    assert result["status"] == "OK"
    assert result["remaining"] == [22]


def test_pending_monitor_watchdog_starts_missing_fast_worker(monkeypatch):
    monkeypatch.setattr(
        monitor_heartbeat, "pending_monitor_status",
        lambda: {"alive": False, "pids": [], "required": True},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "start_pending_monitor",
        lambda: (True, "started pending monitor pid=321"),
    )

    status = monitor_heartbeat.ensure_pending_monitor(auto_start=True)

    assert status["alive"] is True
    assert status["action"] == "started"
    assert status["message"] == "started pending monitor pid=321"


def test_pending_monitor_watchdog_does_not_duplicate_worker(monkeypatch):
    monkeypatch.setattr(
        monitor_heartbeat, "pending_monitor_status",
        lambda: {"alive": True, "pids": [321], "required": True},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "start_pending_monitor",
        lambda: (_ for _ in ()).throw(AssertionError("must not start duplicate")),
    )

    status = monitor_heartbeat.ensure_pending_monitor(auto_start=True)

    assert status["alive"] is True
    assert status["action"] == "healthy"


def test_pending_monitor_watchdog_replaces_stalled_worker(monkeypatch):
    stale = {"alive": True, "pids": [321], "required": True, "lease_fresh": False}
    monkeypatch.setattr(monitor_heartbeat, "pending_monitor_status", lambda: stale.copy())
    monkeypatch.setattr(
        monitor_heartbeat, "restart_pending_monitor",
        lambda status: (True, "started pending monitor pid=654"),
    )

    status = monitor_heartbeat.ensure_pending_monitor(auto_start=True)

    assert status["alive"] is True
    assert status["lease_fresh"] is True
    assert status["action"] == "restarted"


def test_pending_monitor_heartbeat_window_allows_a_heavy_refresh_tick():
    assert monitor_heartbeat.PENDING_MONITOR_LEASE_GRACE_SEC == 300


def test_live_worker_environment_restores_user_scoped_arm_values(monkeypatch):
    from src.live_execution import config as mexc_config

    class DummyCfg:
        def credential_names(self):
            return ("ACCESS_ENV", "SECRET_ENV", "ARM_ENV", "ARM_VALUE")

        def bybit_credential_names(self):
            return ("BYBIT_ACCESS_ENV", "BYBIT_SECRET_ENV", "BYBIT_ARM_ENV", "BYBIT_ARM_VALUE")

    monkeypatch.setattr(mexc_config, "load_live_canary_config", lambda: DummyCfg())
    monkeypatch.delenv("ACCESS_ENV", raising=False)
    monkeypatch.delenv("SECRET_ENV", raising=False)
    monkeypatch.delenv("ARM_ENV", raising=False)
    monkeypatch.delenv("BYBIT_ACCESS_ENV", raising=False)
    monkeypatch.delenv("BYBIT_SECRET_ENV", raising=False)
    monkeypatch.delenv("BYBIT_ARM_ENV", raising=False)
    monkeypatch.setattr(
        monitor_heartbeat, "_read_user_environment",
        lambda name: {
            "ACCESS_ENV": "a", "SECRET_ENV": "s", "ARM_ENV": "armed",
            "BYBIT_ACCESS_ENV": "ba", "BYBIT_SECRET_ENV": "bs",
            "BYBIT_ARM_ENV": "bybit-armed",
        }.get(name, ""),
    )

    env = monitor_heartbeat._live_canary_child_environment()

    assert env["ACCESS_ENV"] == "a"
    assert env["SECRET_ENV"] == "s"
    assert env["ARM_ENV"] == "armed"
    assert env["BYBIT_ACCESS_ENV"] == "ba"
    assert env["BYBIT_SECRET_ENV"] == "bs"
    assert env["BYBIT_ARM_ENV"] == "bybit-armed"


def test_stocks_worker_environment_prefers_current_user_scoped_alpaca_values(monkeypatch):
    names = {
        "ALPACA_API_KEY": "new-user-key",
        "ALPACA_API_SECRET": "new-user-secret",
        "ALPACA_DATA_BASE_URL": "https://data.alpaca.markets/v2",
        "ALPACA_TRADING_BASE_URL": "https://paper-api.alpaca.markets/v2",
    }
    for name in names:
        monkeypatch.setenv(name, "stale-process-value")
    monkeypatch.setattr(
        monitor_heartbeat, "_read_user_environment",
        lambda name: names.get(name, ""),
    )

    env = monitor_heartbeat._stocks_market_data_child_environment()

    assert {name: env[name] for name in names} == names


def test_stock_worker_window_is_new_york_based_and_starts_before_preopen():
    window = monitor_heartbeat.stock_worker_window(
        datetime(2026, 8, 4, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    )
    assert window["trading_day"] is True
    assert window["coverage_expected"] is True
    assert window["preopen_control"] is True


def test_stock_worker_window_skips_weekends():
    window = monitor_heartbeat.stock_worker_window(
        datetime(2026, 8, 8, 13, 0, tzinfo=timezone.utc)
    )
    assert window["trading_day"] is False
    assert window["coverage_expected"] is False


def test_preopen_rollover_detects_yesterday_worker():
    window = monitor_heartbeat.stock_worker_window(
        datetime(2026, 8, 5, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    )
    status = {"processes": [{"pid": 123, "created_at": "2026-08-04T17:53:00+00:00"}]}
    assert monitor_heartbeat._stock_monitor_started_before_session(status, window) is True


def test_telegram_collector_is_started_when_enabled_and_missing(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_reauth_required", lambda: False)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": False, "pids": []},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "start_telegram_collector",
        lambda: (True, "started Telegram collector pid=123"),
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status["required"] is True
    assert status["action"] == "started"
    assert status["message"] == "started Telegram collector pid=123"


def test_telegram_collector_starts_public_fallback_for_revoked_session(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_reauth_required", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_public_fallback_enabled", lambda: True)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": False, "pids": []},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "start_telegram_collector",
        lambda: (True, "started Telegram public fallback"),
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status["action"] == "fallback_started"


def test_telegram_collector_restarts_when_public_fallback_is_stale(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_reauth_required", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_public_fallback_enabled", lambda: True)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": True, "pids": [321]},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_public_fallback_status",
        lambda: {"fresh": False, "age_seconds": 900},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "restart_telegram_collector",
        lambda status: (True, "started Telegram collector pid=654"),
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status["action"] == "fallback_restarted"
    assert status["message"].endswith("pid=654")


def test_telegram_collector_restarts_stale_known_fallback_after_reauth_row_expires(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: True)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_reauth_required", lambda: False)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_public_fallback_enabled", lambda: True)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": True, "pids": [321]},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_public_fallback_status",
        lambda: {"available": True, "last_completed_at": "2026-08-30T00:00:00+00:00",
                 "fresh": False, "age_seconds": 900},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "restart_telegram_collector",
        lambda status: (True, "started Telegram collector pid=654"),
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status["action"] == "fallback_restarted"


def test_telegram_collector_labels_a_fresh_public_cycle_as_fallback(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: True)
    # Historical collector-error rows can be retired while the public fallback
    # remains active, so the completed fallback cycle is the runtime evidence.
    monkeypatch.setattr(monitor_heartbeat, "_telegram_reauth_required", lambda: False)
    monkeypatch.setattr(monitor_heartbeat, "_telegram_public_fallback_enabled", lambda: True)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": True, "pids": [321]},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_public_fallback_status",
        lambda: {"fresh": True, "age_seconds": 100},
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status["action"] == "fallback_healthy"


def test_telegram_public_fallback_status_uses_completed_cycle_freshness(tmp_path):
    import sqlite3

    db = tmp_path / "news.sqlite"
    conn = sqlite3.connect(db)
    conn.executescript("""
      CREATE TABLE news_source_runs (
        id INTEGER PRIMARY KEY, source_name TEXT, status TEXT,
        finished_at TEXT, item_count INTEGER
      );
      INSERT INTO news_source_runs VALUES (
        1, 'collector_public_html', 'ok', '2026-08-28T00:00:00+00:00', 3
      );
    """)
    conn.commit()
    conn.close()

    status = monitor_heartbeat.telegram_public_fallback_status(
        db=db,
        now=datetime(2026, 8, 28, 0, 5, tzinfo=timezone.utc),
    )

    assert status["available"] is True
    assert status["fresh"] is True
    assert status["age_seconds"] == 300.0


def test_telegram_collector_is_not_started_when_disabled(monkeypatch):
    monkeypatch.setattr(monitor_heartbeat, "_telegram_collector_enabled", lambda: False)
    monkeypatch.setattr(
        monitor_heartbeat, "telegram_collector_status",
        lambda: {"alive": False, "pids": []},
    )
    monkeypatch.setattr(
        monitor_heartbeat, "start_telegram_collector",
        lambda: (_ for _ in ()).throw(AssertionError("must not start")),
    )

    status = monitor_heartbeat.ensure_telegram_collector(auto_start=True)

    assert status == {
        "alive": False, "pids": [], "required": False, "action": "not_required"
    }
