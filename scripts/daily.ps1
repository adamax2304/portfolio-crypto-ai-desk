$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m src.cli ask "Analyze the market today and give me the best trade ideas"
