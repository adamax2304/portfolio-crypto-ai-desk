# Crypto Intraday Cohort Guard v2

**Updated:** 2026-07-14  
**Scope:** paper routing only; live, scoring, entry geometry, TP/SL and outcomes are untouched.

## Decision

The broad v1 rule was rolled back from `paper_review_only` to `warn`. It treated a fresh catalyst as
mandatory for almost every crypto intraday long and would have demoted 7 of 8 recent candidates.
That scope was not supported by current evidence:

- 14d no-news intraday longs: PF 1.28, +11.14R;
- forward_postfreeze no-news: n=25, PF 1.53, +5.30R;
- forward_postfreeze no-news PULLBACK_LIMIT: n=20, PF 1.73, +5.10R;
- 14d no-news BREAKOUT_CONTINUATION: n=7, PF 0.25, -1.50R.

The catalyst remains a quality booster, not a universal entry requirement.

## Current production-paper behavior

- `mode: warn`: records the narrow condition but never changes size or routing.
- `PULLBACK_LIMIT` and `STRUCTURAL_RETEST`: excluded from the cohort guard; the normal market,
  session, derivatives, exposure and cooldown rules remain authoritative.
- `BREAKOUT_CONTINUATION`: the only cohort-guard target. It is considered weak only when it has
  neither a verified fresh catalyst nor full market confirmation.
- `LIMIT_THEN_TAKER_TIMEOUT` and `NO_CHASE_SKIP`: remain SHADOW_ONLY through the existing entry-mode
  policy, independently of this guard.
- `MOMENTUM_TAKER_NOW`: remains HALF_SIZE/cautious through the existing entry-mode policy.

## Honest forward evidence

Every new paper-entry decision persists these append-once fields in
`crypto_quality_overlay_decision_snapshots.decision_json`:

- `cohort_guard_policy_version=cohort_guard_v2`;
- `cohort_guard_mode`;
- `cohort_guard_in_scope`;
- `cohort_guard_would_demote`;
- `fresh_catalyst_confirmed`;
- `strong_confirmation` and `entry_mode`.

The overlay report calculates `entry_mode x fresh/no_fresh` metrics only from post-v2 point-in-time
snapshots joined to resolved `forward_postfreeze` outcomes. Mutable current snapshots, pre-v2 rows
and backfill are excluded.

## Re-activation gate

`paper_review_only` must never turn on automatically. It becomes eligible for operator review only
when the narrow unconfirmed-breakout slice has:

1. at least 30 resolved forward trades;
2. profit factor <= 0.80;
3. negative average R.

Until all three hold, the verdict is `NO_FORWARD_EVIDENCE`, `INSUFFICIENT_FORWARD_SAMPLE`, or
`NOT_ELIGIBLE`, and routing remains `warn`.

## Verification

- focused and integration regression: 149 passed;
- controlled same-context replay of the original 8 candidates: 0 routed by the cohort guard;
- replay actions: 2 FULL_SIZE, 4 HALF_SIZE, 2 SHADOW_ONLY; both SHADOW_ONLY decisions came from
  pre-existing independent protections;
- persisted current-context refresh after deployment: 0 `cohort_guard_review` reasons. Its action
  mix is not point-in-time evidence because historical candidates are re-evaluated using the current
  session/cooldown/exposure state.

## Verdict

`COHORT_GUARD_V2_WARN_FORWARD_COLLECTION`
