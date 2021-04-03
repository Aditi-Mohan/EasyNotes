from kivymd.uix.screen import MDScreen
import dbconn as db
import global_vars as gv
from models.user import User
from kivymd.utils import asynckivy
import asyncio

from libs.baseclass.root_screen import RallyRootScreen

class RallyRegisterScreen(MDScreen):

    def on_pre_enter(self, *args):
        if gv.new_usernm != '':
            self.ids.nm.text = gv.new_usernm
            gv.new_usernm = ''
        if gv.pass_changed:
            self.ids.pw.text = ''
            gv.pass_changed = False

    def login(self,name, passw):
        q = 'select * from user where name=%s and password=%s'
        db.mycursor.execute(q, (name, passw))
        a = db.mycursor.fetchall()
        print(len(a))
        if len(a) == 1:
            user = User(*a[0])
            async def set_globals():
                gv.user = user
                temp = await gv.get_subs(user.uid)
            asynckivy.start(set_globals())
            print(user.uid)
            print(user.name)
            print(user.password)
            self.parent.switch_to(RallyRootScreen())
        return