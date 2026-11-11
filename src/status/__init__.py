"""Display/status semantics layer (read-only).

Pure presentation helpers that translate raw lifecycle fields into operator-facing
display states. NOTHING here changes trading logic, scoring, TP/SL, routing,
actionability, or any stored outcome — it only *describes* what already happened.
"""

from src.status.display_status import (  # noqa: F401
    DISPLAY_GROUPS,
    derive_display_status,
    format_r_with_lifecycle,
    summarize_display_states,
    format_paper_monitor_status,
)
