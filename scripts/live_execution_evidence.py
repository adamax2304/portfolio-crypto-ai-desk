from __future__ import annotations

from src.analysis.live_execution_evidence import (
    live_fill_parity, refresh_rejection_counterfactuals, render_markdown,
)
from src.config import load_config


def main() -> int:
    cfg = load_config()
    rejected = refresh_rejection_counterfactuals(db=cfg.db_path)
    parity = live_fill_parity(db=cfg.db_path)
    target = cfg.root / "reports" / "LIVE_EXECUTION_EVIDENCE_LATEST.md"
    target.write_text(render_markdown(parity, rejected), encoding="utf-8")
    print(f"live evidence: closed={parity['closed']} rejected_refreshed={rejected['refreshed']} report={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
