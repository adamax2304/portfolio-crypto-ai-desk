<#
  Persistent, idempotent launcher for the default market scheduler.

  - Duplicate protection: if a `run_default_market_schedule` python process is already
    alive (or a fresh pidfile points at a live process), it exits WITHOUT starting a
    second instance.
  - Launches the existing infinite-restart wrapper `autostart_scheduler.bat` DETACHED
    (survives terminal/session close), logs to logs/monitor_scheduler_*.log, records the
    pid, and sends a "Monitor started" Telegram heartbeat.

  This NEVER changes trading logic — it only (re)starts the existing scheduler.
  Stop with:  Stop-ScheduledTask CryptoAIDesk_Scheduler   (or kill the python child)
#>
param(
  [switch]$Quiet,
  # -Foreground: run the autostart loop INLINE (task-owned, so Task Scheduler
  # restart-on-failure works). Default = detached (survives terminal/session close).
  [switch]$Foreground
)

$ErrorActionPreference = 'Stop'
$Project = Split-Path -Parent $PSScriptRoot
$LogDir  = Join-Path $Project 'logs'
$AutostartLog = Join-Path $Project 'data\autostart'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
if (-not (Test-Path $AutostartLog)) { New-Item -ItemType Directory -Path $AutostartLog | Out-Null }
$PidFile = Join-Path $AutostartLog 'scheduler_runner.pid'
$Bat     = Join-Path $Project 'scripts\autostart_scheduler.bat'

function Test-SchedulerAlive {
  # True if any python process is running the default market scheduler.
  $procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like '*run_default_market_schedule*' }
  return ($procs | Measure-Object).Count -gt 0
}

if (Test-SchedulerAlive) {
  if (-not $Quiet) { Write-Output 'start_monitor_scheduler: scheduler already running — not starting a duplicate.' }
  exit 0
}

# stale pidfile cleanup (informational only; the process check above is authoritative)
if (Test-Path $PidFile) { Remove-Item $PidFile -ErrorAction SilentlyContinue }

$out = Join-Path $LogDir 'monitor_scheduler_stdout.log'
$err = Join-Path $LogDir 'monitor_scheduler_stderr.log'

# "Monitor started" heartbeat (best-effort; never fail the launch on telegram).
try {
  Push-Location $Project
  & python -m scripts.monitor_heartbeat --event start 2>$null | Out-Null
} catch {} finally { Pop-Location }

if ($Foreground) {
  # Task-owned mode: run the infinite-restart loop inline so Task Scheduler can apply
  # restart-on-failure. The .bat already self-redirects to data\autostart\scheduler.log.
  if (-not $Quiet) { Write-Output 'start_monitor_scheduler: running autostart loop in foreground (task-owned).' }
  Set-Content -Path $PidFile -Value $PID -Encoding ascii
  & cmd.exe /c "`"$Bat`""
  exit $LASTEXITCODE
}

# Default: launch the infinite-restart wrapper detached + hidden. cmd /c keeps the .bat
# loop alive; Start-Process is not parented to this shell, so it survives terminal/session close.
$proc = Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c', "`"$Bat`"") `
  -WorkingDirectory $Project -WindowStyle Hidden -PassThru `
  -RedirectStandardOutput $out -RedirectStandardError $err
Set-Content -Path $PidFile -Value $proc.Id -Encoding ascii

if (-not $Quiet) { Write-Output "start_monitor_scheduler: launched runner pid=$($proc.Id) (detached). Logs -> $out" }
exit 0
