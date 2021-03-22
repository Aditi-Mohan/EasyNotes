from notion.client import NotionClient
from notion.block import *
from datetime import datetime
from utils.random_emoji import bookmark_emoji
from utils.random_color import random_color

# def get_user_token():
#     # replace with fetching token for that user from database
#     return "e7efb6c4a8ccd0d1e3c2720985ea3422f71d16c9b62da79a2e4ad12d46c3f73c5799b54493f05f92deff9ef5cb82f11e7977e21c9b53634817c04a9d0ae0523286e65d2392d4e70b23e16fcf7d48"

# def get_home_page_url():
#     # replace with fetching homepage url for that user from database
#     return "https://www.notion.so/EasyNotes-439bbafab39d4ad797ccb60292a1be4c"

def verify_token(token):
    try:
        client = NotionClient(token_v2=token)
    except:
        print('Token not valid')
        return False
    else:
        print('Token valid')
        return True

def verify_homepage_url(token, url):
    client = NotionClient(token_v2=token)
    try:
        homepage = client.get_block(url)
    except:
        print('Not a vaild page')
        return False
    else:
        print('Valid url')
        return True

def get_doc(homepage, sub_name):
    # print(search_blocks(sub_name))
    for page in homepage.children:
        if type(page) == PageBlock:
            if page.title == sub_name:
                return page
    # fetch from database instead of
    # searching for the respective page among children of homepage

async def write_transcript(title, transcript, token_v2, url, sub_name, unit_name, dt_of_creation):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(url)
    sub_page = get_doc(homepage, sub_name)
    unit_page = get_doc(sub_page, unit_name)
    new_page = unit_page.children.add_new(PageBlock, title=title)
    date_block = new_page.children.add_new(TextBlock, title="Created on: "+dt_of_creation)
    date_block.set("format.block_color", "blue_background")
    transcript_block = new_page.children.add_new(SubheaderBlock, title="Transcript")
    new_page.children.add_new(DividerBlock)
    for each in transcript:
        text_block = new_page.children.add_new(TextBlock, title=each)
    return new_page.get_browseable_url()

async def write_transcript_with_bookmarks(title, transcript, token_v2, url, sub_name, unit_name, dt_of_creation):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(url)
    sub_page = get_doc(homepage, sub_name)
    unit_page = get_doc(sub_page, unit_name)
    new_page = unit_page.children.add_new(PageBlock, title=title)
    date_block = new_page.children.add_new(TextBlock, title="Created on: "+dt_of_creation)
    date_block.set("format.block_color", "blue_background")
    transcript_block = new_page.children.add_new(SubheaderBlock, title="Transcript")
    new_page.children.add_new(DividerBlock)
    for each, is_bm in transcript:
        if is_bm == 0:
            text_block = new_page.children.add_new(TextBlock, title=each[0])
        else:
            callout_block = new_page.children.add_new(CalloutBlock, title=each[0], icon=bookmark_emoji)
            callout_block.set("format.block_color", random_color()+"_background")
    return new_page.get_browseable_url()
    
async def write_transcript_with_frames_and_bookmarks(title, frames, transcript, token_v2, url, sub_name, unit_name, dt_of_creation):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(url)
    sub_page = get_doc(homepage, sub_name)
    unit_page = get_doc(sub_page, unit_name)
    new_page = unit_page.children.add_new(PageBlock, title=title)
    date_block = new_page.children.add_new(TextBlock, title="Created on: "+dt_of_creation)
    date_block.set("format.block_color", "blue_background")
    transcript_block = new_page.children.add_new(SubheaderBlock, title="Transcript")
    new_page.children.add_new(DividerBlock)
    for each, is_bm in transcript:
        text = ''
        for i in each:
            text += i
        if is_bm == 0:
            text_block = new_page.children.add_new(TextBlock, title=text)
        else:
            callout_block = new_page.children.add_new(CalloutBlock, title=text, icon=bookmark_emoji)
            callout_block.set("format.block_color", random_color()+"_background")
    if len(frames) > 0:
        new_page.children.add_new(TextBlock, title='')
        new_page.children.add_new(TextBlock, title='')
        new_page.children.add_new(TextBlock, title='')
        new_page.children.add_new(SubheaderBlock, title='Video Bookmarks')
        new_page.children.add_new(DividerBlock)
        for each in frames:
            img = new_page.children.add_new(ImageBlock, width=500)
            img.upload_file(each)
            # print(img.source)
            # print(img.file_id)
    return new_page.get_browseable_url()

async def add_subpage_to_notion(subname):
    token_v2 = get_user_token()
    homepage_url = get_home_page_url()
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    newsub = homepage.children.add_new(PageBlock, title=subname)
    return newsub.get_browseable_url()

async def add_unitpage_to_notion(unitname, subname):
    token_v2 = get_user_token()
    homepage_url = get_home_page_url()
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    sub_page = get_doc(homepage, subname)
    newunit = sub_page.children.add_new(PageBlock, title=unitname)
    return newunit.get_browseable_url()

# if __name__ == "__main__":
#     res = verify_homepage_url('e7efb6c4a8ccd0d1e3c2720985ea3422f71d16c9b62da79a2e4ad12d46c3f73c5799b54493f05f92deff9ef5cb82f11e7977e21c9b53634817c04a9d0ae0523286e65d2392d4e70b23e16fcf7d48', 'https://www.notion.so/EasyNotes-439bbafab39d4ad797ccb60292a1be4c')
#     print(res)
#     transcript = ["kflfn kfjkjfk ddkjfjdnfknvkdjf dkfjvndkfnjvkdjf djfv kdjfvkdjnfvkjdnfkvj kdjdfnvkdjfnvkdf vkdjfvdkjfvndkj fjv",
#                 "dksjkf fjkhgkdjhfg jdhfg djfhgk djfhgk jdhfkgjhdkfjhg dkjfhgkjh kdjfhgjdfhgkjdhf jhfkgjhdfjghkdjfhg djfghk jdfhgkdfjh",
#                 "osidfjosidfi sodifiguhf jfghdkjfhgkdjhf dkjfhgkjhktjehrkj jhksjdhkkjshd fsjdhfkjhfk skdjfh jhjhgkj fkjghkdjfhgkdjf"]
    
#     write_transcript("Lesson 4", transcript=transcript, sub_name="Happiness")
