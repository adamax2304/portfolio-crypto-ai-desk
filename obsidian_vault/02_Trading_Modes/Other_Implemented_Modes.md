# Other Implemented Modes

## Inspection result

After reading `config/scoring.yaml`, `config/universe.yaml`, `src/cli.py`, `src/agents/supervisor.py`, and `src/agents/trade_idea_agent.py`, the **only** trading modes implemented are:

- `scalp`
- `intraday`
- `swing`

There is no `long_term`, `position`, `dca`, `lottery`, `news_catalyst`, or any other named mode. The user's intuition that "there might be more" is correct in the sense that one **should** exist (long-term), but it has not been built.

## Closely-related concepts that look like modes but are not

- `--discovery` flag — widens the universe scanner (rank 250 symbols vs 120, lower volume floor). It is **not** a mode; it pairs with one of the three modes.
- `--auto-universe` flag — triggers the Stage-1 + Stage-2 funnel before the report. Not a mode.
- `kind` parameter in `Supervisor.daily_report(kind, mode)` — distinguishes output folder (`daily / intraday / scalp / swing`). It does **not** change scoring; the mode does.
- `ask` natural-language router — chooses between `daily-report`, `intraday-report`, `review`, `update-data`, `scan`. It does not select scalp or swing.

## If you find a reference somewhere that suggests another mode

Possible places to confuse yourself:

- `README.md` — only mentions the three modes.
- `START_HERE.md` — operational shortcuts, no extra mode.
- `scripts/*.ps1` — Windows wrappers around the three modes.
- `tests/test_supervisor_routing.py` — tests the natural-language router; no other modes.

If a future LLM finds a fourth-mode reference in code, document it here.

## Related

- [[Trading_Modes_Overview]]
- [[Long_Term_Mode]]

## Implemented status

- **Implemented** — this page is the audit.
