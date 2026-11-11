"""SEC Form 4 open-market purchase context for the Stocks Position Framework."""
from __future__ import annotations

import csv
import io
import json
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import yaml

from src.data_collectors import market_intelligence_store as mi
from src.intelligence.context_config import ROOT, section
from src.intelligence.context_store import connect, insert_named


INSIDER_COLS = (
    "accession_number", "filing_at", "transaction_at", "issuer_cik", "ticker",
    "owner_cik", "owner_name", "owner_relationship", "owner_title", "transaction_code",
    "acquired_disposed", "shares", "price_per_share", "transaction_value_usd",
    "shares_owned_after", "direct_indirect", "is_10b5_1", "source", "raw_json",
)


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _flag(value: Any) -> int:
    return int(str(value or "").strip().lower() in {"1", "y", "yes", "true"})


def _universe() -> set[str]:
    path = ROOT / "config" / "stocks" / "universe.yaml"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        raw = {}
    return {str(x).upper() for x in raw.get("default_symbols", [])}


def _tsv(zf: zipfile.ZipFile, name: str):
    with zf.open(name) as raw:
        wrapper = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        yield from csv.DictReader(wrapper, delimiter="\t")


def parse_bulk_zip(content: bytes, *, universe: set[str] | None = None) -> list[dict[str, Any]]:
    universe = {x.upper() for x in universe} if universe else None
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        submissions: dict[str, dict[str, Any]] = {}
        for row in _tsv(zf, "SUBMISSION.tsv"):
            ticker = str(row.get("ISSUERTRADINGSYMBOL") or "").upper().strip()
            doc = str(row.get("DOCUMENT_TYPE") or "").upper()
            if not ticker or (universe is not None and ticker not in universe) or doc not in {"4", "4/A"}:
                continue
            accession = str(row.get("ACCESSION_NUMBER") or "")
            submissions[accession] = {"ticker": ticker, "filing_at": row.get("FILING_DATE"),
                                      "issuer_cik": row.get("ISSUERCIK"),
                                      "is_10b5_1": _flag(row.get("AFF10B5ONE")), "submission": row}
        owners: dict[str, list[dict[str, Any]]] = {}
        for row in _tsv(zf, "REPORTINGOWNER.tsv"):
            accession = str(row.get("ACCESSION_NUMBER") or "")
            if accession in submissions:
                owners.setdefault(accession, []).append(row)
        output: list[dict[str, Any]] = []
        for tx in _tsv(zf, "NONDERIV_TRANS.tsv"):
            accession = str(tx.get("ACCESSION_NUMBER") or "")
            sub = submissions.get(accession)
            if not sub or str(tx.get("TRANS_CODE") or "").upper() != "P":
                continue
            acquired = str(tx.get("TRANS_ACQUIRED_DISP_CD") or "").upper()
            if acquired and acquired != "A":
                continue
            shares, price = _f(tx.get("TRANS_SHARES")), _f(tx.get("TRANS_PRICEPERSHARE"))
            value = shares * price if shares is not None and price is not None else None
            for owner in owners.get(accession) or [{}]:
                relationship = str(owner.get("RPTOWNER_RELATIONSHIP") or "")
                output.append({
                    "accession_number": accession, "filing_at": sub.get("filing_at"),
                    "transaction_at": tx.get("TRANS_DATE"), "issuer_cik": sub.get("issuer_cik"),
                    "ticker": sub["ticker"], "owner_cik": owner.get("RPTOWNERCIK"),
                    "owner_name": owner.get("RPTOWNERNAME"), "owner_relationship": relationship,
                    "owner_title": owner.get("RPTOWNER_TITLE"), "transaction_code": "P",
                    "acquired_disposed": acquired or "A", "shares": shares, "price_per_share": price,
                    "transaction_value_usd": value,
                    "shares_owned_after": _f(tx.get("SHRS_OWND_FOLWNG_TRANS")),
                    "direct_indirect": tx.get("DIRECT_INDIRECT_OWNERSHIP"),
                    "is_10b5_1": sub.get("is_10b5_1", 0), "source": "SEC_FORM345_BULK",
                    "raw_json": {"submission": sub.get("submission"), "owner": owner, "transaction": tx},
                })
        return output


def _quarter_pairs(now: datetime, count: int) -> list[tuple[int, int]]:
    year, quarter = now.year, (now.month - 1) // 3 + 1
    out = []
    for _ in range(count):
        out.append((year, quarter))
        quarter -= 1
        if quarter == 0:
            year, quarter = year - 1, 4
    return out


def _download(year: int, quarter: int) -> tuple[bytes, str]:
    names = [
        f"https://www.sec.gov/files/datastandardsinnovation/data/insider-transactions-data-sets/{year}q{quarter}_form345.zip",
        f"https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{year}q{quarter}_form345.zip",
    ]
    last_error = "unavailable"
    headers = {"User-Agent": "crypto-ai-desk research admin@example.com"}
    for url in names:
        try:
            response = requests.get(url, timeout=60, headers=headers)
            if response.status_code == 200 and response.content.startswith(b"PK"):
                return response.content, url
            last_error = f"http_{response.status_code}"
        except Exception as exc:
            last_error = type(exc).__name__
    raise RuntimeError(last_error)


