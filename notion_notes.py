from notion.client import NotionClient
from notion.block import *

token_v2 = "7a891b7b74950f98146c6059c3939c3dea5be5dedb08440b072aa50199bce91bb5d8577ecb9bcb0b4ac047c6daf144df7e452824e7d6b8a64c8dde7d67ea0b104855df57a4db8b94003411ec1628"
parent_page_url_or_id = "https://www.notion.so/EasyNotes-439bbafab39d4ad797ccb60292a1be4c"
client = NotionClient(token_v2=token_v2)
parent_page = client.get_block(parent_page_url_or_id)
# print(parent_page)
# for child in parent_page.children:
#     print(child)
# newb = parent_page.children.add_new(TextBlock, title="hello")
# newb2 = parent_page.children.add_new(TextBlock, title="world")
# newb2.move_to(newb)
# newb3 = parent_page.children.add_new(TextBlock, title="middle")
# newb3.move_to(newb, "first-child")
# newb = parent_page.children.add_new(TextBlock)
# newb.set("properties.title", [['Only '], ['this part', [['h', 'red']]], [' is colored']])
print("done!")
