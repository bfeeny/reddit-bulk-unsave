# Reddit Saved Posts Management Tool

A Python utility for managing Reddit saved posts using the official Reddit API (PRAW). This tool allows you to bulk unsave posts, export saved posts to various formats, and manage your Reddit saved items programmatically.

## Features

- **Bulk Unsave Posts**: Remove all saved posts from your Reddit account
- **Export Saved Posts**: Export your saved posts to CSV, JSON, or HTML bookmarks  
- **Filter by Subreddit**: Target specific subreddits when unsaving
- **Rate Limit Safe**: Respects Reddit API rate limits with automatic throttling
- **Progress Tracking**: Real-time progress indicators and statistics
- **Dry Run Mode**: Preview what will be unsaved without making changes

## Prerequisites

- Python 3.7+
- Reddit API credentials (see Setup section)
- A Reddit account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/reddit-unsave-tool.git
cd reddit-unsave-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Reddit API Setup

To use this tool, you need Reddit API credentials:

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **Name**: Reddit Unsave Tool (or any name you prefer)
   - **App Type**: Select "script"
   - **Description**: Personal tool for managing saved Reddit posts
   - **Redirect URI**: `http://localhost:8080`
4. Click "Create app"
5. Note your credentials:
   - **Client ID**: The string under "personal use script"
   - **Client Secret**: The "secret" value

## Configuration

Create a `config.ini` file in the project root:

```ini
[reddit]
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
user_agent = Reddit Unsave Tool by /u/YOUR_USERNAME
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

**Security Note**: Never commit `config.ini` to version control. It's already in `.gitignore`.

## Usage

### Unsave All Posts

```bash
python unsave_posts.py
```

### Export Saved Posts First (Recommended)

```bash
python export_saved.py --format json
```

### Unsave Posts from Specific Subreddits

```bash
python unsave_posts.py --subreddit technology,programming,python
```

### Dry Run (Preview Only)

```bash
python unsave_posts.py --dry-run
```

### Limit Number of Posts

```bash
python unsave_posts.py --limit 100
```

## Command Line Options

### unsave_posts.py

```
Options:
  --dry-run              Preview what will be unsaved without making changes
  --subreddit NAMES      Comma-separated list of subreddit names to target
  --limit N              Maximum number of posts to unsave
  --verbose              Enable verbose logging
```

### export_saved.py

```
Options:
  --format FORMAT        Output format: csv, json, or html (default: csv)
  --output FILE          Output filename (default: saved_posts.[ext])
  --limit N              Maximum number of posts to export
```

## Rate Limits

Reddit's API rate limits:
- 60 requests per minute for authenticated users
- 600 requests per 10 minutes

This tool automatically:
- Throttles requests to stay within limits
- Retries on rate limit errors
- Shows progress and estimated time remaining

## Example Output

```
Reddit Saved Posts Unsaver
==========================

Connecting to Reddit API...
✓ Connected as: bfeeny

Fetching saved posts...
Found 2847 saved posts

Starting unsave process...
[████████████████████████████████] 2847/2847 (100%)

Summary:
  Total posts: 2847
  Successfully unsaved: 2847
  Failed: 0
  Time elapsed: 4m 23s

All saved posts have been unsaved!
```

## Security Best Practices

- Never commit `config.ini` to version control
- Use a strong, unique Reddit password
- Enable 2FA on your Reddit account
- Store credentials securely
- Review the code before running (it's open source!)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool interacts with your Reddit account. Use at your own risk. Always backup important data before running bulk operations. The author is not responsible for any data loss or account issues.

## Support

If you encounter issues:
1. Check that your Reddit API credentials are correct
2. Ensure you have the latest version of PRAW installed
3. Verify your Reddit account credentials
4. Check Reddit API status at https://www.redditstatus.com/
5. Open an issue on GitHub with error details

## Acknowledgments

- Built with [PRAW](https://praw.readthedocs.io/) (Python Reddit API Wrapper)
- Inspired by the need to manage large collections of saved Reddit content
