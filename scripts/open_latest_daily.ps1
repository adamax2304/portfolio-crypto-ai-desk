$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
$report = Get-ChildItem "data\reports\daily" -Filter "*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($null -eq $report) {
  Write-Host "No daily report found. Run .\scripts\daily.ps1 first."
  exit 1
}
Invoke-Item $report.FullName
