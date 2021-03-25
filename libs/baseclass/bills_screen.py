from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen
from kivy.uix.splitter import Splitter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivymd.utils import asynckivy
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, TwoLineIconListItem, IconLeftWidget, IconRightWidget

import global_vars as gv
from datetime import datetime


class RallyBillsScreen(MDScreen):
    friends = []
    pending = []
    recommended = []

    def on_pre_enter(self, *args):
        # clear list every time
        pl = self.ids.pending
        fl = self.ids.friends
        pl.clear_widgets()
        fl.clear_widgets()
        asynckivy.start(gv.get_pending_friend_requests())
        self.pending = gv.pending
        pl.add_widget(OneLineListItem(text='Pending Requests'))
        for i in self.pending:
            item = TwoLineIconListItem(
                text=i.name,
                secondary_text='Sent On: '+i.sent_on.strftime(r"%m/%d/%Y, %H:%M:%S"),
                on_release=self.address_request,
            )
            icon = IconLeftWidget(
                icon='account-plus',
            )
            item.add_widget(icon)
            pl.add_widget(item)
        asynckivy.start(gv.get_friends())
        self.friends = gv.friends
        for i in self.friends:
            item = TwoLineIconListItem(
                text=i.name,
                secondary_text='Last Interaction: '+i.last_interaction.strftime(r"%m/%d/%Y, %H:%M:%S"),
                on_release=self.show_friend_details,
            )
            icon = IconLeftWidget(
                icon='account',
            )
            item.add_widget(icon)
            fl.add_widget(item)
        self.ids.search_bar.bind(text=self.search)
    
    def address_request(self, tile):
        ind = self.ids.pending.children.index(tile)
        req = self.pending[len(self.pending) - 1 - ind]
        print(req.name)
        sent_on = req.sent_on.strftime(r"%m/%d/%Y, %H:%M:%S")
        semester = str(req.semester)
        
        async def accept_callback(req_from):
            dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            await gv.accept_friend_request(req_from, dt)
            self._popup.dismiss()
            self.on_pre_enter()

        async def reject_callback(req_from):
            dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            await gv.reject_friend_request(req_from, dt)
            self._popup.dismiss()
            self.on_pre_enter()

        content = AddressRequest(accept_callback=accept_callback, reject_callback=reject_callback, req=req, semester=semester, sent_on=sent_on)
        self._popup = Popup(title='Request From '+tile.text, content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def show_friend_details(self, tile):
        # ind = self.ids.friends.children.index(tile)
        friend = [x for x in self.friends if x.name == tile.text][0]

        def rem_fr():

            async def callback(proceed):
                if proceed:
                    dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
                    await gv.remove_friend(friend.friend_id, dt)
                self._popup.content._popup.dismiss()
                self._popup.dismiss()
                self.on_pre_enter()

            content = Conformation(name=friend.name, callback=callback)
            self._popup.content._popup = Popup(content=content, size_hint=(0.5, 0.5))
            self._popup.content._popup.open()

        content = FriendDetails(
            friend=friend, last_interaction=friend.last_interaction.strftime(r"%m/%d/%Y, %H:%M:%S"),
            semester=str(friend.semester), added_on=friend.added_on.strftime(r"%m/%d/%Y, %H:%M:%S"),
            notes_sent=str(friend.notes_sent), notes_received=str(friend.notes_received), rem_fr=rem_fr)
        self._popup = Popup(title='Details', content=content, size_hint=(0.9, 0.9))
        self._popup.open()


    def search(self, instance, value):
        fl = self.ids.friends
        if value == '':
            if len(fl.children) < len(self.friends):
                fl.clear_widgets()
                for i in self.friends:
                    item = TwoLineIconListItem(
                        text=i.name,
                        secondary_text='Last Interaction: '+i.last_interaction.strftime(r"%m/%d/%Y, %H:%M:%S"),
                        on_release=self.show_friend_details,
                    )
                    icon = IconLeftWidget(
                        icon='account'
                    )
                    item.add_widget(icon)
                    fl.add_widget(item)
        else:
            fl.clear_widgets()
            for i in self.friends:
                if value in i.name:
                    item = TwoLineIconListItem(
                        text=i.name,
                        secondary_text='Last Interaction: '+i.last_interaction.strftime(r"%m/%d/%Y, %H:%M:%S"),
                        on_release=self.show_friend_details,
                    )
                    icon = IconLeftWidget(
                        icon='account'
                    )
                    item.add_widget(icon)
                    fl.add_widget(item)

    def send_request(self):
        async def send_request_callback(req_to, comments):
            print(req_to)
            print(comments)
            await gv.send_friend_request(req_to, comments, datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"))
            self._popup.dismiss()
        content = RequestPopup(callback=send_request_callback)
        self._popup = Popup(title='Send Request', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

class RequestPopup(FloatLayout):
    callback = ObjectProperty()

    def evaluate(self):
        req_to = self.ids.uid.text
        if req_to.isdecimal():
            valid = False
            async def check_uid():
                nonlocal valid
                valid = await gv.is_uid_valid(int(req_to))
            asynckivy.start(check_uid())
            if valid:
                print(valid)
                comments = self.ids.comments.text
                asynckivy.start(self.callback(int(req_to), comments))

class AddressRequest(FloatLayout):
    accept_callback = ObjectProperty()
    reject_callback = ObjectProperty()
    req = ObjectProperty()
    sent_on = StringProperty()
    semester = StringProperty()

    def address_request(self, status):
        if status == 'accepted':
            asynckivy.start(self.accept_callback(self.req.req_from))
        else:
            asynckivy.start(self.reject_callback(self.req.req_from))

class FriendDetails(FloatLayout):
    friend = ObjectProperty()
    last_interaction = StringProperty()
    semester = StringProperty()
    added_on = StringProperty()
    notes_sent = StringProperty()
    notes_received = StringProperty()
    rem_fr = ObjectProperty()

class Conformation(FloatLayout):
    name = StringProperty()
    callback = ObjectProperty()

    def callback_callback(self, option):
        proceed = False
        if option == 'yes':
            proceed = True
        print(proceed)
        asynckivy.start(self.callback(proceed))