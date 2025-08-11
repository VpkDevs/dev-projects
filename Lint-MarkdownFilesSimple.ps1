# Markdown File Linter for what-belongs-here.md files
# Validates that each file contains required sections and follows content rules.

param(
    [string]$Path = ".",
    [switch]$Detailed,
    [string]$ReportFile = "lint_report_ps.txt"
)

# Required sections in order
$RequiredSections = @(
    "Category Definition",
    "Inclusion Criteria",
    "Examples That Belong",
    "Examples That Do NOT Belong",
    "Where to Move Non-Matching Projects"
)

function Find-MarkdownFiles {
    param([string]$BasePath)
    
    Get-ChildItem -Path $BasePath -Filter "what-belongs-here*.md" -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch "generation-report" } |
        ForEach-Object { $_.FullName }
}

function Get-FileSections {
    param([string]$Content)
    
    $sections = @{}
    $lines = $Content -split "`n"
    $currentSection = $null
    $currentContent = @()
    $currentLineNum = 0
    
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].Trim()
        
        if ($line -match '^## (.+)$') {
            # Save previous section
            if ($currentSection) {
                $sections[$currentSection] = @{
                    LineNumber = $currentLineNum
                    Content = $currentContent -join "`n"
                }
            }
            
            # Start new section
            $currentSection = $Matches[1].Trim()
            $currentContent = @()
            $currentLineNum = $i + 1
        }
        elseif ($currentSection) {
            $currentContent += $lines[$i]
        }
    }
    
    # Save last section
    if ($currentSection) {
        $sections[$currentSection] = @{
            LineNumber = $currentLineNum
            Content = $currentContent -join "`n"
        }
    }
    
    return $sections
}

function Test-CriteriaBullets {
    param([string]$Content)
    
    $requiredCount = 0
    $optionalCount = 0
    
    $lines = $Content -split "`n"
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match '^- ') {
            if ($trimmed -match '\*\(optional\)\*') {
                $optionalCount++
            }
            else {
                $requiredCount++
            }
        }
    }
    
    return @{
        Required = $requiredCount
        Optional = $optionalCount
        Total = $requiredCount + $optionalCount
    }
}

function Test-ExamplesSection {
    param([string]$Content)
    
    $hasExample = $false
    $lines = $Content -split "`n"
    
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        # Check for numbered examples (1. **name**: description)
        if ($trimmed -match '^\d+\.\s+\*\*[^*]+\*\*:') {
            $hasExample = $true
            break
        }
        # Check for bullet examples (- **name**: description)
        elseif ($trimmed -match '^-\s+\*\*[^*]+\*\*:') {
            $hasExample = $true
            break
        }
    }
    
    return $hasExample
}

function Test-CounterExamplesSection {
    param([string]$Content)
    
    $hasExample = $false
    $hasShouldBeIn = $false
    $lines = $Content -split "`n"
    
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        # Check for numbered examples
        if ($trimmed -match '^\d+\.\s+\*\*[^*]+\*\*:') {
            $hasExample = $true
        }
        # Check for "Should be in:" indication
        elseif ($trimmed -match '^-\s+\*Should be in:\*') {
            $hasShouldBeIn = $true
        }
    }
    
    return @{
        HasExample = $hasExample
        HasShouldBeIn = $hasShouldBeIn
    }
}

function Test-MarkdownFile {
    param([string]$FilePath)
    
    $result = @{
        FilePath = $FilePath
        IsValid = $true
        Errors = @()
        Warnings = @()
    }
    
    try {
        $content = Get-Content -Path $FilePath -Raw -ErrorAction Stop
    }
    catch {
        $result.IsValid = $false
        $result.Errors += "Failed to read file: $_"
        return $result
    }
    
    # Extract sections
    $sections = Get-FileSections -Content $content
    
    # Check 1: All required sections present and in order
    $foundSections = @()
    foreach ($section in $RequiredSections) {
        if ($sections.ContainsKey($section)) {
            $foundSections += $section
        }
        else {
            $result.Errors += "Missing required section: '$section'"
            $result.IsValid = $false
        }
    }
    
    # Check section order
    if ($foundSections.Count -eq $RequiredSections.Count) {
        $positions = @()
        foreach ($section in $RequiredSections) {
            if ($sections.ContainsKey($section)) {
                $positions += $sections[$section].LineNumber
            }
        }
        
        $sortedPositions = $positions | Sort-Object
        if (Compare-Object $positions $sortedPositions) {
            $result.Errors += "Sections are not in the required order"
            $result.IsValid = $false
        }
    }
    
    # Check 2: Inclusion Criteria has 3-5 bullets
    if ($sections.ContainsKey("Inclusion Criteria")) {
        $bullets = Test-CriteriaBullets -Content $sections["Inclusion Criteria"].Content
        
        if ($bullets.Total -lt 3) {
            $result.Errors += "Inclusion Criteria has $($bullets.Total) bullets, minimum is 3"
            $result.IsValid = $false
        }
        elseif ($bullets.Total -gt 5) {
            $result.Warnings += "Inclusion Criteria has $($bullets.Total) bullets, recommended maximum is 5"
        }
        
        if ($bullets.Required -lt 3) {
            $result.Errors += "Inclusion Criteria should have at least 3 required criteria (found $($bullets.Required))"
            $result.IsValid = $false
        }
    }
    
    # Check 3: Examples section has at least one example
    if ($sections.ContainsKey("Examples That Belong")) {
        $hasExamples = Test-ExamplesSection -Content $sections["Examples That Belong"].Content
        if (-not $hasExamples) {
            $result.Errors += "Examples That Belong: No properly formatted examples found"
            $result.IsValid = $false
        }
    }
    
    # Check 4: Counter-examples section has at least one example
    if ($sections.ContainsKey("Examples That Do NOT Belong")) {
        $counterCheck = Test-CounterExamplesSection -Content $sections["Examples That Do NOT Belong"].Content
        
        if (-not $counterCheck.HasExample) {
            $result.Errors += "Examples That Do NOT Belong: No properly formatted counter-examples found"
            $result.IsValid = $false
        }
        elseif (-not $counterCheck.HasShouldBeIn) {
            $result.Errors += "Examples That Do NOT Belong: Counter-examples should include 'Should be in:' notes"
            $result.IsValid = $false
        }
    }
    
    # Additional validation: Check for placeholder text
    if ($content -match 'Example [45]') {
        $result.Warnings += "File contains placeholder example text that should be replaced"
    }
    if ($content -match 'Misplaced Project') {
        $result.Warnings += "File contains placeholder counter-example text that should be replaced"
    }
    if ($content -match 'To be determined') {
        $result.Warnings += "File contains 'To be determined' text that should be updated"
    }
    
    return $result
}

