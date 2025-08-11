param()
$ErrorActionPreference = 'Stop'
$PSDefaultParameterValues['*:ErrorAction'] = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$work = Join-Path -Path (Get-Location) -ChildPath '_agent_work'
New-Item -ItemType Directory -Force -Path $work | Out-Null

# Start logging
try {
  if (-not (Test-Path (Join-Path $work 'transcript.log'))) {
    New-Item -ItemType File -Path (Join-Path $work 'transcript.log') | Out-Null
  }
  Start-Transcript -Path (Join-Path $work 'transcript.log') -Append | Out-Null
} catch {}

# Simple logging function
function Write-Log {
  param(
    [string]$Message,
    [ValidateSet('INFO','WARN','ERROR')][string]$Level = 'INFO'
  )
  $ts = (Get-Date).ToString('s')
  $line = "[$ts] [$Level] $Message"
  $line | Tee-Object -FilePath (Join-Path $work 'agent.log') -Append
}

# Attempt to install a portable gh into the working directory
try {
  $zip  = Join-Path -Path $work -ChildPath 'gh_windows_amd64.zip'
  $dest = Join-Path -Path $work -ChildPath 'gh_portable'
  $url  = 'https://github.com/cli/cli/releases/download/v2.55.0/gh_2.55.0_windows_amd64.zip'
  Write-Log "Downloading GitHub CLI from $url"
  Invoke-WebRequest -Uri $url -OutFile $zip
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  Expand-Archive -Path $zip -DestinationPath $dest -Force
  $exe = Get-ChildItem -Path $dest -Recurse -Filter 'gh.exe' | Select-Object -First 1
  if ($null -eq $exe) { throw 'gh.exe not found after extraction' }
  $bin = Split-Path -Path $exe.FullName -Parent
  $env:PATH = ($bin + ';' + $env:PATH)
  [Environment]::SetEnvironmentVariable('PATH', $env:PATH, 'Process')
  Write-Log "gh installed at $bin"
  (& $exe.FullName --version) | Write-Log
} catch {
  Write-Log ("gh install failed: " + $_.Exception.Message) 'ERROR'
}

# Verify Git is available
try {
  (git --version) | Write-Log
} catch {
  Write-Log ("git not found: " + $_.Exception.Message) 'ERROR'
}

try { Stop-Transcript | Out-Null } catch {}

