"""Paper / accounting execution models (PAPER-ONLY).

This package holds derived execution-accounting logic only. It NEVER places real
orders, never touches live/exchange execution, and never rewrites historical
`signal_outcomes.final_r`. See `paper_execution_accounting.py`.
"""
