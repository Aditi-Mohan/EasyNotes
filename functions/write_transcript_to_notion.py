from notion.client import NotionClient
from notion.block import *
from datetime import datetime

def get_user_token():
    # replace with fetching token for that user from database
    return "e7efb6c4a8ccd0d1e3c2720985ea3422f71d16c9b62da79a2e4ad12d46c3f73c5799b54493f05f92deff9ef5cb82f11e7977e21c9b53634817c04a9d0ae0523286e65d2392d4e70b23e16fcf7d48"

def get_home_page_url():
    # replace with fetching homepage url for that user from database
    return "https://www.notion.so/EasyNotes-439bbafab39d4ad797ccb60292a1be4c"

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
    now = datetime.now()
    date_block = new_page.children.add_new(TextBlock, title="Created on: "+dt_of_creation)
    date_block.set("format.block_color", "blue_background")
    transcript_block = new_page.children.add_new(SubheaderBlock, title="Transcript")
    new_page.children.add_new(DividerBlock)
    for each in transcript:
        text_block = new_page.children.add_new(TextBlock, title=each)
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
#     transcript = ["kflfn kfjkjfk ddkjfjdnfknvkdjf dkfjvndkfnjvkdjf djfv kdjfvkdjnfvkjdnfkvj kdjdfnvkdjfnvkdf vkdjfvdkjfvndkj fjv",
#                 "dksjkf fjkhgkdjhfg jdhfg djfhgk djfhgk jdhfkgjhdkfjhg dkjfhgkjh kdjfhgjdfhgkjdhf jhfkgjhdfjghkdjfhg djfghk jdfhgkdfjh",
#                 "osidfjosidfi sodifiguhf jfghdkjfhgkdjhf dkjfhgkjhktjehrkj jhksjdhkkjshd fsjdhfkjhfk skdjfh jhjhgkj fkjghkdjfhgkdjf"]
    
#     write_transcript("Lesson 4", transcript=transcript, sub_name="Happiness")
