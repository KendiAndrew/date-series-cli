#!/usr/bin/env python3
"""
Date Series CLI — find a perfect series for your date based on her Instagram.

Usage:
    python main.py <instagram_username>
    python main.py natalie_portman
"""

import sys
import argparse
from instagram import scrape_profile
from ai import recommend_series


def print_separator():
    print("─" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Find a perfect series for your date based on her Instagram profile.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python main.py natalie_portman",
    )
    parser.add_argument("username", help="Instagram username (without @)")
    args = parser.parse_args()

    username = args.username.lstrip("@")

    print_separator()
    print(f"  Scanning Instagram: @{username}")
    print_separator()

    try:
        profile = scrape_profile(username)
    except Exception as e:
        print(f"  [ERROR] Could not load profile: {e}")
        print("  Make sure the account is public and the username is correct.")
        sys.exit(1)

    print(f"  Bio: {profile.bio or '(empty)'}")
    print(f"  Followers: {profile.followers:,}")
    print(f"  Posts scanned: {len(profile.posts)}")
    print_separator()

    print("  Analyzing interests & choosing series...")
    print_separator()

    try:
        result = recommend_series(profile)
    except Exception as e:
        print(f"  [ERROR] AI analysis failed: {e}")
        sys.exit(1)

    print(f"  Her vibe:  {result.get('interests', '—')}")
    print_separator()
    print(f"  RECOMMENDED: {result.get('series', '—')} ({result.get('year', '—')})")
    print(f"  Genre:     {result.get('genre', '—')}")
    print(f"  Platform:  {result.get('platform', '—')}")
    print(f"  Duration:  {result.get('episode_duration', '—')}")
    print(f"  Why:       {result.get('why', '—')}")
    print_separator()
    print(f"  Watch here: {result.get('watch_url', '—')}")
    print_separator()
    print("  Good luck on your date!")
    print_separator()


if __name__ == "__main__":
    main()
