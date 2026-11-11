"""Shadow exit measurement (FAST SAFE ACCELERATION).

Computes what alternative exit rules (BE / partial / trailing / candle-close /
re-entry) WOULD have produced, candle-by-candle, for measurement only. It NEVER
changes real exits, never enables partial_exit_model, never mutates actual
outcomes. Every result is shadow.
"""
