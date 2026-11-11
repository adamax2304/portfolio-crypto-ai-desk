<# Install/update the independent 15-minute LLM quality refresh task. #>
[CmdletBinding()]
param(
    [int]$IntervalMinutes = 15,
    [switch]$NoStart
)

$ErrorActionPreference = "Stop"
if ($IntervalMinutes -lt 5) {
    throw "IntervalMinutes must be at least 5"
}

$TaskName = "CryptoAIDesk_LLMQuality"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $ProjectRoot "scripts\run_llm_quality_schedule.ps1"
$PowerShell = (Get-Command powershell.exe -ErrorAction Stop).Source
$Action = New-ScheduledTaskAction `
    -Execute $PowerShell `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Runner`"" `
    -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 20) `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 2)
$Principal = New-ScheduledTaskPrincipal `
    -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Refresh Crypto AI Desk LLM advisory cache and router metrics every $IntervalMinutes minutes." `
    -Force | Out-Null

if (-not $NoStart) {
    Start-ScheduledTask -TaskName $TaskName
}

Get-ScheduledTask -TaskName $TaskName |
    Select-Object TaskName, State
