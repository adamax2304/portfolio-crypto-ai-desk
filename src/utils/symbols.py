from __future__ import annotations


def normalize_symbol(symbol: str) -> str:
    value = symbol.strip().upper().replace("-", "/")
    if "/" not in value and value.endswith("USDT"):
        value = f"{value[:-4]}/USDT"
    return value


def symbol_to_filename(symbol: str) -> str:
    return normalize_symbol(symbol).replace("/", "_")


def symbol_to_ticker(symbol: str) -> str:
    return normalize_symbol(symbol).split("/")[0]


def symbol_to_exchange_symbol(symbol: str) -> str:
    return normalize_symbol(symbol).replace("/", "")


def filename_to_symbol(filename_stem: str) -> str:
    return filename_stem.replace("_", "/").upper()
