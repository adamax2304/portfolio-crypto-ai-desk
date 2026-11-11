from __future__ import annotations


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}%"


def fmt_float(value: float | None, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if abs(value) >= 100:
        digits = min(digits, 2)
    elif abs(value) >= 1:
        digits = min(digits, 3)
    return f"{value:.{digits}f}"


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- n/a"
    return "\n".join(f"- {item}" for item in items)
