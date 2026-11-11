# Expired Signal Decision (PART 7)

**Date:** 2026-06-16 · Based on [EXPIRED_SIGNAL_ROOT_CAUSE_AUDIT.md](EXPIRED_SIGNAL_ROOT_CAUSE_AUDIT.md)

## Verdict

```
EXPIRED_RATE_HIGH_BUT_PROTECTIVE
```

(with a targeted **EXPIRED_RATE_NEEDS_ENTRY_VALIDITY_STUDY** flag for **stocks intraday
only** — see recommendations.)

## Answers

1. **Is a high expired count normal for this system?** **Yes.** The system proposes entry
   *zones* with finite validity, not market orders. A signal that never fills (no risk) or
   chops flat and times out (no commitment) is the validity window doing its job. A
   meaningful expiry rate is expected and healthy for a zone-based paper system.

2. **Which expired signals are harmless / protective?**
   - **setup_expired_no_entry** (368 all-time): entry zone never touched → zero capital at
     risk. Fully protective.
   - **entered_then_expired_flat** (426): entered, drifted, timed out. **0% hit the stop**
     and only ~4–6% reached +1R MFE — they protect against time-decay on trades that never
     developed. Mostly protective; modest missed upside.

3. **Which represent missed opportunity?** Only the slice of entered-then-flat that
   reached +0.5R (47–72%) but not +1R. The miss is *modest* (avg MFE ~0.5R) and capturing
   it would require an exit-logic change (forbidden without a separate backtest).

4. **Are stocks-intraday expiries mostly no-fill / flat / market-hours?** **Yes** — stocks
   intraday is 87% of all expiries, split ~49% no-fill / ~51% entered-flat. This is an RTH
   timing pattern: zones proposed too far from price for the remaining session, or
   sideways chop into the close.

5. **Is the entry zone too conservative?** Plausibly for stocks intraday (high no-fill).
   **Unknown without a study** — and changing it is forbidden here.

6. **Is validity too short?** No evidence it's too short — entered-flat trades had ample
   time and simply didn't develop (only ~5% reached +1R). Extending validity globally is
   forbidden and unsupported.

7. **Is the tracker too slow?** Not for *accuracy* — the candle walk catches touches
   retroactively, so latency does not create false expiries. (Latency hurts manual
   actionability — that's PART 10, not expiry correctness.)

8. **Are too many setup alerts created before realistic entry?** For stocks intraday,
   likely yes (high no-fill). This is the one place a study is warranted.

9. **Should expired signals be shown in Telegram less aggressively?** **Yes** — already
   partly handled: setup Telegram is suppressed for scalp; close_expired alerts for
   never-actionable trades add noise. Recommend not pushing close-expired for
   never-pushed entries (most are now `late_shadow`/`shadow_only` anyway after PART 5).

## Allowed safe recommendations (no strategy change)

- ✅ **Better labels / dashboard grouping** — group expired by no-fill vs entered-flat so
  the operator sees protective vs modest-miss at a glance. (Dashboard label work — safe.)
- ✅ **No Telegram for expired-no-entry** — a setup that never filled needs no close ping.
- ✅ **Late-entry shadow routing** — implemented in PART 5; reduces un-actionable noise.
- ✅ **Per-playbook validity STUDY for stocks intraday** — a read-only research study of
  entry-zone distance vs fill rate vs RTH clock. **Study only**, no change without
  separate approval.

## Forbidden (require separate approval — NOT done)

Changing TP/SL, loosening filters, widening entry zones, extending validity globally,
promoting expiry-prone setups. None performed.

**PART 7 status: DONE — verdict `EXPIRED_RATE_HIGH_BUT_PROTECTIVE`; stocks-intraday
validity study recommended as the one targeted follow-up.**
