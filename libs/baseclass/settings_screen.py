from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.utils import asynckivy
import global_vars as gv

from datetime import datetime

class RallySettingsScreen(MDScreen):
    # list_created = BooleanProperty(False)

    # def on_pre_enter(self):
        # if not self.list_created:
        #     items = [
        #         # "Tax documents",
        #         "Change Username",
        #         "Change Password",
        #         "Change Email Address",
        #         # "Notifications",
        #         # "Personal Information",
        #         # "Paperless settings",
        #         # "Find ATMs",
        #         # "Help",
        #         "Sign out",
        #     ]
        #     for i in items:
        #         list_item = OneLineListItem(
        #             text=i, divider="Inset", font_style="H6"
        #         )
        #         list_item.bind(on_release=self.goto_register_screen)
        #         self.ids._list.add_widget(list_item)
        #     self.list_created = True
    def see_uid(self):
        def close():
            self._popup.dismiss()

        content = UIDPopup(uid=str(gv.user.uid), close=close)
        self._popup = Popup(title='UID', content=content, size_hint=(0.3, 0.3))
        self._popup.open()

    def change_username(self):
        async def change_usernm_callback(new_usernm):
            await gv.change_username(new_usernm)
            self._popup.dismiss()
            def so():
                self._popup.dismiss()
                gv.new_usernm = new_usernm
                self.signout()
            content = RefreshPopup(signout=so)
            self._popup = Popup(title='Done', content=content, size_hint=(0.5, 0.5))
            self._popup.open()

        content = ChangeUsernamePopup(cusn_callback=change_usernm_callback)
        self._popup = Popup(title='Change Username', content=content, size_hint=(0.5, 0.5))
        self._popup.open()

    def goto_register_screen(self):
        self.parent.parent.parent.parent.current = "rally register screen"
        self.parent.parent.parent.ids.nav_bar.set_current(-1)
    
    def signout(self):
        async def signout_callback():
            await gv.put_last_active(datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))
            print('cleaning up...')
            await gv.clean_up()
            gv.signout()
        asynckivy.start(signout_callback())
        self.goto_register_screen()
    
    def change_password(self):
        
        async def set_new_pass(new_pass):
            print(new_pass)
            await gv.set_password(new_pass)
            self._popup.dismiss()
            def so():
                self._popup.dismiss()
                self.signout()
            content = RefreshPopup(signout=so)
            self._popup = Popup(title='Done', content=content, size_hint=(0.5, 0.5))
            self._popup.open()

        def check_curr_password(passw):
            if passw == gv.user.password:
                self._popup.dismiss()

                content = NewPasswordPopup(set_pass=set_new_pass)
                self._popup = Popup(title='Set New Password', content=content, size_hint=(0.5, 0.6))
                self._popup.open()
            else:
                print('Password Incorrect')
        
        content = ConfPassword(conf=check_curr_password)
        self._popup = Popup(title='Confirm Current Password', content=content, size_hint=(0.5, 0.5))
        self._popup.open()
    
    def delete_acc(self):
        async def del_acc():
            await gv.delete_account()
            print('cleaning up...')
            await gv.clean_up()
        asynckivy.start(del_acc())
        self.goto_register_screen()

class ChangeUsernamePopup(FloatLayout):
    cusn_callback = ObjectProperty()

    def cusn(self):
        if self.ids.nnm.text != '':
            valid = False
            async def validate():
                nonlocal valid
                valid = await gv.check_username(self.ids.nnm.text)
            asynckivy.start(validate())
            if valid:
                asynckivy.start(self.cusn_callback(self.ids.nnm.text))
            else:
                if self.ids.nnm.text == gv.user.name:
                    print('Username unchanged')
                else:
                    print('Username already exists')

class RefreshPopup(FloatLayout):
    signout = ObjectProperty()

class ConfPassword(FloatLayout):
    conf = ObjectProperty()

class NewPasswordPopup(FloatLayout):
    set_pass = ObjectProperty()

    def finish(self):
        if self.ids.pw.text == self.ids.cpw.text:
            asynckivy.start(self.set_pass(self.ids.pw.text))
        else:
            print('Passwords do not match')

class UIDPopup(FloatLayout):
    uid = StringProperty()
    close = ObjectProperty()