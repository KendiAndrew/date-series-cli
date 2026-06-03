#!/usr/bin/env python3
"""
Date Series CLI — find a perfect series for your date based on her Instagram.

Usage:
    python main.py <instagram_username>
    python main.py natalie_portman
    python main.py --demo sofia_demo   # use sample data (no Instagram login needed)
"""

import sys
import argparse
from dataclasses import dataclass, field
from instagram import scrape_profile, ProfileData
from ai import recommend_series


DEMO_PROFILE = ProfileData(
    username="sofia_demo",
    bio="🎨 Художниця | кава та книги | Київ ☕📚 lover of quiet mornings and good stories",
    followers=3420,
    posts=[
        {"caption": "Нарешті закінчила нову ілюстрацію 🖌️ місяцями збиралась", "hashtags": ["art", "illustration", "handmade"], "likes": 312},
        {"caption": "Цей роман змінив моє розуміння часу. Рекомендую всім хто любить магічний реалізм", "hashtags": ["books", "reading", "booklover"], "likes": 289},
        {"caption": "Ранкова кава і скетчбук — ідеальний початок дня ☕", "hashtags": ["morning", "coffee", "sketch"], "likes": 401},
        {"caption": "Переглянула весь серіал за вихідні. Не могла зупинитись 😅", "hashtags": ["series", "netflix", "weekend"], "likes": 198},
        {"caption": "Осінній Київ — найкращий Київ 🍂", "hashtags": ["kyiv", "autumn", "city"], "likes": 534},
    ],
)


def print_separator():
    print("─" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Find a perfect series for your date based on her Instagram profile.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python main.py natalie_portman\n       python main.py --demo sofia",
    )
    parser.add_argument("username", help="Instagram username (without @)")
    parser.add_argument("--demo", action="store_true", help="Use sample profile data (no Instagram scraping)")
    args = parser.parse_args()

    username = args.username.lstrip("@")

    print_separator()
    print(f"  Scanning Instagram: @{username}")
    print_separator()

    if args.demo:
        profile = DEMO_PROFILE
        profile.username = username
        print("  [DEMO MODE] Using sample profile data")
    else:
        try:
            profile = scrape_profile(username)
        except Exception as e:
            print(f"  [ERROR] Could not load profile: {e}")
            print("  Make sure the account is public and the username is correct.")
            print("  Tip: use --demo flag to test with sample data")
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
