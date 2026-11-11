# Proxy-Duplicate Collapse — Rule A (PART 2)

**Date:** 2026-06-16 · `src/signals/portfolio_caps.py`

For stocks intraday A/B in the same day + direction + collapse-key, keep only the **best**
candidate actionable; the rest → `shadow_proxy_duplicate` (effective_weight 0.0,
telegram routed shadow). Score/tier/raw R/levels are never changed; nothing deleted.

**Best-candidate order:** tier (A>B) → higher score → catalyst-backed (`news_supported>0`)
→ higher `data_confidence` → earlier `created_at` (final tie-break).

**Collapse key:** `*_proxy` groups collapse across symbols (QQQ↔XLK, SPY↔DIA↔IWM);
all other groups collapse only against the **same symbol** (duplicate signals), so distinct
single names are never merged here.

**Examples (tested):**
- QQQ(80) + XLK(70) same day/long → keep QQQ, XLK → `shadow_proxy_duplicate`.
- SPY(75)+DIA(82)+IWM(60) → keep DIA, SPY & IWM shadowed.

Tests: `test_1_qqq_xlk_collapse_keeps_best_score`, `test_2_spy_dia_iwm_collapse_keeps_best`,
live `test_live_proxy_duplicate_shadow`. **PART 2 status: DONE.**
