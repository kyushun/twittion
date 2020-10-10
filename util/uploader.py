import requests
from util import notionapi, twitterapi, notifier

notion_url = "https://www.notion.so/"

def upload_images(tweet_status):
    image_urls = twitterapi.get_image_urls(tweet_status)
    tweet_text = twitterapi.get_text(tweet_status)
    tweet_url = twitterapi.get_url(tweet_status)
    tweet_username = twitterapi.get_username(tweet_status)
    tweet_posted_at = twitterapi.get_post_date(tweet_status)

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
    notifier.post(page_url, tweet_status)
