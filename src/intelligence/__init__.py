"""Shadow Intelligence Layer (2026-06-18).

Five shadow/diagnostic modules — symbol timeline memory, derivatives trajectory,
squeeze phase classifier, thesis/invalidation formatter, on-chain risk — plus an
aggregator. EVERYTHING here is diagnostic/add-only: it never changes trades,
routing, scoring, TP/SL, size, leverage, or exits, and never blocks the alert path
(the aggregator reads only pre-computed local caches; heavy/external work runs in
background scheduler scripts). All entry points fail open to 'unknown'/'unavailable'.
"""
