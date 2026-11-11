"""One-time Telethon authorization for crypto-ai-desk.

Creates a *separate* session file from any other Telegram-enabled project on
this machine (the news_trader project lives under
``C:/Users/adama/Documents/zeph ai projects/news_trader`` and uses
``news_trader_tg.session`` — we deliberately do NOT touch it).

Usage
-----
1. Put TG_API_ID and TG_API_HASH into ``.env`` at the project root::

       TG_API_ID=123456
       TG_API_HASH=abc...

   Obtain both at https://my.telegram.org.

2. Run::

       py -3 scripts/setup_telegram_auth.py

   Telegram will send a login code to your *Telegram app* (NOT SMS). Paste it
   into the console. If 2FA is enabled, you will also be prompted for your
   cloud password.

3. On success the script writes a host-specific session under
   ``data/telegram`` and exits. After that the
   collector module (``src.data_collectors.telegram_collector``) and the
   runner (``scripts/run_telegram_collector.py``) can connect non-interactively.

The script never:
    - prompts for a phone number you didn't enter
    - reads or writes any file under the news_trader directory
    - logs your API hash or auth code

If something goes wrong (wrong code, FloodWait, expired session etc.) you can
re-run the script — it is idempotent.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# .env loader is optional — fall back to plain environment vars.
try:  # pragma: no cover - import-time tolerance
    from dotenv import load_dotenv
except Exception:  # noqa: BLE001
    def load_dotenv(*_a, **_kw):  # type: ignore
        return False


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _session_target() -> tuple[Path, str]:
    sys.path.insert(0, str(PROJECT_ROOT))
    from src.config import load_config
    from src.data_collectors.telegram_collector import TelegramCollectorSettings

    cfg = load_config(PROJECT_ROOT)
    settings = TelegramCollectorSettings.from_sources_yaml(cfg.sources)
    return (PROJECT_ROOT / settings.session_path).resolve(), settings.session_name


async def _run() -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    api_id_raw = os.getenv("TG_API_ID", "").strip()
    api_hash = os.getenv("TG_API_HASH", "").strip()
    if not api_id_raw or not api_hash:
        print(
            "ERROR: TG_API_ID / TG_API_HASH not set in .env.\n"
            "Get them at https://my.telegram.org and put them into "
            f"{PROJECT_ROOT / '.env'}.",
            file=sys.stderr,
        )
        return 2
    try:
        api_id = int(api_id_raw)
    except ValueError:
        print(f"ERROR: TG_API_ID must be an integer, got {api_id_raw!r}", file=sys.stderr)
        return 2

    try:
        from telethon import TelegramClient
    except ImportError:
        print("ERROR: telethon not installed. `pip install telethon`.", file=sys.stderr)
        return 3

    session_dir, session_name = _session_target()
    session_dir.mkdir(parents=True, exist_ok=True)
    session_path = session_dir / session_name
    print(f"[setup] session file: {session_path}.session")

    phone = input("Phone number (international format, e.g. +491234567890): ").strip()
    if not phone:
        print("ERROR: phone number required", file=sys.stderr)
        return 2

    client = TelegramClient(str(session_path), api_id, api_hash)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(
            f"[setup] already authorized as @{getattr(me, 'username', '?') or '?'} "
            f"(id={getattr(me, 'id', '?')}). Session is ready."
        )
        await client.disconnect()
        return 0

    try:
        await client.send_code_request(phone)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: failed to request login code: {exc}", file=sys.stderr)
        await client.disconnect()
        return 4

    code = input("Telegram code (sent to your Telegram app): ").strip()
    try:
        await client.sign_in(phone=phone, code=code)
    except Exception as exc:  # noqa: BLE001
        # Most likely a 2FA password is required.
        msg = str(exc).lower()
        if "password" in msg or "2fa" in msg or "two-step" in msg:
            import getpass
            pwd = getpass.getpass("2FA cloud password: ")
            try:
                await client.sign_in(password=pwd)
            except Exception as exc2:  # noqa: BLE001
                print(f"ERROR: 2FA sign-in failed: {exc2}", file=sys.stderr)
                await client.disconnect()
                return 5
        else:
            print(f"ERROR: sign-in failed: {exc}", file=sys.stderr)
            await client.disconnect()
            return 5

    me = await client.get_me()
    print(
        f"[setup] authorized as @{getattr(me, 'username', '?') or '?'} "
        f"(id={getattr(me, 'id', '?')}). Session saved."
    )
    await client.disconnect()
    return 0


def main() -> int:
    try:
        return asyncio.run(_run())
    except KeyboardInterrupt:
        print("\n[setup] aborted by user")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
