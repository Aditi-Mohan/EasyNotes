from kivymd.uix.screen import MDScreen
# import dbconn as db
import global_vars as gv
from models.user import User, create_new_user
from kivymd.utils import asynckivy
import asyncio
import re

class SignUpScreen(MDScreen):

    def validate(self):
        nm = self.ids.nm.text
        em = self.ids.em.text
        pw = self.ids.pw.text
        cpw = self.ids.cpw.text

        if nm != '' and em != '' and pw != '' and cpw != '':
            valid = False
            async def nm_valid():
                nonlocal valid
                valid = await gv.check_username(nm)
            asynckivy.start(nm_valid())
            if valid:
                regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                if re.search(regex, em):
                    if pw == cpw:
                        nu = create_new_user()
                        nu.name = nm
                        nu.email = em
                        nu.password = pw
                        gv.newuser = nu
                        return True
                    else:
                        print('Passwords do not match')
                else:
                    print('Email not valid')
            else:
                print('Username Already taken')
        else:
            print('Please enter data for all feilds')
