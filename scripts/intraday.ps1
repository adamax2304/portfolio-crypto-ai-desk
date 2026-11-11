$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m src.cli ask "Update the data and check if morning ideas are still valid"
