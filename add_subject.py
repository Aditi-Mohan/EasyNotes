from notion.client import NotionClient
from notion.block import *

def get_user_token():
    # replace with fetching token for that user from database
    return "7a891b7b74950f98146c6059c3939c3dea5be5dedb08440b072aa50199bce91bb5d8577ecb9bcb0b4ac047c6daf144df7e452824e7d6b8a64c8dde7d67ea0b104855df57a4db8b94003411ec1628"

def get_home_page_url():
    # replace with fetching homepage url for that user from database
    return "https://www.notion.so/EasyNotes-439bbafab39d4ad797ccb60292a1be4c"

def add_subject(sub_name):
    token_v2 = get_user_token()
    homepage_url = get_home_page_url()
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    new_sub_page = homepage.children.add_new(PageBlock, title=sub_name)
    new_sub_page.set("format.page_icon", "😃")
    # add new_sub_page -> title and id to database
    # set random icons

if __name__ == "__main__":
    add_subject("Happiness")
    print("done")