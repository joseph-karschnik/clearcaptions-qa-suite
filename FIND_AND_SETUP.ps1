# Find the project files and set up Git repository
Write-Host "Finding ClearCaptions QA Suite files..." -ForegroundColor Cyan

# Search for README.md in common locations
$possiblePaths = @(
    "C:\Users\order\clearcaptions-qa-suite",
    "$PSScriptRoot",
    "$PWD",
    (Get-Location).Path
)

$projectPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path (Join-Path $path "README.md")) {
        $projectPath = $path
        Write-Host "✓ Found project at: $projectPath" -ForegroundColor Green
        break
    }
}

if (-not $projectPath) {
    Write-Host "Searching for project files..." -ForegroundColor Yellow
    $readme = Get-ChildItem -Path C:\Users\order -Recurse -Filter "README.md" -ErrorAction SilentlyContinue | 
        Where-Object { $_.DirectoryName -like "*clearcaptions*" } | 
        Select-Object -First 1
    
    if ($readme) {
        $projectPath = $readme.DirectoryName
        Write-Host "✓ Found project at: $projectPath" -ForegroundColor Green
    }
}

if (-not $projectPath) {
    Write-Host "✗ Could not find project files. Please navigate to the clearcaptions-qa-suite directory manually." -ForegroundColor Red
    Write-Host "Then run: git init && git add . && git commit -m 'Initial commit'" -ForegroundColor Yellow
    exit 1
}

# Change to project directory
Set-Location $projectPath
Write-Host "Changed to: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Check for Git
$gitPath = "C:\Program Files\Git\bin\git.exe"
if (-not (Test-Path $gitPath)) {
    Write-Host "Git not found at standard location. Trying to find it..." -ForegroundColor Yellow
    $gitPath = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitPath) {
        Write-Host "✗ Git not found. Please install Git first." -ForegroundColor Red
        exit 1
    }
    $gitPath = $gitPath.Source
}

Write-Host "Using Git at: $gitPath" -ForegroundColor Green
Write-Host ""

# Initialize repository
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    & $gitPath init
    Write-Host "✓ Repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Repository already initialized" -ForegroundColor Green
}

# Configure user
& $gitPath config user.name "Joseph Karschnik"
Write-Host "✓ User configured" -ForegroundColor Green

# Add all files
Write-Host "Adding files..." -ForegroundColor Yellow
& $gitPath add -A
$fileCount = (& $gitPath status --short | Measure-Object).Count
Write-Host "✓ Added files (status shows $fileCount items)" -ForegroundColor Green

# Show what will be committed
Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
& $gitPath status --short | Select-Object -First 30

# Create commit
Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Yellow
$commitMsg = @"
Initial commit: ClearCaptions QA Testing Suite

- Comprehensive end-to-end testing framework
- 80+ test cases across 7 categories
- Integration testing for telephony, ASR, and captioning flows
- Accessibility and compliance testing
- Production-ready framework with documentation

Created by Joseph Karschnik
"@

& $gitPath commit -m $commitMsg
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit created successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠ No changes to commit (files may already be committed or .gitignore is excluding everything)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create repository at: https://github.com/new" -ForegroundColor White
Write-Host "   Name: clearcaptions-qa-suite" -ForegroundColor Yellow
Write-Host "   Description: Comprehensive End-to-End Testing Framework for ClearCaptions" -ForegroundColor Yellow
Write-Host "   Make it Public" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Then run these commands:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/joseph-karschnik/clearcaptions-qa-suite.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
