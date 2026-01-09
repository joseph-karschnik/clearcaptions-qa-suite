# ClearCaptions QA Suite - Git Installation and Upload Script
# This script will help install Git and upload to GitHub

Write-Host "ClearCaptions QA Suite - GitHub Upload Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
$gitInstalled = $false
try {
    $null = git --version 2>$null
    $gitInstalled = $true
    Write-Host "✓ Git is already installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed" -ForegroundColor Yellow
}

# If Git is not installed, try to install it
if (-not $gitInstalled) {
    Write-Host ""
    Write-Host "Attempting to install Git..." -ForegroundColor Yellow
    
    # Try winget (Windows Package Manager)
    try {
        $winget = Get-Command winget -ErrorAction SilentlyContinue
        if ($winget) {
            Write-Host "Installing Git via winget..." -ForegroundColor Yellow
            winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
            Write-Host "✓ Git installation initiated via winget" -ForegroundColor Green
            Write-Host "Please restart PowerShell after installation completes, then run this script again." -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Or install manually from: https://git-scm.com/downloads" -ForegroundColor Cyan
            exit 0
        }
    } catch {
        Write-Host "winget not available" -ForegroundColor Yellow
    }
    
    # Try chocolatey
    try {
        $choco = Get-Command choco -ErrorAction SilentlyContinue
        if ($choco) {
            Write-Host "Installing Git via Chocolatey..." -ForegroundColor Yellow
            choco install git -y
            Write-Host "✓ Git installation initiated via Chocolatey" -ForegroundColor Green
            Write-Host "Please restart PowerShell after installation completes, then run this script again." -ForegroundColor Yellow
            exit 0
        }
    } catch {
        Write-Host "Chocolatey not available" -ForegroundColor Yellow
    }
    
    # If neither worked, provide manual instructions
    Write-Host ""
    Write-Host "Automatic installation not available. Please install Git manually:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://git-scm.com/downloads" -ForegroundColor Cyan
    Write-Host "2. Run the installer" -ForegroundColor Cyan
    Write-Host "3. Restart PowerShell" -ForegroundColor Cyan
    Write-Host "4. Run this script again" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "OR use GitHub Desktop (includes Git):" -ForegroundColor Yellow
    Write-Host "Download from: https://desktop.github.com/" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Git is installed, proceed with setup
Write-Host ""
Write-Host "Setting up Git repository..." -ForegroundColor Yellow

# Check if already a git repo
if (Test-Path ".git") {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Configure user
$currentUser = git config user.name
if (-not $currentUser) {
    git config user.name "Joseph Karschnik"
    Write-Host "✓ Git user name configured" -ForegroundColor Green
} else {
    Write-Host "✓ Git user: $currentUser" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "Adding files to repository..." -ForegroundColor Yellow
git add .
$fileCount = (git status --short | Measure-Object).Count
Write-Host "✓ Added $fileCount files" -ForegroundColor Green

# Create commit
Write-Host ""
Write-Host "Creating initial commit..." -ForegroundColor Yellow
$commitMessage = @"
Initial commit: ClearCaptions QA Testing Suite

- Comprehensive end-to-end testing framework
- 80+ test cases across 7 categories
- Integration testing for telephony, ASR, and captioning flows
- Accessibility and compliance testing
- Production-ready framework with documentation

Created by Joseph Karschnik
"@

git commit -m $commitMessage
Write-Host "✓ Initial commit created" -ForegroundColor Green

Write-Host ""
Write-Host "=" -ForegroundColor Cyan
Write-Host "Repository is ready to push!" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is available
try {
    $null = gh --version 2>$null
    Write-Host "GitHub CLI detected. Would you like to create the repository automatically? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Creating repository on GitHub..." -ForegroundColor Yellow
        gh repo create clearcaptions-qa-suite --public --source=. --remote=origin --push
        Write-Host "✓ Repository created and pushed to GitHub!" -ForegroundColor Green
        Write-Host "View at: https://github.com/joseph-karschnik/clearcaptions-qa-suite" -ForegroundColor Cyan
        exit 0
    }
} catch {
    Write-Host "GitHub CLI not available" -ForegroundColor Yellow
}

# Manual instructions
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host "   Name: clearcaptions-qa-suite" -ForegroundColor White
Write-Host "   Description: Comprehensive End-to-End Testing Framework for ClearCaptions" -ForegroundColor White
Write-Host "   Make it Public" -ForegroundColor White
Write-Host "   DO NOT initialize with README" -ForegroundColor White
Write-Host ""
Write-Host "2. After creating, run these commands:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/joseph-karschnik/clearcaptions-qa-suite.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "OR use GitHub Desktop for easier upload!" -ForegroundColor Cyan
Write-Host ""
