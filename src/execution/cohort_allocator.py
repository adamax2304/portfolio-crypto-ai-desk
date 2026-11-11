"""Cohort allocator / candidate risk-weights — READ-MODEL / REPORTING ONLY.

Encodes the audit's strategic conclusion (see AUDIT_REAUDIT_TAILS_REPORT): the structural
B logic is a better *idea* than A, but clean forward B is still net-negative, so we do NOT
promote "all of B". Instead each cohort gets a candidate weight for further PAPER validation:

  * crypto swing (pullback / breakdown) ...... 1.0   candidate (strongest forward B)
  * crypto intraday short breakdown ......... 0.5   candidate_reduced (lower weight)
  * crypto intraday long pullback ........... 0.0   disabled
  * stocks intraday long continuation ....... 0.0   disabled
  * crypto scalp ............................ 0.0   shadow_only
  * stocks short continuation ............... 0.0   research_shadow (needs own forward proof)
  * everything else ......................... 0.0   shadow_only (no forward-proven edge)

THIS IS NOT LIVE EXECUTION. Nothing here sizes, routes, or gates a real or paper order — it
is a labelling/reporting layer the review + dashboards read. `paper_execution_r`,
`signal_outcomes.final_r`, and every live/auto/manual-live path are untouched and hard-locked.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

# order matters: most specific rule first; the first match wins.
# a rule matches a trade when EVERY key it specifies equals the trade's value
# (setup_family is derived by `setup_family()` below).
_RULES: list[dict] = [
    {"asset_class": "crypto", "mode": "swing",
     "weight": 1.0, "status": "candidate",
     "note": "crypto swing pullback/breakdown — strongest clean-forward B candidate"},
    {"asset_class": "crypto", "mode": "intraday", "direction": "short", "setup_family": "breakdown",
     "weight": 0.5, "status": "candidate_reduced",
     "note": "crypto intraday short breakdown — promising but lower conviction; half weight"},
    {"asset_class": "crypto", "mode": "intraday", "direction": "long", "setup_family": "pullback",
     "weight": 0.0, "status": "disabled",
     "note": "crypto intraday long pullback — no forward edge; disabled"},
    {"asset_class": "stocks", "mode": "intraday", "direction": "long", "setup_family": "continuation",
     "weight": 0.0, "status": "disabled",
     "note": "stocks intraday long continuation — no forward edge; disabled"},
    {"asset_class": "crypto", "mode": "scalp",
     "weight": 0.0, "status": "shadow_only",
     "note": "crypto scalp — shadow only (latency/fee fragile)"},
    {"asset_class": "stocks", "direction": "short", "setup_family": "continuation",
     "weight": 0.0, "status": "research_shadow",
     "note": "stocks short continuation — research/shadow candidate until its OWN forward proof"},
]

_DEFAULT = {"weight": 0.0, "status": "shadow_only",
            "note": "no forward-proven edge for this cohort — shadow only"}


def setup_family(setup_type: str = "", playbook: str = "") -> str:
    """Coarse setup family from the setup_type / playbook strings.
    Breakdown is checked BEFORE pullback: a `failed_bounce` is a SHORT/breakdown setup and must
    not be swallowed by the "bounce" substring in the pullback bucket."""
    s = f"{setup_type or ''} {playbook or ''}".lower()
    if any(k in s for k in ("breakdown", "failed_bounce", "breakout_short")):
        return "breakdown"
    if any(k in s for k in ("pullback", "bounce", "retest")):
        return "pullback"
    if any(k in s for k in ("continuation", "momentum", "breakout", "rs_", "rotation")):
        return "continuation"
    return "other"


@dataclass
class Allocation:
    cohort_key: str
    asset_class: str
    mode: str
    direction: str
    setup_family: str
    weight: float
    status: str
    note: str
    live_locked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


def _matches(rule: dict, *, asset_class, mode, direction, fam) -> bool:
    got = {"asset_class": asset_class, "mode": mode, "direction": direction, "setup_family": fam}
    for k, v in rule.items():
        if k in ("weight", "status", "note"):
            continue
        if str(got.get(k) or "").lower() != str(v).lower():
            return False
    return True


def allocate(asset_class: str, mode: str, direction: str = "long",
             setup_type: str = "", playbook: str = "") -> Allocation:
    """Return the paper candidate weight + status for a cohort. Read-model only."""
    ac = str(asset_class or "").lower()
    ac = "stocks" if ac.startswith("stock") else ("crypto" if ac.startswith("crypto") else ac)
    md = str(mode or "").lower()
    dr = str(direction or "long").lower()
    fam = setup_family(setup_type, playbook)
    rule = next((r for r in _RULES if _matches(r, asset_class=ac, mode=md, direction=dr, fam=fam)),
                _DEFAULT)
    return Allocation(
        cohort_key=f"{ac}/{md}/{dr}/{fam}", asset_class=ac, mode=md, direction=dr,
        setup_family=fam, weight=float(rule["weight"]), status=rule["status"], note=rule["note"])


def weights_table() -> list[dict]:
    """The full declared cohort weight table (for reporting/UI). Read-only."""
    rows = []
    for r in _RULES:
        rows.append({"match": {k: v for k, v in r.items() if k not in ("weight", "status", "note")},
                     "weight": r["weight"], "status": r["status"], "note": r["note"]})
    rows.append({"match": {"*": "default"}, **_DEFAULT})
    return rows
