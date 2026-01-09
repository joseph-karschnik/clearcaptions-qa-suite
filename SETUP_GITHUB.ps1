# PowerShell script to set up and push to GitHub
# Run this script from the clearcaptions-qa-suite directory

Write-Host "ClearCaptions QA Suite - GitHub Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed. Please install from https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "✗ Please run this script from the clearcaptions-qa-suite directory" -ForegroundColor Red
    exit 1
}

Write-Host "✓ In correct directory" -ForegroundColor Green
Write-Host ""

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

Write-Host ""

# Configure git user (if not already set)
$userName = git config --global user.name
$userEmail = git config --global user.email

if (-not $userName) {
    Write-Host "Git user name not set. Please configure:" -ForegroundColor Yellow
    $name = Read-Host "Enter your name (or press Enter to skip)"
    if ($name) {
        git config --global user.name $name
    }
}

if (-not $userEmail) {
    Write-Host "Git user email not set. Please configure:" -ForegroundColor Yellow
    $email = Read-Host "Enter your email (or press Enter to skip)"
    if ($email) {
        git config --global user.email $email
    }
}

Write-Host ""

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: ClearCaptions QA Testing Suite

- Comprehensive end-to-end testing framework
- 80+ test cases across 7 categories
- Integration testing for telephony, ASR, and captioning flows
- Accessibility and compliance testing
- Production-ready framework with documentation

Created by Joseph Karschnik"
    Write-Host "✓ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "✓ No changes to commit (already committed)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host "   Name: clearcaptions-qa-suite" -ForegroundColor White
Write-Host "   Description: Comprehensive End-to-End Testing Framework for ClearCaptions" -ForegroundColor White
Write-Host ""
Write-Host "2. After creating the repository, run these commands:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/joseph-karschnik/clearcaptions-qa-suite.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or use GitHub Desktop for a GUI approach!" -ForegroundColor Cyan
Write-Host ""
