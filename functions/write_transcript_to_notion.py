from notion.client import NotionClient
from notion.block import *
from datetime import datetime

def get_user_token():
    # replace with fetching token for that user from database
    return "7a891b7b74950f98146c6059c3939c3dea5be5dedb08440b072aa50199bce91bb5d8577ecb9bcb0b4ac047c6daf144df7e452824e7d6b8a64c8dde7d67ea0b104855df57a4db8b94003411ec1628"

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

def write_transcript(title, transcript, sub_name):
    token_v2 = get_user_token()
    homepage_url = get_home_page_url()
    client = NotionClient(token_v2=token_v2)
    homepage = client.get_block(homepage_url)
    sub_page = get_doc(homepage, sub_name)
    new_page = sub_page.children.add_new(PageBlock, title=title)
    now = datetime.now()
    date_of_creation = now.strftime(r"%d-%m-%Y, %H:%M")
    date_block = new_page.children.add_new(TextBlock, title="Created on: "+date_of_creation)
    date_block.set("format.block_color", "blue_background")
    transcript_block = new_page.children.add_new(SubheaderBlock, title="Transcript")
    new_page.children.add_new(DividerBlock)
    for each in transcript:
        text_block = new_page.children.add_new(TextBlock, title=each)
    


if __name__ == "__main__":
    transcript = ["kflfn kfjkjfk ddkjfjdnfknvkdjf dkfjvndkfnjvkdjf djfv kdjfvkdjnfvkjdnfkvj kdjdfnvkdjfnvkdf vkdjfvdkjfvndkj fjv",
                "dksjkf fjkhgkdjhfg jdhfg djfhgk djfhgk jdhfkgjhdkfjhg dkjfhgkjh kdjfhgjdfhgkjdhf jhfkgjhdfjghkdjfhg djfghk jdfhgkdfjh",
                "osidfjosidfi sodifiguhf jfghdkjfhgkdjhf dkjfhgkjhktjehrkj jhksjdhkkjshd fsjdhfkjhfk skdjfh jhjhgkj fkjghkdjfhgkdjf"]
    
    write_transcript("Lesson 4", transcript=transcript, sub_name="Happiness")
