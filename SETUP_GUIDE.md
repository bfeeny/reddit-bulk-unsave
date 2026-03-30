# GitHub Repository Setup Guide

## Files Created

All files for your GitHub repository have been created in:
`/Users/brianfeeny/Downloads/export_bfeeny_20260329/`

Files with the `GITHUB_` prefix are ready to upload:

1. **GITHUB_README.md** → Rename to `README.md`
2. **GITHUB_unsave_posts.py** → Rename to `unsave_posts.py`
3. **GITHUB_export_saved.py** → Rename to `export_saved.py`
4. **GITHUB_requirements.txt** → Rename to `requirements.txt`
5. **GITHUB_gitignore.txt** → Rename to `.gitignore`
6. **GITHUB_config.ini.example** → Rename to `config.ini.example`
7. **GITHUB_LICENSE** → Rename to `LICENSE`

## Step-by-Step GitHub Setup

### 1. Create a New GitHub Repository

1. Go to https://github.com/new
2. Repository name: `reddit-unsave-tool`
3. Description: `Python tool for managing Reddit saved posts via API`
4. Make it **Public** (required for Reddit API review)
5. Do **NOT** initialize with README, gitignore, or license
6. Click "Create repository"

### 2. Prepare Your Files

```bash
# Create a new directory for the repo
cd ~/Downloads
mkdir reddit-unsave-tool
cd reddit-unsave-tool

# Copy and rename all GitHub files
cp ../export_bfeeny_20260329/GITHUB_README.md README.md
cp ../export_bfeeny_20260329/GITHUB_unsave_posts.py unsave_posts.py
cp ../export_bfeeny_20260329/GITHUB_export_saved.py export_saved.py
cp ../export_bfeeny_20260329/GITHUB_requirements.txt requirements.txt
cp ../export_bfeeny_20260329/GITHUB_gitignore.txt .gitignore
cp ../export_bfeeny_20260329/GITHUB_config.ini.example config.ini.example
cp ../export_bfeeny_20260329/GITHUB_LICENSE LICENSE
```

### 3. Initialize Git and Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Reddit saved posts management tool"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/reddit-unsave-tool.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. For Reddit API Application

When filling out the Reddit API Developer Support form, provide:

**Source Code Repository URL:**
```
https://github.com/YOUR_USERNAME/reddit-unsave-tool
```

**Description of Use:**
```
Personal automation tool for managing saved Reddit posts. Allows bulk 
unsaving of saved posts and exporting saved posts to various formats 
(CSV, JSON, HTML). Used to clean up accumulated saved posts on my 
personal Reddit account. Rate-limited and follows Reddit API best practices.
```

**Redirect URI:**
```
http://localhost:8080
```

## Alternative: Manual Upload via GitHub Web Interface

If you prefer not to use command line:

1. Go to your new repository on GitHub
2. Click "uploading an existing file"
3. Drag and drop all the renamed files
4. Commit the changes

## What to Put in Your Reddit API Application

**Application Name:** Reddit Saved Posts Manager

**Application Type:** Script (for personal use)

**Description:** Personal tool to manage saved Reddit posts including bulk unsaving and exporting to various formats

**About URL:** `https://github.com/YOUR_USERNAME/reddit-unsave-tool`

**Redirect URI:** `http://localhost:8080`

**Link to Source Code:** `https://github.com/YOUR_USERNAME/reddit-unsave-tool`

## Important Notes

- The repository **must be public** so Reddit can review your code
- Never commit your actual `config.ini` file (it's in `.gitignore`)
- The example `config.ini.example` shows the format but has placeholder values
- Your actual credentials stay private on your local machine

## Testing Before Submitting

1. Make sure the repository is public and accessible
2. Verify README.md displays correctly
3. Check that all files are present
4. Test the link works in an incognito browser window

## After Reddit Approves Your API Access

1. Create your `config.ini` file locally (never commit this!)
2. Follow the README instructions to use the tool
3. Run `python unsave_posts.py` to unsave your posts

---

**Questions?** The README.md file in your repository has full documentation!
