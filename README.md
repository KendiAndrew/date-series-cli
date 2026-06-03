# Date Series CLI

Scans a public Instagram profile, analyzes her interests with Claude AI, and recommends a perfect TV series for a date night on Netflix or HBO Max.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python main.py <instagram_username>
```

**Example:**
```bash
python main.py natalie_portman
```

**Output:**
```
──────────────────────────────────────────────────
  Scanning Instagram: @natalie_portman
──────────────────────────────────────────────────
  Bio: Actor, producer...
  Followers: 9,200,000
  Posts scanned: 15
──────────────────────────────────────────────────
  Analyzing interests & choosing series...
──────────────────────────────────────────────────
  Her vibe:  Artistic, socially conscious, loves cinema and culture
──────────────────────────────────────────────────
  RECOMMENDED: The Bear (2022)
  Genre:     Drama / Comedy
  Platform:  Hulu / Disney+
  Duration:  ~30 min per episode
  Why:       Fast-paced, critically acclaimed — great conversation starter
──────────────────────────────────────────────────
  Watch here: https://www.netflix.com/search?q=The+Bear
──────────────────────────────────────────────────
  Good luck on your date!
──────────────────────────────────────────────────
```

## Architecture

```
main.py          → CLI entrypoint, argument parsing, formatted output
instagram.py     → Public profile scraping via instaloader (no login required)
ai.py            → Claude claude-opus-4-8 prompt: analyze interests → recommend series
```

**Pipeline:**
```
CLI input (username)
  → instaloader scrapes public profile (bio, captions, hashtags)
  → Claude analyzes personality & interests
  → Claude recommends series available on Netflix / HBO Max
  → Formatted output with direct watch link
```

## Requirements

- Python 3.10+
- `ANTHROPIC_API_KEY` environment variable
- Target Instagram account must be **public**
