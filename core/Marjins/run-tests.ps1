# Test Runner Scripts for Marjins

## PowerShell Script - Run Tests
param(
    [string]$Configuration = "Debug",
    [string]$TestProject = "Marjins.Tests",
    [switch]$Coverage,
    [switch]$Verbose
)

Write-Host "Running Marjins Test Suite" -ForegroundColor Green
Write-Host "Configuration: $Configuration" -ForegroundColor Yellow

# Build the solution first
Write-Host "Building solution..." -ForegroundColor Blue
dotnet build --configuration $Configuration --no-restore

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed. Exiting."
    exit 1
}

# Run tests
Write-Host "Running tests..." -ForegroundColor Blue

$testArgs = @(
    "test"
    "$TestProject"
    "--configuration"
    $Configuration
    "--no-build"
    "--logger"
    "console;verbosity=normal"
)

if ($Coverage) {
    $testArgs += @(
        "--collect"
        "XPlat Code Coverage"
        "--results-directory"
        "TestResults"
    )
}

if ($Verbose) {
    $testArgs += @(
        "--verbosity"
        "detailed"
    )
}

& dotnet @testArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
    
    if ($Coverage) {
        Write-Host "Code coverage reports generated in TestResults folder" -ForegroundColor Yellow
    }
} else {
    Write-Error "Some tests failed. Check the output above."
    exit 1
}
