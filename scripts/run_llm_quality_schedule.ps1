<# Run the short OpenRouter quality-agent cache refresh as a hidden task. #>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = (Get-Command python -ErrorAction Stop).Source
Set-Location -LiteralPath $ProjectRoot
& $Python -m scripts.run_llm_quality_schedule --once
exit $LASTEXITCODE
