from kivymd.uix.screen import MDScreen
import dbconn as db
import global_vars as gv
from models.user import User
from kivymd.utils import asynckivy
import asyncio

class RallyRegisterScreen(MDScreen):

    def login(self,name, passw):
        q = 'select * from user where name=%s and password=%s'
        db.mycursor.execute(q, (name, passw))
        a = db.mycursor.fetchall()
        if len(a) == 1:
            user = User(*a[0])
        async def set_globals():
            gv.user = user
            temp = await gv.get_subs(user.uid)
        asynckivy.start(set_globals())
        print(user.uid)
        print(user.name)
        print(user.password)
        self.ids.fingpr.dispatch('on_release')
        return