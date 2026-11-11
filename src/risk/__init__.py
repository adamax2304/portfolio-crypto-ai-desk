"""Risk-guard diagnostics (alert-only / shadow-only).

Everything in this package is DIAGNOSTIC: it computes labels, flags, and
"would_*" counterfactuals. It must never block a trade, change size, change
routing, change scoring, or change TP/SL. All entry points fail open (return a
neutral/ok state) so they can never break a monitor/tracking loop.
"""
