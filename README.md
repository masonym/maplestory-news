# MapleStory News Parser

This bot monitors the MapleStory news page and automatically sends updates to a specified Discord webhook whenever new news items are published.

## Features

- Monitors MapleStory news page every 15 seconds
- Posts new articles with embedded formatting
- Includes article category, date, title, and summary
- Caches previous posts to avoid duplicates

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the webhook URL:
   - Create a Discord webhook URL in your Discord server and place it in the environment variable `DISCORD_WEBHOOK_URL`

3. Run the bot:
```bash
python webhook_bot.py
```

## Configuration

You can modify these settings in `webhook_bot.py`:
- `CHECK_INTERVAL`: How often to check for new posts (in seconds)
- `NEWS_URL`: The MapleStory news page URL to monitor

## Note

Make sure to keep your bot token private and never share it with others.
