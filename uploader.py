import os
from os.path import join, dirname
from dotenv import load_dotenv
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

notion_token = os.environ.get("NOTION_TOKEN")
client = NotionClient(token_v2=notion_token)

notion_database_url = os.environ.get("NOTION_DATABASE_URL")
page = client.get_block(notion_database_url)

def create_new_page(title):
    row = page.collection.add_row()
    row.name = title
    return row

def set_properties(row, *, text=None, url=None, username=None):
    if text is not None:
        row.children.add_new(TextBlock, title=text)
    if url is not None:
        row.url = url
    if username is not None:
        row.username = username

def add_image(row, image_path):
    image = row.children.add_new(ImageBlock)
    image.upload_file(image_path)
