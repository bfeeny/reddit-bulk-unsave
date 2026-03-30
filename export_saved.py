#!/usr/bin/env python3
"""
Reddit Saved Posts Exporter
Export your saved Reddit posts to CSV, JSON, or HTML format.

Usage:
    python export_saved.py --format csv
    python export_saved.py --format json --output my_saved_posts.json
    python export_saved.py --format html --limit 1000
"""

import praw
import argparse
import configparser
import json
import csv
from datetime import datetime
import sys

class RedditExporter:
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
    
    def fetch_saved_posts(self, limit=None):
        """Fetch all saved posts."""
        print("Fetching saved posts...")
        saved_items = []
        
        for item in self.reddit.user.me().saved(limit=limit):
            data = {
                'type': 'submission' if hasattr(item, 'title') else 'comment',
                'subreddit': item.subreddit.display_name if hasattr(item, 'subreddit') else 'unknown',
                'author': str(item.author) if item.author else '[deleted]',
                'created_utc': datetime.fromtimestamp(item.created_utc).isoformat(),
                'url': f"https://reddit.com{item.permalink}",
                'score': item.score if hasattr(item, 'score') else 0,
            }
            
            if hasattr(item, 'title'):
                data['title'] = item.title
                data['selftext'] = item.selftext[:500] if hasattr(item, 'selftext') else ''
            else:
                data['title'] = f"Comment in: {item.link_title if hasattr(item, 'link_title') else 'unknown'}"
                data['selftext'] = item.body[:500] if hasattr(item, 'body') else ''
            
            saved_items.append(data)
            
            if len(saved_items) % 100 == 0:
                print(f"  Fetched {len(saved_items)} items...", end='\r')
        
        print(f"\nFetched {len(saved_items)} saved posts")
        return saved_items
    
    def export_csv(self, saved_items, output_file):
        """Export to CSV format."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=saved_items[0].keys())
            writer.writeheader()
            writer.writerows(saved_items)
        print(f"✓ Exported to {output_file}")
    
    def export_json(self, saved_items, output_file):
        """Export to JSON format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(saved_items, f, indent=2, ensure_ascii=False)
        print(f"✓ Exported to {output_file}")
    
    def export_html(self, saved_items, output_file):
        """Export to HTML bookmarks format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
            f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
            f.write('<TITLE>Reddit Saved Posts</TITLE>\n')
            f.write('<H1>Reddit Saved Posts</H1>\n')
            f.write('<DL><p>\n')
            
            for item in saved_items:
                timestamp = int(datetime.fromisoformat(item['created_utc']).timestamp())
                f.write(f'    <DT><A HREF="{item["url"]}" ADD_DATE="{timestamp}">')
                f.write(f'{item["title"]}</A>\n')
            
            f.write('</DL><p>\n')
        
        print(f"✓ Exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Export Reddit saved posts to various formats'
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'json', 'html'],
        default='csv',
        help='Output format (default: csv)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output filename'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Maximum number of posts to export'
    )
    
    args = parser.parse_args()
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        output_file = f'saved_posts.{args.format}'
    
    print(f"\n{'='*60}")
    print("Reddit Saved Posts Exporter")
    print(f"{'='*60}\n")
    
    print("Connecting to Reddit API...")
    
    try:
        exporter = RedditExporter()
    except FileNotFoundError:
        print("✗ Error: config.ini file not found!")
        sys.exit(1)
    
    # Fetch saved posts
    saved_items = exporter.fetch_saved_posts(limit=args.limit)
    
    if not saved_items:
        print("No saved posts found!")
        sys.exit(0)
    
    # Export
    print(f"\nExporting to {args.format.upper()} format...")
    
    if args.format == 'csv':
        exporter.export_csv(saved_items, output_file)
    elif args.format == 'json':
        exporter.export_json(saved_items, output_file)
    elif args.format == 'html':
        exporter.export_html(saved_items, output_file)
    
    print(f"\n✓ Export complete: {output_file}")

if __name__ == '__main__':
    main()
