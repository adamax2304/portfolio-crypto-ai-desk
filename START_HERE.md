# Start Here

This is the quick operator card for Crypto AI Desk.

## First Run

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
python -m pip install -r requirements.txt
python -m src.cli update-data
python -m src.cli daily-report
python -m src.cli doctor
```

## Daily Use

Fresh market report:

```powershell
python -m src.cli ask "Analyze the market today and give me the best trade ideas"
```

Intraday re-check:

```powershell
python -m src.cli ask "Update the data and check if morning ideas are still valid"
```

Money/attention flow:

```powershell
python -m src.cli ask "Find where money and attention are flowing today"
```

Add manual KOL/crowd notes before a scan:

```text
data/raw/social/manual_social_mentions.yaml
```

Review:

```powershell
python -m src.cli ask "Review today ideas and tell me what worked and failed"
```

Latest report path:

```powershell
python -m src.cli latest --kind daily
```

Open latest daily report in Windows:

```powershell
.\scripts\open_latest_daily.ps1
```

## Important Outputs

- Daily report: `data/reports/daily/`
- Intraday reports: `data/reports/intraday/`
- Reviews: `data/reports/reviews/`
- Charts: `data/reports/charts/`
- Codex context: `data/processed/context_for_llm.md`
- Manual crowd/KOL notes: `data/raw/social/manual_social_mentions.yaml`
- KOL/source checklist: `config/kol_watchlist.yaml`
- SQLite database: `db/crypto_ai_desk.sqlite`

The desk is allowed to say `NO TRADE`. That is a feature, not a bug.
