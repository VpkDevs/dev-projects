param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
$ErrorActionPreference = 'Stop'
$gh = Join-Path -Path $PSScriptRoot -ChildPath 'gh_portable/bin/gh.exe'
& $gh @Args