def refresh(*, db_path=None, now: datetime | None = None, backfill: bool = False) -> dict[str, Any]:
    cfg = section("insider_confirmation")
    now = now or datetime.now(timezone.utc)
    count = int(cfg.get("history_years", 3)) * 4 if backfill else 1
    rows = written = downloaded = 0
    errors: list[str] = []
    skipped_unpublished: list[str] = []
    # The current quarter file is often not published yet. Walk back until the
    # requested number of available datasets has been imported.
    for year, quarter in _quarter_pairs(now, count + 1):
        if downloaded >= count:
            break
        try:
            content, url = _download(year, quarter)
            downloaded += 1
            parsed = parse_bulk_zip(content, universe=_universe())
            rows += len(parsed)
            with connect(db_path) as conn:
                for row in parsed:
                    written += int(insert_named(conn, "insider_transactions", row, INSIDER_COLS))
                conn.commit()
        except Exception as exc:
            if "http_404" in str(exc):
                skipped_unpublished.append(f"{year}q{quarter}")
            else:
                errors.append(f"{year}q{quarter}:{type(exc).__name__}:{exc}")
    with connect(db_path) as conn:
        mi.record_source_health(conn, "context:sec_form4_bulk", status="ok" if downloaded else "error",
                                success=bool(downloaded), records_written=written,
                                latest_provider_ts=now.isoformat() if downloaded else None,
                                error=";".join(errors) or None,
                                details={"quarters": count, "parsed": rows, "backfill": backfill,
                                         "skipped_unpublished": skipped_unpublished})
        conn.commit()
    return {"at": now.isoformat(), "quarters": count, "downloaded": downloaded,
            "rows": rows, "written": written,
            "errors": errors, "skipped_unpublished": skipped_unpublished}


def _is_routine(conn, owner_cik: str, tx_at: datetime, years: int) -> bool:
    if not owner_cik:
        return False
    prior = conn.execute(
        "SELECT transaction_at FROM insider_transactions WHERE owner_cik=? AND transaction_code='P' "
        "AND transaction_at<? ORDER BY transaction_at", (owner_cik, tx_at.date().isoformat()),
    ).fetchall()
    months = set()
    for row in prior:
        try:
            dt = datetime.fromisoformat(str(row[0])[:10])
            months.add((dt.year, dt.month))
        except (TypeError, ValueError):
            continue
    return all((tx_at.year - offset, tx_at.month) in months for offset in range(1, years + 1))


def ticker_context(ticker: str, *, as_of: datetime | None = None, db_path=None,
                   cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or section("insider_confirmation")
    now = as_of or datetime.now(timezone.utc)
    start = now - timedelta(days=float(cfg.get("cluster_window_days", 30)))
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM insider_transactions WHERE ticker=? AND filing_at<=? AND filing_at>=? "
            "AND transaction_code=? ORDER BY filing_at,transaction_at",
            (str(ticker).upper(), now.date().isoformat(), start.date().isoformat(),
             str(cfg.get("require_transaction_code", "P"))),
        ).fetchall()
        valid = []
        for raw in rows:
            item = dict(raw)
            if cfg.get("exclude_10b5_1", True) and int(item.get("is_10b5_1") or 0):
                continue
            try:
                tx_at = datetime.fromisoformat(str(item.get("transaction_at"))[:10])
            except (TypeError, ValueError):
                continue
            item["routine"] = _is_routine(conn, str(item.get("owner_cik") or ""), tx_at,
                                            int(cfg.get("history_years", 3)))
            valid.append(item)
    owners = {str(x.get("owner_cik") or x.get("owner_name") or "") for x in valid}
    total = sum(float(x.get("transaction_value_usd") or 0.0) for x in valid)
    opportunistic = [x for x in valid if not x.get("routine")]
    qualifies = (len(owners) >= int(cfg.get("min_cluster_insiders", 2))
                 and total >= float(cfg.get("min_total_purchase_usd", 50000))
                 and bool(opportunistic))
    return {"status": "ok" if valid else "unknown", "ticker": str(ticker).upper(),
            "cluster_confirmed": qualifies, "unique_insiders": len(owners),
            "purchase_value_usd": round(total, 2), "purchase_count": len(valid),
            "opportunistic_purchase_count": len(opportunistic), "window_start": start.isoformat(),
            "context_ts": max((str(x.get("filing_at")) for x in valid), default=None),
            "paper_routing_enabled": bool(cfg.get("paper_routing_enabled", False)),
            "reason": "insider_cluster_confirmed" if qualifies else "no_qualified_insider_cluster"}


__all__ = ["refresh", "ticker_context", "parse_bulk_zip", "INSIDER_COLS"]
