param()
$ErrorActionPreference = 'Stop'
$PSDefaultParameterValues['*:ErrorAction'] = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$work = Join-Path -Path (Get-Location) -ChildPath '_agent_work'
$ghExe  = Join-Path -Path $work -ChildPath 'gh_portable\bin\gh.exe'
$patFile = Join-Path -Path $work -ChildPath 'pat.txt'
$report  = Join-Path -Path $work -ChildPath 'env_validation_report.txt'

if (-not (Test-Path $ghExe)) { throw "gh executable not found at $ghExe" }
if (-not (Test-Path $patFile)) { throw "PAT file not found at $patFile" }

$token = Get-Content -Raw -Path $patFile
if ([string]::IsNullOrWhiteSpace($token)) { throw 'PAT file is empty' }

# Authenticate using token via stdin (token is not printed)
$null = $token | & $ghExe auth login --hostname github.com --with-token

# Validation calls (non-destructive)
$who   = & $ghExe api user --jq '.login'
$repos = & $ghExe repo list --limit 5 --json name,owner,visibility --jq '[.[] | {name, owner: .owner.login, visibility}]'
$rate  = & $ghExe api rate_limit --jq '.resources.core.remaining'
$scopes = (& $ghExe auth status) 2>&1

"GitHub user: $who`nRate limit remaining: $rate`nAuth status:`n$scopes`nSample repos:`n$repos" | Set-Content -Path $report -Encoding UTF8

Write-Output "Auth and API checks completed. Report: $report"
