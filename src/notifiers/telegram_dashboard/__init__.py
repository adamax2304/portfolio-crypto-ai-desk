"""Read-only Telegram dashboard for Paper and Shadow observability.

The dashboard deliberately lives outside every trading path.  It reads the
desk SQLite database in read-only mode and persists Telegram cursor/message
metadata in a small JSON file under ``data/telegram``.
"""

from .service import TelegramDashboardService

__all__ = ["TelegramDashboardService"]
