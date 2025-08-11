# Script to compare projects with their backups and remove duplicates

$backupDir = "C:\users\public\Development_Projects\_BACKUP_BEFORE_ORGANIZATION_20250722_112514"
$mainDir = "C:\users\public\Development_Projects"
$duplicates = @()
$differences = @()

Write-Host "Analyzing projects for duplicates..." -ForegroundColor Cyan

# Get all directories in backup that also exist in main (excluding the backup itself)
$backupProjects = Get-ChildItem -Path $backupDir -Directory | Where-Object { $_.Name -ne "_BACKUP_BEFORE_ORGANIZATION_20250722_112514" }

foreach ($backupProject in $backupProjects) {
    $projectName = $backupProject.Name
    $mainProjectPath = Join-Path $mainDir $projectName
    
    # Check if the project exists in the main directory
    if (Test-Path $mainProjectPath) {
        Write-Host "`nComparing: $projectName" -ForegroundColor Yellow
        
        # Get all files from both directories recursively
        $backupFiles = Get-ChildItem -Path $backupProject.FullName -Recurse -File -ErrorAction SilentlyContinue | 
            Where-Object { $_.FullName -notmatch '\\\.git\\' } |
            ForEach-Object {
                @{
                    RelativePath = $_.FullName.Replace($backupProject.FullName, "")
                    Hash = (Get-FileHash $_.FullName -Algorithm MD5).Hash
                    Size = $_.Length
                }
            }
        
        $mainFiles = Get-ChildItem -Path $mainProjectPath -Recurse -File -ErrorAction SilentlyContinue | 
            Where-Object { $_.FullName -notmatch '\\\.git\\' } |
            ForEach-Object {
                @{
                    RelativePath = $_.FullName.Replace($mainProjectPath, "")
                    Hash = (Get-FileHash $_.FullName -Algorithm MD5).Hash
                    Size = $_.Length
                }
            }
        
        # Compare file counts first
        if ($backupFiles.Count -ne $mainFiles.Count) {
            Write-Host "  Different file counts: Backup=$($backupFiles.Count), Main=$($mainFiles.Count)" -ForegroundColor Red
            $differences += $projectName
            continue
        }
        
        # Create hashtables for comparison
        $backupHashTable = @{}
        foreach ($file in $backupFiles) {
            $backupHashTable[$file.RelativePath] = $file.Hash
        }
        
        $mainHashTable = @{}
        foreach ($file in $mainFiles) {
            $mainHashTable[$file.RelativePath] = $file.Hash
        }
        
        # Check if all files match
        $isIdentical = $true
        foreach ($key in $backupHashTable.Keys) {
            if (-not $mainHashTable.ContainsKey($key) -or $backupHashTable[$key] -ne $mainHashTable[$key]) {
                $isIdentical = $false
                break
            }
        }
        
        if ($isIdentical) {
            Write-Host "  DUPLICATE FOUND - Identical to backup" -ForegroundColor Green
            $duplicates += @{
                Name = $projectName
                Path = $mainProjectPath
                BackupPath = $backupProject.FullName
            }
        } else {
            Write-Host "  Has differences from backup" -ForegroundColor Red
            $differences += $projectName
        }
    }
}

Write-Host "`n`n=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "Total duplicates found: $($duplicates.Count)" -ForegroundColor Green
Write-Host "Projects with differences: $($differences.Count)" -ForegroundColor Red

if ($duplicates.Count -gt 0) {
    Write-Host "`nDuplicate projects:" -ForegroundColor Yellow
    foreach ($dup in $duplicates) {
        Write-Host "  - $($dup.Name)" -ForegroundColor Yellow
    }
    
    Write-Host "`nDo you want to remove these duplicate projects? (Y/N)" -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq 'Y' -or $response -eq 'y') {
        foreach ($dup in $duplicates) {
            Write-Host "Removing duplicate: $($dup.Path)" -ForegroundColor Red
            Remove-Item -Path $dup.Path -Recurse -Force -ErrorAction SilentlyContinue
        }
        Write-Host "`nDuplicates removed successfully!" -ForegroundColor Green
    } else {
        Write-Host "No projects were removed." -ForegroundColor Yellow
    }
} else {
    Write-Host "`nNo duplicate projects found!" -ForegroundColor Green
}
