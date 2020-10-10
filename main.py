import os
import re
import requests
import tweepy
from rq import Queue
from worker import conn
from flask import Flask, request
from util import twitterapi, uploader

twitter_url_pettern = re.compile(r"^https://twitter.com/.+/status/(\d+)")

q = Queue(connection=conn)
app = Flask(__name__)

@app.route("/")
def save_images():
    id = request.args.get('id') or ""
    url_match = twitter_url_pettern.match(id)
    if not id.isdecimal():
        if url_match:
            id = url_match.groups()[0]
        else:
            return "invalid params"

    try:
        status = twitterapi.get_status(id)
    except tweepy.error.TweepError:
        return "invalid id"

    image_urls = twitterapi.get_image_urls(status)
    if len(image_urls) > 0:
        q.enqueue(uploader.upload_images, status)
        return "ok"
    else:
        return "no images"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
