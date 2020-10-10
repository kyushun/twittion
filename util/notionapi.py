import os
from os.path import join, dirname
from notion.client import NotionClient
from notion.block import TextBlock, ImageBlock

notion_token = os.environ.get("NOTION_TOKEN")
notion_database_url = os.environ.get("NOTION_DATABASE_URL")

def create_new_page(title):
    client = NotionClient(token_v2=notion_token)    
    page = client.get_block(notion_database_url)
    row = page.collection.add_row()
    row.name = title
    return row

def set_properties(row, *, text=None, url=None, username=None, posted_at=None):
    if text is not None:
        row.children.add_new(TextBlock, title=text)
    if url is not None:
        row.url = url
    if username is not None:
        row.username = username
    if posted_at is not None:
        row.posted = posted_at

def add_image(row, image_path):
    image = row.children.add_new(ImageBlock)
    image.upload_file(image_path)
