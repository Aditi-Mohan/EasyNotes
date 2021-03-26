from kivymd.uix.screen import MDScreen
# import dbconn as db
import global_vars as gv
from models.user import User
from kivymd.utils import asynckivy
import asyncio

# from libs.baseclass.root_screen import RallyRootScreen

class SignUp2Screen(MDScreen):

    def validate(self):
        clg = self.ids.clg.text
        crs = self.ids.crs.text
        sm = self.ids.sm.text
        if clg != '' and crs != '' and sm != '':
            if sm.isdecimal():
                gv.newuser.college = clg
                gv.newuser.course = crs
                gv.newuser.semester = int(sm)
                return True
            else:
                print('Semster must be a number')
        else:
            print('Please enter data for all feilds')
