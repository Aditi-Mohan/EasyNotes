from kivymd.uix.screen import MDScreen
# import dbconn as db
import global_vars as gv
from models.user import User
from kivymd.utils import asynckivy
from functions.write_transcript_to_notion import validate_token_and_url
import asyncio
from datetime import datetime

from libs.baseclass.root_screen import RallyRootScreen

class SignUp3Screen(MDScreen):

    def validate(self):
        tk = self.ids.tk.text
        hu = self.ids.hu.text
        valid = False
        async def vtu():
            nonlocal valid
            valid = await validate_token_and_url(tk, hu)
        asynckivy.start(vtu())
        if valid:
            gv.newuser.token = tk
            gv.newuser.homepage_url = hu
            gv.newuser.last_login = datetime.now()
            # create user
            asynckivy.start(gv.create_user())
            # go to homescreen
            self.parent.switch_to(RallyRootScreen())
