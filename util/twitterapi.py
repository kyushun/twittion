import os
import datetime
import tweepy
from os.path import join, dirname

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def get_status(id):
    api = tweepy.API(auth)  
    return api.get_status(id, tweet_mode='extended')

def get_url(status):
    return f"https://twitter.com/{status.user.id}/status/{status.id}"

def get_username(status):
    return status.user.name

def get_post_date(status):
    return status.created_at + datetime.timedelta(hours=9)

def get_text(status):
    return status.full_text

def get_image_urls(status):
    image_urls = []
    if hasattr(status, "extended_entities") and "media" in status.extended_entities:
        for media in status.extended_entities["media"]:
            image_urls.append(media["media_url_https"])
        image_urls = [url + ":orig" for url in image_urls]
        return image_urls
    else:
        return []
