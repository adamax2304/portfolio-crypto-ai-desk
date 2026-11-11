# Control Plane Frontend Health (PART 5)

**Date:** 2026-06-20.

- **Model:** the Mini App is a **static Vite/React build** in `frontend/dist`, served by the backend at `/` (single origin). No standalone dev server is required (and none was running — that is by design, not a failure).
- **Typecheck:** `npx tsc -b` → **exit 0** (no TS errors).
- **Build:** `launch_robust.ps1` runs `npm run build` before serving, so `dist` is fresh on each (re)launch. No stale-build problem.
- **Loads through tunnel:** `GET <tunnel>/` → **200**, HTML contains `id="root"`, and **`@vite/client` is absent** (`vite_dev=False`) → confirmed production build, not the fragile dev server.
- **Empty state:** "No open actionable trades" copy present (status-clarity session) → no blank/spinner when there are 0 actionable trades.
- **API base:** same-origin `/api` → no cross-origin breakage inside Telegram.

## Verdict
**CONTROL_PLANE_FRONTEND_OK** (built dist served fresh through the tunnel; tsc clean). The frontend was not the failure — it had no live origin because the backend/tunnel were down (now fixed).
