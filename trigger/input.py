import feedparser
from datetime import datetime
import pytz
import os
import yaml

## load the yaml file
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
print(config)

if "rss_url" in config["youtube_channel"]:
    rss_url = config["youtube_channel"]["rss_url"]

ist = pytz.timezone('Asia/Kolkata')

# File to store the last seen video ID
last_video_file = "last_video.txt"

# Load last seen video ID
if os.path.exists(last_video_file):
    with open(last_video_file, "r") as f:
        last_seen_video = f.read().strip()
else:
    last_seen_video = None

feed = feedparser.parse(rss_url)

# Filter out Shorts and pick the latest video
latest_video = None
for entry in feed.entries:
    if "/shorts/" in entry.link:
        continue
    latest_video = entry
    break  # Stop after the first normal video

if latest_video:
    if latest_video.yt_videoid != last_seen_video:
        # New video detected
        published_utc = datetime.strptime(latest_video.published, "%Y-%m-%dT%H:%M:%S%z")
        published_ist = published_utc.astimezone(ist)
        
        print("\n🚀 New Video Uploaded!")
        print("Title:", latest_video.title)
        print("Link:", latest_video.link)
        print("Published (IST):", published_ist.strftime("%Y-%m-%d %H:%M:%S"))
        print("Video ID:", latest_video.yt_videoid)
        print("-" * 40)
        
        # Update last seen video ID
        with open(last_video_file, "w") as f:
            f.write(latest_video.yt_videoid)
    else:
        print("No new videos.")
else:
    print("No regular videos found.")
