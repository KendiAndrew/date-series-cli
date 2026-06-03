import instaloader
from dataclasses import dataclass, field


@dataclass
class ProfileData:
    username: str
    bio: str
    followers: int
    posts: list[dict] = field(default_factory=list)


def scrape_profile(username: str, max_posts: int = 15) -> ProfileData:
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        quiet=True,
    )

    profile = instaloader.Profile.from_username(L.context, username)

    posts = []
    for post in profile.get_posts():
        posts.append({
            "caption": (post.caption or "")[:300],
            "hashtags": list(post.caption_hashtags)[:10],
            "likes": post.likes,
        })
        if len(posts) >= max_posts:
            break

    return ProfileData(
        username=profile.username,
        bio=profile.biography or "",
        followers=profile.followers,
        posts=posts,
    )
