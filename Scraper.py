
import instaloader
from pathlib import Path

PROFILE = "kraftkorner.clx"

L = instaloader.Instaloader(
    download_pictures=False,
    download_video_thumbnails=False,
    save_metadata=False,
    compress_json=False
)

profile = instaloader.Profile.from_username(L.context, PROFILE)
posts = []

for post in profile.get_posts():
    if not post.is_video:
        continue

    text = (post.caption or "").lower()

    if "resin" in text or "epoxy" in text:
        category = "Resin Gifts"
    elif "miniature" in text:
        category = "Miniatures"
    elif "frame" in text:
        category = "Photo Frames"
    elif "mug" in text or "bottle" in text:
        category = "Sublimation"
    elif "magnet" in text:
        category = "Fridge Magnets"
    else:
        category = "Custom Gifts"

    posts.append({
        "title": (post.caption or "Instagram Reel").split("\n")[0][:60],
        "url": f"https://www.instagram.com/reel/{post.shortcode}/",
        "thumb": post.url,
        "category": category
    })

html = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#f5f5f5;padding:15px}
.card{background:#fff;border-radius:14px;padding:12px;margin:12px 0;
display:flex;gap:12px}
img{width:95px;height:95px;border-radius:10px;object-fit:cover}
.btn{background:#E1306C;color:#fff;padding:8px 12px;
text-decoration:none;border-radius:8px;display:inline-block}
small{color:#666}
</style></head><body>
<h2>Kraft Korner Catalogue</h2>
"""

for p in posts:
    html += f"""
    <div class="card">
        <img src="{p['thumb']}">
        <div>
            <b>{p['title']}</b><br>
            <small>{p['category']}</small><br><br>
            <a class="btn" href="{p['url']}">Watch Reel</a>
        </div>
    </div>
    """

html += "</body></html>"

Path("catalogue.html").write_text(html, encoding="utf-8")
print("Generated", len(posts), "reels")
