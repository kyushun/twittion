import os
import requests
import tweepy
import twitter
import uploader
from flask import Flask, request

notion_url = "https://www.notion.so/"

app = Flask(__name__)

@app.route("/")
def save_images():
    id = request.args.get('id')
    if id is None or not id.isdecimal():
        return "invalid params"

    try:
        status = twitter.get_status(id)
    except tweepy.error.TweepError:
        return "invalid id"
    image_urls = twitter.get_image_urls(status)
    tweet_text = twitter.get_text(status)
    tweet_url = twitter.get_url(status)
    tweet_username = twitter.get_username(status)

    page = uploader.create_new_page(tweet_text)
    uploader.set_properties(page, url=tweet_url, username=tweet_username)

    for url in image_urls:
        response = requests.get(url)
        image = response.content

        filename = url.split("/")[-1]
        filepath = f"/tmp/{filename}.png"
        with open(filepath, "wb") as f:
            f.write(image)

        uploader.add_image(page, filepath)

    page_url = notion_url + page.id.replace("-", "")
    return page_url

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
