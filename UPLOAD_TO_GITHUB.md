# Upload to GitHub - Step by Step Instructions

Git has been installed! Follow these steps to upload your repository.

## Step 1: Open PowerShell in the Project Directory

1. Navigate to where your `clearcaptions-qa-suite` folder is located
2. Right-click on the `clearcaptions-qa-suite` folder
3. Select "Open in Terminal" or "Open PowerShell window here"

OR manually navigate:
```powershell
cd C:\Users\order\clearcaptions-qa-suite
```

## Step 2: Initialize Git (if not already done)

```powershell
git init
git config user.name "Joseph Karschnik"
git config user.email "your-email@example.com"
```

## Step 3: Add All Files

```powershell
git add .
```

## Step 4: Create Initial Commit

```powershell
git commit -m "Initial commit: ClearCaptions QA Testing Suite

- Comprehensive end-to-end testing framework
- 80+ test cases across 7 categories
- Integration testing for telephony, ASR, and captioning flows
- Accessibility and compliance testing
- Production-ready framework with documentation

Created by Joseph Karschnik"
```

## Step 5: Create Repository on GitHub

1. Go to: **https://github.com/new**
2. Repository name: `clearcaptions-qa-suite`
3. Description: `Comprehensive End-to-End Testing Framework for ClearCaptions Phone Captioning Services`
4. Choose **Public**
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click **"Create repository"**

## Step 6: Connect and Push

After creating the repository, run these commands in PowerShell:

```powershell
git remote add origin https://github.com/joseph-karschnik/clearcaptions-qa-suite.git
git branch -M main
git push -u origin main
```

You'll be prompted for credentials:
- Username: `joseph-karschnik`
- Password: Use a **Personal Access Token** (not your GitHub password)

### To Create a Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: "ClearCaptions QA Upload"
4. Select scopes: Check `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## Alternative: Use GitHub Desktop

If you prefer a GUI:

1. Download: https://desktop.github.com/
2. Sign in with your GitHub account
3. File → Add Local Repository
4. Browse to `clearcaptions-qa-suite` folder
5. Click "Publish repository"
6. Name: `clearcaptions-qa-suite`
7. Make it Public
8. Click "Publish repository"

## Verify Upload

After pushing, your repository will be at:
**https://github.com/joseph-karschnik/clearcaptions-qa-suite**

## Troubleshooting

### "Git is not recognized"
- Restart PowerShell after Git installation
- Or use full path: `"C:\Program Files\Git\bin\git.exe" --version`

### "Nothing to commit"
- Check if files are in the directory: `Get-ChildItem`
- Make sure you're in the right folder
- Check `.gitignore` isn't excluding everything

### Authentication failed
- Use Personal Access Token, not password
- Make sure token has `repo` scope

### Large files
- All files should be small enough
- Check `.gitignore` is working

## Quick Copy-Paste Commands

```powershell
# Navigate to project (adjust path as needed)
cd C:\Users\order\clearcaptions-qa-suite

# Initialize and commit
git init
git config user.name "Joseph Karschnik"
git add .
git commit -m "Initial commit: ClearCaptions QA Testing Suite - Created by Joseph Karschnik"

# After creating repo on GitHub:
git remote add origin https://github.com/joseph-karschnik/clearcaptions-qa-suite.git
git branch -M main
git push -u origin main
```

Good luck! 🚀
