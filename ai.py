import json
import anthropic
from instagram import ProfileData

_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


SYSTEM_PROMPT = "You are a helpful assistant. Always respond with valid JSON only, no markdown, no code blocks."

ANALYZE_PROMPT = """You are helping pick a perfect TV series for a first date evening.

Instagram profile data:
- Username: {username}
- Bio: {bio}
- Followers: {followers}
- Recent posts (captions + hashtags):
{posts}

Instructions:
1. Analyze her personality, aesthetic preferences, and likely genre interests from the data above
2. Recommend exactly ONE TV series perfect for a cozy first date — engaging but not too heavy, good for conversation
3. The series MUST be available on Netflix or HBO Max (user has subscriptions to both)
4. Avoid horror, extreme violence, or anything depressing

Respond ONLY with this JSON structure:
{{
    "interests": "2-3 sentence analysis of her vibe and interests based on the profile",
    "series": "Exact Series Title",
    "year": 2021,
    "genre": "Genre / Subgenre",
    "platform": "Netflix",
    "why": "Why this series fits her personality specifically",
    "episode_duration": "~40 min per episode",
    "watch_url": "https://www.netflix.com/search?q=Title"
}}"""


def recommend_series(profile: ProfileData) -> dict:
    posts_text = "\n".join(
        f"  • {p['caption'][:200].strip()} {' '.join('#' + h for h in p['hashtags'][:5])}"
        for p in profile.posts
        if p["caption"].strip()
    ) or "  (no captions available)"

    prompt = ANALYZE_PROMPT.format(
        username=profile.username,
        bio=profile.bio or "(no bio)",
        followers=profile.followers,
        posts=posts_text,
    )

    response = get_client().messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return json.loads(response.content[0].text)
