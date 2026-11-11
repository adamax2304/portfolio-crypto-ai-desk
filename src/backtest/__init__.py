"""Backtest / offline-replay package.

Everything here is READ-MODEL / PAPER only. It sources deep OHLCV history from a
SEPARATE store (``data/history/ohlcv/...``) so the live rolling cache and the
live collectors are never touched, and it never writes to ``proposed_signals``,
``signal_outcomes`` / ``final_r`` or any live execution path.

The purpose is Move 1 of the backtest-acceleration plan: compress the *settings*
dimension (Model-F protection params, entry-mode fill mechanics, stop/TP/RR
geometry, fee sensitivity) from months of forward waiting to hours of replay,
by re-running the existing sweep variants over the FULL signal history on real
deep price paths. Signals are real; only their handling is varied — so this is
not look-ahead for the settings question. It does NOT replace the forward-only
promotion gate (which stays forward + post-fee + positive + sign-off).
"""
