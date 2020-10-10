import os
import re
import requests
import tweepy
from util import notionapi, twitterapi
from flask import Flask, request

notion_url = "https://www.notion.so/"
twitter_url_pettern = re.compile(r"^https://twitter.com/.+/status/(\d+)")

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
    tweet_text = twitterapi.get_text(status)
    tweet_url = twitterapi.get_url(status)
    tweet_username = twitterapi.get_username(status)
    tweet_posted_at = twitterapi.get_post_date(status)

    page = notionapi.create_new_page(tweet_text)
    notionapi.set_properties(page, url=tweet_url, username=tweet_username, posted_at=tweet_posted_at)

    for url in image_urls:
        response = requests.get(url)
        image = response.content

        filename = url.split("/")[-1]
        filepath = f"/tmp/{filename}.png"
        with open(filepath, "wb") as f:
            f.write(image)

        notionapi.add_image(page, filepath)

    page_url = notion_url + page.id.replace("-", "")
    return page_url

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
