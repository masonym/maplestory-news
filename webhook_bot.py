import requests
import json
import os
import time
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
NEWS_API_URL = "https://g.nexonstatic.com/maplestory/cms/v1/news"
CACHE_FILE = "news_cache.json"
CHECK_INTERVAL = 15  # Check every 15 seconds

# Get webhook URL from environment variables
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL not found in environment variables")


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {"last_posts": []}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def fetch_news():
    try:
        response = requests.get(NEWS_API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def send_webhook(post):
    # Build the full image URL
    image_url = (
        f"https://g.nexonstatic.com{post['imageThumbnail']}"
        if post["imageThumbnail"].startswith("/")
        else post["imageThumbnail"]
    )

    # Create the article URL
    article_url = (
        f"https://www.nexon.com/maplestory/news/{post['category']}/{post['id']}"
    )
    send_everyone = False
    if post["category"] == "update":
        send_everyone = True

    embed = {
        "title": post["name"],
        "url": article_url,
        "description": post["summary"],
        "color": 0x00FF00,
        "fields": [
            {"name": "Category", "value": post["category"], "inline": True},
            {
                "name": "Date",
                "value": parser.parse(post["liveDate"]).strftime("%b %d, %Y"),
                "inline": True,
            },
        ],
        "thumbnail": {"url": image_url},
    }

    data = {"embeds": [embed], "content": "@everyone" if send_everyone else None}

    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"Sent notification for new post: {post['name']}")
    except Exception as e:
        print(f"Error sending webhook: {e}")


def check_news():
    print("Checking for new MapleStory news...")
    cache = load_cache()
    last_posts = cache["last_posts"]

    current_posts = fetch_news()
    if not current_posts:
        return

    # Compare with cached posts
    for post in current_posts:
        if not any(cached_post["id"] == post["id"] for cached_post in last_posts):
            # New post found!
            send_webhook(post)

    # Update cache with current posts
    cache["last_posts"] = current_posts
    save_cache(cache)


def main():
    print("Starting MapleStory News Monitor...")
    # Create cache file if it doesn't exist
    if not os.path.exists(CACHE_FILE):
        save_cache({"last_posts": []})

    while True:
        check_news()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
