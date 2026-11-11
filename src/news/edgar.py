"""SEC EDGAR reliable filing ingest (2026-07-03) — advisory / legal-risk context only.

The old `SEC EDGAR Filings` source was a generic browse-edgar Atom URL that returned nothing (0 rows).
This replaces it with the OFFICIAL, reliable path:
  * ticker→CIK map built from SEC's own `company_tickers.json` (cached; fail-open),
  * per-CIK `data.sec.gov/submissions/CIK##########.json` (structured recent filings),
  * normalize target forms (8-K, 10-Q, 10-K, S-1, S-3, 424B*, Form 4) into `news_items` with
    source='SEC EDGAR', asset_class='stocks', event_type='filing', form_type, cik, filing_url.

Unknown CIK → a diagnostics warning, never a crash. This feeds the legal-risk / catalyst advisory
layer ONLY — it never changes trading score, tier, or actionability. Network calls are guarded and
fail-open; the normalizer is pure and unit-tested.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.news.source_telemetry import now_iso, record_source_run

_ROOT = Path(__file__).resolve().parents[2]
_CIK_CACHE = _ROOT / "data" / "reference" / "ticker_cik_map.json"
_UA = "crypto-ai-desk research (contact: operator@example.com)"   # SEC requires a UA header

# target forms + importance heuristic (higher = more material for the advisory/legal layer)
FORM_IMPORTANCE = {
    "8-K": 2.6, "8-K/A": 2.6,          # material events / legal disclosures
    "10-Q": 1.9, "10-K": 2.0,          # periodic financials
    "S-1": 2.2, "S-3": 2.2,            # registration (potential dilution)
    "424B5": 2.4, "424B2": 2.4, "424B3": 2.4,   # prospectus (offering/dilution)
    "4": 1.4,                          # insider transactions
}
DEFAULT_FORMS = tuple(FORM_IMPORTANCE.keys())
_LAST_FETCH_ERRORS: list[str] = []


def load_cik_map() -> dict[str, str]:
    """ticker(upper) -> zero-padded 10-digit CIK, from the cached SEC map (empty if not built yet)."""
    try:
        return {k.upper(): str(v) for k, v in json.loads(_CIK_CACHE.read_text(encoding="utf-8")).items()}
    except Exception:
        return {}


def refresh_cik_map() -> dict[str, str]:
    """Build/refresh the ticker→CIK cache from SEC's official company_tickers.json. Fail-open: on any
    network/parse error returns the existing cache unchanged."""
    try:
        import requests
        r = requests.get("https://www.sec.gov/files/company_tickers.json",
                         headers={"User-Agent": _UA}, timeout=20)
        r.raise_for_status()
        data = r.json()
        out = {str(row["ticker"]).upper(): f"{int(row['cik_str']):010d}" for row in data.values()}
        _CIK_CACHE.parent.mkdir(parents=True, exist_ok=True)
        _CIK_CACHE.write_text(json.dumps(out), encoding="utf-8")
        return out
    except Exception:
        return load_cik_map()


def normalize_filing(*, ticker: str, cik: str, form: str, filed_at: str,
                     accession: str = "", primary_doc: str = "", title: str | None = None) -> dict[str, Any]:
    """Pure normalizer: one SEC filing → a news_items-shaped row. No I/O. Unit-tested."""
    t = str(ticker).upper()
    cik_num = str(cik).lstrip("0") or str(cik)
    acc_nodash = accession.replace("-", "")
    url = (f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_nodash}/{primary_doc}"
           if accession and primary_doc else
           f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={form}")
    imp = FORM_IMPORTANCE.get(form.upper(), 1.5)
    ttl = title or f"{t} filed {form} with the SEC"
    return {
        "title": ttl, "source": "SEC EDGAR", "url": url, "published_at": filed_at,
        "asset_class": "stocks", "importance": imp,
        "detected_symbols_json": json.dumps([t]),
        "raw_json": json.dumps({"ticker": t, "cik": cik, "form_type": form, "filed_at": filed_at,
                                "filing_url": url, "event_type": "filing", "accession": accession,
                                "source_quality": "primary_or_regulator"}),
    }


def _fetch_recent_filings(cik: str, forms: tuple, limit: int) -> list[dict[str, Any]]:
    global _LAST_FETCH_ERRORS
    try:
        import requests
        r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json",
                         headers={"User-Agent": _UA}, timeout=20)
        r.raise_for_status()
        recent = ((r.json() or {}).get("filings") or {}).get("recent") or {}
    except Exception as exc:
        _LAST_FETCH_ERRORS.append(f"CIK {cik}: {type(exc).__name__}: {exc}")
        return []
    forms_l = {f.upper() for f in forms}
    out = []
    ff = recent.get("form") or []
    dates = recent.get("filingDate") or []
    accs = recent.get("accessionNumber") or []
    docs = recent.get("primaryDocument") or []
    for i, form in enumerate(ff):
        if str(form).upper() not in forms_l:
            continue
        out.append({"form": form, "filed_at": (dates[i] if i < len(dates) else ""),
                    "accession": (accs[i] if i < len(accs) else ""),
                    "primary_doc": (docs[i] if i < len(docs) else "")})
        if len(out) >= limit:
            break
    return out


def diagnostics(tickers: list[str] | None = None) -> dict[str, Any]:
    """Which universe tickers have / lack a known CIK (drives a source-health warning). Read-only."""
    tickers = tickers or _universe_tickers()
    cmap = load_cik_map()
    known = [t for t in tickers if t.upper() in cmap]
    unknown = [t for t in tickers if t.upper() not in cmap]
    return {"cik_map_size": len(cmap), "universe": len(tickers),
            "known_cik": len(known), "unknown_cik": unknown[:40],
            "warning": (f"{len(unknown)} universe tickers lack a CIK — run edgar.refresh_cik_map()"
                        if unknown else None)}


def _universe_tickers() -> list[str]:
    try:
        from src.stocks import load_stocks_config
        return [str(s).upper() for s in (load_stocks_config().default_symbols or [])]
    except Exception:
        return []


def refresh(db=None, *, tickers: list[str] | None = None, forms: tuple = DEFAULT_FORMS,
            per_ticker: int = 8, build_map: bool = False) -> dict[str, Any]:
    """Ingest recent SEC filings for the stocks universe into news_items (advisory/legal context).
    Fail-open network. Returns a summary incl. unknown-CIK warnings. Never changes scoring."""
    global _LAST_FETCH_ERRORS
    _LAST_FETCH_ERRORS = []
    started_at = now_iso()
    if build_map or not load_cik_map():
        refresh_cik_map()
    cmap = load_cik_map()
    tickers = tickers or _universe_tickers()
    from src.config import load_config
    from src.storage.sqlite import SQLiteStore
    store = SQLiteStore((db and Path(db)) or load_config().db_path)
    store.init_db()
    saved, unknown = 0, []
    for t in tickers:
        cik = cmap.get(t.upper())
        if not cik:
            unknown.append(t)
            continue
        for f in _fetch_recent_filings(cik, forms, per_ticker):
            rec = normalize_filing(ticker=t, cik=cik, form=f["form"], filed_at=f["filed_at"],
                                   accession=f["accession"], primary_doc=f["primary_doc"])
            try:
                # raw-json-preserving save so form_type/cik/filing_url/event_type survive in news_items
                store.save_news_rows([rec], asset_class="stocks")
                saved += 1
            except Exception:
                continue
    status = "error" if _LAST_FETCH_ERRORS and not saved else ("ok" if saved else "ok_empty")
    record_source_run(
        source_name="SEC EDGAR", source_type="api", asset_class="stocks", status=status,
        started_at=started_at, item_count=saved,
        error_code=("sec_request_failed" if _LAST_FETCH_ERRORS else None),
        error_message="; ".join(_LAST_FETCH_ERRORS[:4]) if _LAST_FETCH_ERRORS else None,
        metadata={"tickers": len(tickers), "unknown_cik": len(unknown), "forms": list(forms)},
    )
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "saved": saved,
            "tickers": len(tickers), "unknown_cik_count": len(unknown), "unknown_cik": unknown[:30],
            "forms": list(forms),
            "transport_status": status, "transport_errors": _LAST_FETCH_ERRORS[:10],
            "note": "SEC filings ingested as advisory/legal context only — no score/tier/actionability change."}
