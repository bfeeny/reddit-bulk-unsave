#!/usr/bin/env python3
"""
Reddit Saved Posts Unsaver
Bulk unsave all saved posts from your Reddit account using the official Reddit API.

Usage:
    python unsave_posts.py
    python unsave_posts.py --dry-run
    python unsave_posts.py --subreddit technology,programming
    python unsave_posts.py --limit 100
"""

import praw
import argparse
import time
import configparser
from datetime import datetime
import sys

class RedditUnsaver:
    def __init__(self, config_file='config.ini'):
        """Initialize Reddit API connection."""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        self.reddit = praw.Reddit(
            client_id=self.config['reddit']['client_id'],
            client_secret=self.config['reddit']['client_secret'],
            user_agent=self.config['reddit']['user_agent'],
            username=self.config['reddit']['username'],
            password=self.config['reddit']['password']
        )
        
        self.stats = {
            'total': 0,
            'unsaved': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def verify_connection(self):
        """Verify Reddit API connection."""
        try:
            user = self.reddit.user.me()
            print(f"✓ Connected as: {user.name}\n")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def fetch_saved_posts(self, limit=None):
        """Fetch all saved posts."""
        print("Fetching saved posts...")
        saved_items = []
        
        try:
            for item in self.reddit.user.me().saved(limit=limit):
                saved_items.append(item)
                if len(saved_items) % 100 == 0:
                    print(f"  Fetched {len(saved_items)} items...", end='\r')
            
            print(f"Found {len(saved_items)} saved posts\n")
            return saved_items
        
        except Exception as e:
            print(f"✗ Error fetching saved posts: {e}")
            return []
    
    def unsave_posts(self, saved_items, dry_run=False, subreddit_filter=None):
        """Unsave posts with rate limiting and progress tracking."""
        self.stats['total'] = len(saved_items)
        
        if dry_run:
            print("🔍 DRY RUN MODE - No posts will be unsaved\n")
        
        print("Starting unsave process...\n")
        start_time = time.time()
        
        for i, item in enumerate(saved_items, 1):
            try:
                # Get subreddit name
                if hasattr(item, 'subreddit'):
                    subreddit_name = item.subreddit.display_name
                else:
                    subreddit_name = "unknown"
                
                # Filter by subreddit if specified
                if subreddit_filter and subreddit_name not in subreddit_filter:
                    self.stats['skipped'] += 1
                    continue
                
                # Get title/body preview
                if hasattr(item, 'title'):
                    preview = item.title[:50]
                else:
                    preview = str(item)[:50]
                
                # Progress bar
                progress = int((i / len(saved_items)) * 50)
                bar = '█' * progress + '░' * (50 - progress)
                
                print(f"[{bar}] {i}/{len(saved_items)} - r/{subreddit_name}", end='\r')
                
                # Unsave (unless dry run)
                if not dry_run:
                    item.unsave()
                    self.stats['unsaved'] += 1
                else:
                    self.stats['unsaved'] += 1
                
                # Rate limiting: ~30 requests per minute
                time.sleep(2)
                
            except Exception as e:
                self.stats['failed'] += 1
                print(f"\n✗ Error unsaving post {i}: {e}")
                continue
        
        # Final newline after progress bar
        print()
        
        elapsed_time = time.time() - start_time
        self.print_summary(elapsed_time, dry_run)
    
    def print_summary(self, elapsed_time, dry_run=False):
        """Print operation summary."""
        print(f"\n{'='*60}")
        print("Summary:")
        print(f"  Total posts: {self.stats['total']}")
        
        if dry_run:
            print(f"  Would unsave: {self.stats['unsaved']}")
        else:
            print(f"  Successfully unsaved: {self.stats['unsaved']}")
        
        if self.stats['skipped'] > 0:
            print(f"  Skipped (filtered): {self.stats['skipped']}")
        
        if self.stats['failed'] > 0:
            print(f"  Failed: {self.stats['failed']}")
        
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"  Time elapsed: {minutes}m {seconds}s")
        print(f"{'='*60}\n")
        
        if not dry_run and self.stats['unsaved'] > 0:
            print("✓ All saved posts have been unsaved!")
        elif dry_run:
            print("🔍 Dry run complete. Run without --dry-run to actually unsave.")

def main():
    parser = argparse.ArgumentParser(
        description='Bulk unsave Reddit saved posts using the official API'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what will be unsaved without making changes'
    )
    parser.add_argument(
        '--subreddit',
        type=str,
        help='Comma-separated list of subreddit names to target'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Maximum number of posts to unsave'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Parse subreddit filter
    subreddit_filter = None
    if args.subreddit:
        subreddit_filter = [s.strip() for s in args.subreddit.split(',')]
    
    # Print header
    print(f"\n{'='*60}")
    print("Reddit Saved Posts Unsaver")
    print(f"{'='*60}\n")
    
    print("Connecting to Reddit API...")
    
    # Initialize unsaver
    try:
        unsaver = RedditUnsaver()
    except FileNotFoundError:
        print("✗ Error: config.ini file not found!")
        print("\nCreate a config.ini file with your Reddit API credentials.")
        print("See README.md for setup instructions.")
        sys.exit(1)
    except KeyError as e:
        print(f"✗ Error: Missing configuration key: {e}")
        print("\nCheck your config.ini file. See README.md for required fields.")
        sys.exit(1)
    
    # Verify connection
    if not unsaver.verify_connection():
        sys.exit(1)
    
    # Fetch saved posts
    saved_items = unsaver.fetch_saved_posts(limit=args.limit)
    
    if not saved_items:
        print("No saved posts found!")
        sys.exit(0)
    
    # Confirm before proceeding (unless dry run)
    if not args.dry_run:
        response = input(f"Unsave {len(saved_items)} posts? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Unsave posts
    unsaver.unsave_posts(
        saved_items,
        dry_run=args.dry_run,
        subreddit_filter=subreddit_filter
    )

if __name__ == '__main__':
    main()
