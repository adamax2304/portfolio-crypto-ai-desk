<#
Run the autonomous pre-US stocks review through OpenRouter.

Task Scheduler invokes this wrapper around the US open. The
wrapper itself uses America/New_York and a per-session success marker, so the
Windows account timezone and the two annual DST mismatch weeks cannot shift the
review. Deterministic code owns all hard gates, score clamps and actionability;
the model can only return a structured advisory verdict. This task never sends
an order or edits a proposed signal.
#>
[CmdletBinding()]
param([switch]$Force)

$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Users\adama\Documents\crypto-ai-desk"
$Python = (Get-Command python -ErrorAction Stop).Source
function Get-NewYorkNow {
    $tz = [System.TimeZoneInfo]::FindSystemTimeZoneById("Eastern Standard Time")
    return [System.TimeZoneInfo]::ConvertTimeFromUtc([DateTime]::UtcNow, $tz)
}

Set-Location -LiteralPath $ProjectRoot
$nyNow = Get-NewYorkNow
$minutes = $nyNow.Hour * 60 + $nyNow.Minute
$isWeekday = $nyNow.DayOfWeek -notin @([DayOfWeek]::Saturday, [DayOfWeek]::Sunday)

# Start at 08:50 ET and leave bounded retries through the configured 09:12
# deadline. The heartbeat
# watchdog may use the same wrapper as a recovery path when a Windows trigger
# is missed, so keep a small bounded retry window rather than relying on one
# exact local-clock minute.
if (-not $Force -and ((-not $isWeekday) -or $minutes -lt 530 -or $minutes -gt 552)) {
    exit 0
}

$session = $nyNow.ToString("yyyy-MM-dd")
$runDir = Join-Path $ProjectRoot "data\scheduled_runs\preus_review"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null
$donePath = Join-Path $runDir ("{0}.openrouter.done" -f $session)
$logPath = Join-Path $runDir ("{0}.log" -f $session)

if (-not $Force -and (Test-Path -LiteralPath $donePath)) {
    exit 0
}

function Invoke-Logged([string]$Label, [scriptblock]$Command) {
    "[$([DateTime]::UtcNow.ToString('o'))] $Label" | Tee-Object -FilePath $logPath -Append
    & $Command 2>&1 | Tee-Object -FilePath $logPath -Append
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

try {
    Invoke-Logged "stocks-preus-openrouter-review" {
        & $Python -m src.cli stocks-preus-openrouter-review --require-complete
    }

    $healthOutput = & $Python -m src.cli stocks-preus-review-health 2>&1 |
        Tee-Object -FilePath $logPath -Append
    if ($LASTEXITCODE -ne 0) {
        throw "stocks-preus-review-health failed with exit code $LASTEXITCODE"
    }
    Set-Content -LiteralPath $donePath -Value ("openrouter_completed_at=" + [DateTime]::UtcNow.ToString("o")) -Encoding ascii
    "[$([DateTime]::UtcNow.ToString('o'))] Autonomous OpenRouter pre-US review completed" |
        Tee-Object -FilePath $logPath -Append
}
catch {
    "[$([DateTime]::UtcNow.ToString('o'))] ERROR: $($_.Exception.Message)" |
        Tee-Object -FilePath $logPath -Append
    exit 1
}
