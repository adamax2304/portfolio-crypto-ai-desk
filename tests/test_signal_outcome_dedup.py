from src.storage.sqlite import SQLiteStore


def test_signal_outcome_snapshot_is_only_appended_when_state_changes(tmp_path):
    store = SQLiteStore(tmp_path / "outcomes.sqlite")
    store.init_db()
    first = {
        "signal_id": "sig-dedup",
        "checked_at": "2026-10-02T01:00:00+00:00",
        "status": "waiting_for_entry",
        "entry_triggered": 0,
        "final_r": 0.0,
        "final_outcome": "not_triggered",
        "notes": "confirmation pending",
    }

    first_id = store.add_signal_outcome_if_changed(first)
    repeated_id = store.add_signal_outcome_if_changed(
        {**first, "checked_at": "2026-10-02T01:00:15+00:00"}
    )

    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == 1
    assert repeated_id == first_id

    changed_id = store.add_signal_outcome_if_changed({
        **first,
        "checked_at": "2026-10-02T01:01:00+00:00",
        "notes": "confirmation pending; closed bars seen=1",
    })
    terminal_id = store.add_signal_outcome_if_changed({
        **first,
        "checked_at": "2026-10-02T01:02:00+00:00",
        "status": "stopped",
        "entry_triggered": 1,
        "final_r": -1.0,
        "final_outcome": "loss",
        "notes": "confirmed then stopped",
    })
    repeated_terminal_id = store.add_signal_outcome_if_changed({
        **first,
        "checked_at": "2026-10-02T01:02:15+00:00",
        "status": "stopped",
        "entry_triggered": 1,
        "entry_triggered_at": "2026-10-02T01:02:15+00:00",
        "entry_price_used": 101.25,
        "final_r": -1.0,
        "final_outcome": "loss",
        "notes": "confirmed then stopped",
    })

    with store.connect() as conn:
        rows = conn.execute(
            "SELECT id, status FROM signal_outcomes ORDER BY id"
        ).fetchall()
    assert [tuple(row) for row in rows] == [
        (first_id, "waiting_for_entry"),
        (changed_id, "waiting_for_entry"),
        (terminal_id, "stopped"),
    ]
    assert repeated_terminal_id == terminal_id
