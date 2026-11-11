# C-Tier / Watchlist Setups

## Definition

- `final_score ≥ 50` and < 65 (or pinned by cap below 65).
- `direction = "watchlist only"` in the trade idea (regardless of underlying `setup.direction`).
- Status: `watchlist`.

## What C-tier means

- The desk is interested but not ready to commit.
- Either the structure is incomplete (no clear acceptance, weak volume), or the extension is too high, or evidence is too thin.
- The setup is conditional — `entry_plan` describes a potential pullback zone.

## How to use it

- **Track it**: log into [[11_Trade_Journal/Watchlist_Ideas/README|Watchlist_Ideas]] using [[Watchlist_Template]].
- **Wait**: `WatchlistMonitor` auto-watches C-tier symbols and alerts on upgrade.
- **Do not force entry**: a C-tier is C-tier for a reason. If you trade C-tier as if it were B-tier, the desk's discipline collapses.

## Conditional entries

For C-tier ideas with a directional setup (`setup.direction ∈ {long, short}` but tier=C), the `entry_plan` will say:

```
Watch only. Conditional pullback zone: 1.2345 - 1.2456.
Do not treat this as active until regime, volume, or confirmation improves.
```

And `invalidation` will say:

```
Potential invalidation if activated: 1h close beyond 1.2200.
Not active while score is below threshold.
```

## When C-tier becomes tradable

- Watchlist monitor reports C → B/A. Telegram alert fires.
- Operator notices an event (volume spike, narrative catalyst, regime shift) that the next report should re-classify.
- Manual judgment that the cap reason no longer applies (e.g. listing on anchor announced).

In all cases, **wait for the next official tier upgrade**. Don't unilaterally upgrade.

## Related

- [[Scoring_Overview]]
- [[B_Tier_Setups]]
- [[Rejected_Setups]]
- [[Watchlist_Monitor_Agent]]
- [[Watchlist_Template]]

## Implemented status

- **Implemented**.
