# 📌 Opus Auto Reviews — enriched analyses

_Refreshed: **2026-11-11 23:42 EEST**_

The Claude `routine` **opus-enriched-review-4h** fires automatically **6×/day** (00:30, 04:30, 08:30, 12:30, 16:30, 20:30 EEST) and runs the full `enriched-review` skill:
- Reads latest reports + catalyst data.
- WebSearch + WebFetch per candidate (§14 source discipline).
- Ingests external sources into `news_items` SQLite.
- Writes `OPUS_ENRICHED_REVIEW_LATEST.md` (always overwritten) + `OPUS_ENRICHED_REVIEW_AUTO_<timestamp>.md` (history).
- Sends a compact Telegram summary with top decisions + key risks.

Manual reviews (typed `/enriched-review` in chat) use the **same** skill.

---

## 📜 Recent reviews (latest first)

- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1608.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1608.md) · _2026-09-09 13:13 UTC_
- [OPUS_ENRICHED_REVIEW_LATEST.md](../OPUS_ENRICHED_REVIEW_LATEST.md) · _2026-09-09 13:13 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1145.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1145.md) · _2026-09-09 08:53 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_0445.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_0445.md) · _2026-09-09 01:48 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2330.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2330.md) · _2026-09-08 20:37 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2155.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2155.md) · _2026-09-08 18:58 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1839.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1839.md) · _2026-09-08 15:50 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1603.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1603.md) · _2026-09-08 13:08 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1139.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1139.md) · _2026-09-08 08:49 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_0450.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_0450.md) · _2026-09-08 01:47 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2334.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2334.md) · _2026-09-07 20:37 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2139.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2139.md) · _2026-09-07 18:50 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1841.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1841.md) · _2026-09-07 15:52 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1601.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1601.md) · _2026-09-07 13:05 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1147.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_1147.md) · _2026-09-07 08:51 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_0439.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_0439.md) · _2026-09-07 01:50 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_2331.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_2331.md) · _2026-09-06 20:34 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_2145.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_2145.md) · _2026-09-06 18:48 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1838.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1838.md) · _2026-09-06 15:49 UTC_
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1602.md](../OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1602.md) · _2026-09-06 13:06 UTC_

---

## How to read these

Each review has fixed sections:
- **Executive Summary** — 3-6 bullets, read this first.
- **Data Used** — what was loaded + what was unavailable.
- **Candidate Deep Dives** — verified external claims with URL + date.
- **Best Candidates / Avoid / Main Risks / Action Plan**.
- **Final Verdict** per mode + overall.
- **Sources** with markdown hyperlinks (verification: primary_source / single_source / social_only).

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
