# Multi-Venue Live Execution: MEXC + Bybit

Date: 2026-08-18

## Result

The existing Paper decision remains authoritative. One immutable eligible
decision is claimed once, preflighted against all armed venues in parallel,
and submitted to exactly one selected venue. Strategies, Paper sizing,
quality overlay, risk guards, Model F and the shared outbox were not forked.

MEXC and Bybit are both armed. The new Bybit trade-only key passed mainnet V5
private preflight with `readOnly=0` and `ContractTrade=[Order, Position]`.
Credentials are stored in the Windows user environment and are not present in
the repository, YAML, report or application logs.

An older credential pair was discovered in another local project and tested
only with private GET requests. Bybit returned `retCode=33004` (`api key has
expired`). The values were not copied into this project or persisted into the
live monitor environment. This confirms that the existing keys cannot be used
for execution. A replacement key was then validated and activated.

## Routing

- Preference order: MEXC, then Bybit.
- Bybit wins when its estimated round-trip all-in cost improves by at least
  2 bps, or when MEXC cannot support/preflight the contract.
- Within 1 bp of the best cost, measured parallel-preflight latency is a
  tiebreaker when one venue is at least 75 ms faster. Latency never overrides
  a materially better executable price.
- Cost comparison includes signed entry drift, actual account fee rates when
  private Bybit preflight is available, and the existing slippage model.
- An order is never split between venues.
- Native symbols are kept for execution; a canonical symbol is used by the
  shared risk ledger so BTC_USDT and BTCUSDT cannot bypass same-symbol limits.
- Aggregate risk remains shared across venues. Both MEXC and Bybit use the
  same $10 FULL / $5 HALF base risk. The global cross-venue cap remains $50.
- The former static 50x operator ceiling is removed. Each plan now uses the
  highest leverage permitted by the venue contract and the existing 3x
  stop-to-liquidation buffer; this minimizes required margin without moving
  liquidation close to the protective stop.

## Stock Futures Routing

- Stock Paper decisions use a canonical `TICKER/USDT` identity and freeze a
  per-venue symbol map. MEXC keeps its authoritative catalog mappings such as
  `AAPLSTOCK_USDT`, `NVIDIA_USDT`, `TESLA_USDT` and `COINBASE_USDT`; Bybit uses
  its current linear stock symbols such as `AAPLUSDT`, `NVDAUSDT`, `TSLAUSDT`
  and `COINUSDT`.
- Bybit candidates must be `status=Trading` and `symbolType=stock` or `ETF`.
  MEXC candidates must retain the existing Stock/TradFi contract metadata,
  active state and API permission checks.
- A MEXC-local business block no longer suppresses the whole Paper decision.
  The router may use a valid Bybit contract, while still submitting exactly
  one order.
- The 104-symbol default stock universe currently has 100 active MEXC
  mappings, 75 Bybit mappings and 101 in the union. `DIA`, `XLY` and `XLC`
  currently have no eligible contract on either venue and fail closed.

## Bybit Lifecycle

- V5 linear USDT-perpetual REST signing and deterministic orderLinkId.
- IOC limit entry with no blind POST retry.
- Unknown submission is resolved by orderLinkId; unresolved state trips the
  shared kill switch and cannot fall through to MEXC.
- Full-position MarkPrice market stop is installed immediately after fill.
- Three deterministic reduce-only GTC TP legs are installed and tracked.
- Partial IOC fills are treated as real positions and protected immediately.
- Model F moves the full-position stop using the same thresholds as Paper.
- Repeated reconciliation is idempotent: filled TP legs remain terminal and
  are not recreated.
- If a new fill cannot obtain a confirmed stop, the executor submits a
  deterministic reduce-only emergency close and trips the shared kill switch.

## Storage And Monitoring

- Existing live tables gained an idempotent `venue` column; historical rows
  default to `mexc` and are preserved.
- Orders, positions, risk reservations and TP legs remain in one shared audit
  model with explicit venue attribution.
- Monitor reconciliation and watchdog diagnostics aggregate MEXC and Bybit.
- Existing `mexc-canary-*` commands remain compatible with the scheduler.

## Verification

- Real DB: kill switch CLEAR, pending outbox 0, open positions 0.
- MEXC public/private readiness: ready.
- Bybit public BTCUSDT contract and order book: ready.
- Bybit private readiness: ready; equity approximately $16.95, isolated UTA
  free USDT approximately $16.97, no open Bybit positions at activation.
- API safety: wallet permissions are empty, an IP restriction is configured,
  and private position inspection confirms one-way mode (`positionIdx=0`).
- Real read-only AAPL parallel plan: both venues passed. Bybit was selected
  for lower modeled all-in cost (17.19 bps versus 25.12 bps), despite MEXC's
  faster preflight (1.83 s versus 2.56 s). Modeled stock risk was $4.90,
  margin $15.71 at 10x, with three valid TP legs.
- Focused live/stock/multi-venue regression: 147 passed, then 26 focused tests
  passed after the final stock-routing changes.
- Full project regression: 2257 passed, 5 skipped. Two tests initially hit a
  concurrent working-DB lock from the active scheduler; both passed in an
  immediate isolated rerun and were unrelated to changed modules.
- No test or verification command submitted an exchange order.
- Live monitor reloaded successfully; heartbeat and watchdog both report OK
  with zero issues and no duplicate monitor process.
- The union of the 69 preferred/invest symbols has 68 currently tradable
  contracts: MEXC 67, Bybit 67. Bybit adds FIL/USDT when MEXC is unavailable;
  FET/USDT is MEXC-only; TON/USDT is unavailable on both (Bybit status Closed).
- Windows user-level secrets and the existing heartbeat scheduled task make
  the Bybit arm available again after monitor restart/logon.
- Both watchdog and the two-hour scheduler now explicitly restore MEXC and
  Bybit user-scoped credentials when spawning the live monitor. This closes a
  restart-only failure mode where an older scheduler environment could have
  silently returned execution to MEXC-only.
- Post-restart PID 8860 reports a fresh `OK` heartbeat. Read-only watchdog
  reconciliation reports both venues `OK`, zero issues, kill switch `CLEAR`
  and no pending outbox rows.

## Activation State

The following host secret variables are configured and armed:

- `BYBIT_LIVE_ACCESS_KEY`
- `BYBIT_LIVE_SECRET`
- `BYBIT_LIVE_ARMED=I_UNDERSTAND_REAL_BYBIT_ORDERS`

Private preflight, fee lookup, balance lookup, permissions and open-position
reconciliation all pass. The operator must still keep withdrawal permission
disabled, maintain an IP allowlist, and ensure the account can legally access
Bybit linear derivatives from its registered jurisdiction.
