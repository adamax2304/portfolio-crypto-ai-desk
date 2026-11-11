$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m src.cli ask "Review today ideas and tell me what worked and failed"