function Write-ValidationResult {
    param($Result)
    
    $relativePath = [System.IO.Path]::GetRelativePath($Path, $Result.FilePath)
    
    if ($Result.IsValid -and $Result.Warnings.Count -eq 0) {
        Write-Host "[PASS] $relativePath - VALID" -ForegroundColor Green
    }
    elseif ($Result.IsValid -and $Result.Warnings.Count -gt 0) {
        Write-Host "[WARN] $relativePath - VALID WITH WARNINGS" -ForegroundColor Yellow
        if ($Detailed) {
            foreach ($warning in $Result.Warnings) {
                Write-Host "  --> $warning" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host "[FAIL] $relativePath - INVALID" -ForegroundColor Red
        if ($Detailed) {
            foreach ($error in $Result.Errors) {
                Write-Host "  [X] $error" -ForegroundColor Red
            }
            foreach ($warning in $Result.Warnings) {
                Write-Host "  --> $warning" -ForegroundColor Yellow
            }
        }
    }
}

function Write-Report {
    param(
        [array]$Results,
        [string]$OutputFile
    )
    
    $report = @()
    $report += "MARKDOWN FILE VALIDATION REPORT"
    $report += "=" * 80
    $report += ""
    
    # Invalid files
    $invalidResults = $Results | Where-Object { -not $_.IsValid }
    if ($invalidResults) {
        $report += "FILES REQUIRING MANUAL REVIEW (INVALID):"
        $report += "-" * 40
        $report += ""
        
        foreach ($result in $invalidResults) {
            $report += "File: $($result.FilePath)"
            $report += "Errors:"
            foreach ($error in $result.Errors) {
                $report += "  - $error"
            }
            if ($result.Warnings) {
                $report += "Warnings:"
                foreach ($warning in $result.Warnings) {
                    $report += "  - $warning"
                }
            }
            $report += ""
        }
    }
    
    # Files with warnings
    $warningResults = $Results | Where-Object { $_.IsValid -and $_.Warnings.Count -gt 0 }
    if ($warningResults) {
        $report += ""
        $report += "FILES WITH WARNINGS (VALID BUT COULD BE IMPROVED):"
        $report += "-" * 40
        $report += ""
        
        foreach ($result in $warningResults) {
            $relativePath = [System.IO.Path]::GetRelativePath($Path, $result.FilePath)
            $report += "File: $relativePath"
            $report += "Warnings:"
            foreach ($warning in $result.Warnings) {
                $report += "  - $warning"
            }
            $report += ""
        }
    }
    
    # Summary
    $validCount = ($Results | Where-Object { $_.IsValid }).Count
    $invalidCount = ($Results | Where-Object { -not $_.IsValid }).Count
    $warningCount = ($Results | Where-Object { $_.Warnings.Count -gt 0 }).Count
    
    $report += ""
    $report += "SUMMARY:"
    $report += "-" * 40
    $report += "Total files checked: $($Results.Count)"
    $report += "Valid files: $validCount"
    $report += "Invalid files: $invalidCount"
    $report += "Files with warnings: $warningCount"
    
    $report | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "`nDetailed report saved to: $OutputFile" -ForegroundColor Cyan
}

# Main execution
Write-Host "Markdown File Linter" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan

# Find all markdown files
$mdFiles = Find-MarkdownFiles -BasePath $Path

if ($mdFiles.Count -eq 0) {
    Write-Host "No what-belongs-here*.md files found." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($mdFiles.Count) markdown files to validate`n" -ForegroundColor Cyan

# Validate each file
$results = @()
foreach ($file in $mdFiles) {
    $result = Test-MarkdownFile -FilePath $file
    $results += $result
    Write-ValidationResult -Result $result
}

# Summary
Write-Host "`n$("=" * 80)" -ForegroundColor Cyan
Write-Host "`nVALIDATION SUMMARY:" -ForegroundColor Cyan

$validCount = ($results | Where-Object { $_.IsValid }).Count
$invalidCount = ($results | Where-Object { -not $_.IsValid }).Count
$warningCount = ($results | Where-Object { $_.Warnings.Count -gt 0 }).Count

Write-Host "  Total files checked: $($results.Count)"
Write-Host "  [PASS] Valid files: $validCount" -ForegroundColor Green
Write-Host "  [FAIL] Invalid files: $invalidCount" -ForegroundColor Red
Write-Host "  [WARN] Files with warnings: $warningCount" -ForegroundColor Yellow

# Generate report if there are issues
if ($invalidCount -gt 0 -or $warningCount -gt 0) {
    Write-Report -Results $results -OutputFile $ReportFile
}

# Exit with appropriate code
exit $(if ($invalidCount -eq 0) { 0 } else { 1 })
