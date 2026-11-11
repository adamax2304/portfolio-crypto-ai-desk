"""Small deterministic helpers for preserving and fingerprinting news content."""
from __future__ import annotations

import hashlib
import html
import re


def clean_text(value: object, *, limit: int = 12000) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def content_hash(title: object, body: object = "") -> str:
    normalized = "\n".join((clean_text(title).lower(), clean_text(body).lower())).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
