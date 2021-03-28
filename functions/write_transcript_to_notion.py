from notion.client import NotionClient
from notion.block import *
from datetime import datetime
from utils.random_emoji import bookmark_emoji
from utils.random_color import random_color
from copy import copy

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
        text = ''
        for i in each:
            text += i
        if is_bm == 0:
            text_block = new_page.children.add_new(TextBlock, title=text)
        else:
            callout_block = new_page.children.add_new(CalloutBlock, title=text, icon=bookmark_emoji)
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

async def add_subpage_to_notion(token_v2, homepage_url, subname):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    newsub = homepage.children.add_new(PageBlock, title=subname)
    return newsub.get_browseable_url()

async def add_unitpage_to_notion(token_v2, homepage_url, unitname, subname):
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

async def copy_page(token_v2, homepage_url, sub_name, unit_name, title, f_token_v2, f_homepage_url, f_sub_name, f_unit_name, f_title, dt):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    sub_page = get_doc(homepage, sub_name)
    unit_page = get_doc(sub_page, unit_name)
    f_client = NotionClient(token_v2=f_token_v2)
    f_homepage = f_client.get_block(f_homepage_url)
    f_sub_page = get_doc(f_homepage, f_sub_name)
    f_unit_page = get_doc(f_sub_page, f_unit_name)
    f_note_page = get_doc(f_unit_page, f_title)
    new_page = unit_page.children.add_new(PageBlock)
    _copy_properties(f_note_page, new_page)
    date_block = new_page.children.add_new(TextBlock, title="Received on: "+dt)
    date_block.set("format.block_color", "blue_background")
    new_page.title = title
    return new_page.get_browseable_url()

def _copy_properties(old, new):
    for prop in dir(old):
        try:
            if not prop.startswith('_'):
                attr = getattr(old, prop)
                # copying tags creates a whole new set of problems
                if prop != 'tags' and attr != '' and not callable(attr):
                    setattr(new, prop, copy(attr))

        # notion-py raises AttributeError when it can't assign an attribute
        except AttributeError:
            pass

    if bool(old.children):
        for old_child in old.children:
            new_child = new.children.add_new(old_child.__class__)
            _copy_properties(old_child, new_child)

async def validate_token_and_url(token_v2, url):
    try:
        client = NotionClient(token_v2=token_v2)
        block = client.get_block(url)
        return True
    except:
        print('Token or Url not valid')
        return False

async def validate_page(token_v2, link):
    client = NotionClient(token_v2=token_v2)
    try:
        page = client.get_block(link)
        return True
    except:
        print('Link not Valid, Make sure the Page is not a Subpage and is directly accessible')
        return False

async def create_page_from_link(link, token_v2, homepage_url, sub_name, unit_name, title, dt):
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    sub_page = get_doc(homepage, sub_name)
    unit_page = get_doc(sub_page, unit_name)
    new_page = unit_page.children.add_new(PageBlock)
    old_page = client.get_block(link)
    _copy_properties(old_page, new_page)
    new_page.title = title
    return new_page.get_browseable_url()