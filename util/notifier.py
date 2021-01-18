import os
import requests
import json
from util import twitterapi

webhook_url = os.environ.get("WEBHOOK_URL")

def success(notion_url, tweet_status):
    requests.post(webhook_url, data=json.dumps({
        "attachments":[{
                "pretext": f"The new images have been uploaded successfully!\n{notion_url}",
                "color": "good",
                "author_name": twitterapi.get_username(tweet_status),
                "author_icon": twitterapi.get_profile_image_url(tweet_status),
                "text": twitterapi.get_text(tweet_status),
                "image_url": twitterapi.get_image_urls(tweet_status)[0]
        }]
    }))

def error(tweet_url, message):
    requests.post(webhook_url, data=json.dumps({
        "attachments":[{
                "pretext": tweet_url,
                "color": "danger",
                "text": message
        }]
    }))
