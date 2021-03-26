from kivy.properties import ListProperty, StringProperty, ObjectProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivymd.utils import asynckivy

from kivymd.uix.list import MDList, OneLineListItem, ThreeLineIconListItem, IconLeftWidget,  TwoLineIconListItem
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from functions.write_transcript_to_notion import copy_page
import global_vars as gv
import webbrowser
from datetime import datetime


class RallyOverviewScreen(MDScreen):
    username = StringProperty('')
    last_active = StringProperty('')
    recent_notes = []
    notifs = []
    pending_shares = []

    def on_pre_enter(self, *args):
        self.username = gv.user.name
        self.last_active = gv.user.last_login.strftime(r"%m/%d/%Y, %H:%M:%S")
        if len(gv.latest_notes) == 0:
            asynckivy.start(gv.get_latest_notes())
        asynckivy.start(gv.get_notifications())
        asynckivy.start(gv.get_pending_shares())
        self.recent_notes = gv.latest_notes
        self.notifs = gv.notifs
        self.pending_shares = gv.pending_shares
        if len(self.children) != 0:
            ntl = self.ids.notifs
            ntl.clear_widgets()
            ntl.add_widget(
                OneLineListItem(
                    text='Notifications',
                    font_style='H6',
                    # on_release=delete all notifications
                )
            )      
            lst = self.ids.list_view
            lst.clear_widgets()
            lst.add_widget(
                OneLineListItem(
                    text='Quick Access',
                    font_style='H6',
                    bg_color=[40/255, 44/255, 64/255,1],
                )
            )
            plt = self.ids.pending_shares
            plt.clear_widgets()
            plt.add_widget(
                OneLineListItem(
                    text='Pending Note Shares',
                    font_style='H6',
                    bg_color=[40/255, 44/255, 64/255,1],
                )
            )
            for i in self.recent_notes:
                sub_name = gv.get_name_for_sub(i.subject_id)
                unit_name = ''
                async def get_unitname():
                    nonlocal unit_name
                    unit_name = await gv.get_name_for_unit(i.subject_id, sub_name, i.unit_id)
                asynckivy.start(get_unitname())
                item = ThreeLineIconListItem(
                    text = i.note_title,
                    secondary_text = 'from '+unit_name+' of '+sub_name,
                    tertiary_text = 'On '+i.datetime_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S")+"    "+str(i.num_of_bookmarks)+(' bookmarks' if i.num_of_bookmarks>1 else ' bookmark'),
                    bg_color=[40/255, 44/255, 64/255,1],
                    on_release = self.open_note,
                )
                icon = IconLeftWidget(
                    icon="note",
                    theme_text_color="Custom",
                    text_color=gv.get_color_for_sub(i.subject_id),
                )
                item.add_widget(icon)
                lst.add_widget(item)
            for i in self.notifs:
                item = TwoLineIconListItem(
                    text=i.notif_title,
                    secondary_text=i.dt.strftime(r"%m/%d/%Y, %H:%M:%S"),
                    on_release=self.open_notif,
                )
                icon = IconLeftWidget(
                    icon='message'
                )
                item.add_widget(icon)
                ntl.add_widget(item)
            for i in self.pending_shares:
                item = TwoLineIconListItem(
                    text=i.note_title,
                    secondary_text='From: '+i.friend_name,
                    on_release=self.address_pending_shares,
                )
                icon = IconLeftWidget(
                    icon='note-plus'
                )
                item.add_widget(icon)
                plt.add_widget(item)
    
    def scan_for_friend_recom(self):
        return 
    
    def address_pending_shares(self, tile):
        ind = self.ids.pending_shares.children.index(tile)
        share_req = self.pending_shares[len(self.pending_shares) - 1 - ind]
        print(share_req.note_title)
        dt = share_req.sent_on.strftime(r"%m/%d/%Y, %H:%M:%S")

        async def accept_sr():
            token_v2, homepage_url = await gv.get_friend_token_url(share_req.req_from)
            # print(token_v2)
            # print(homepage_url)
            # write_to notion and get link
            await gv.get_list_of_subs_and_units()
            self._popup.dismiss()

            async def finish(sub_name, unit_name, title):
                sub_id = [x for x in gv.subjects if x.subject_name == sub_name][0].subject_id
                unit_id = [x for x in gv.units[sub_name] if x.unit_name == unit_name][0].unit_id
                nbm = await gv.get_nbm(share_req.note_id)
                dt = datetime.now()
                newlink = await copy_page(gv.user.token, gv.user.homepage_url, sub_name, unit_name, title, token_v2, homepage_url, share_req.sub_name, share_req.unit_name, share_req.note_title, dt.strftime(r"%m/%d/%Y, %H:%M:%S"))
                print(newlink)
                await gv.accept_share_request(sub_id, gv.user.uid, unit_id, title, dt.strftime(r"%Y-%m-%d %H:%M:%S"), newlink, nbm, share_req.note_id, share_req.sent_on, share_req.req_from, share_req.note_title)
                self._popup.dismiss()
                self.on_pre_enter()

            content = SelectSubAndUnit(subs=[x.subject_name for x in gv.subjects], finish=finish, og_name=share_req.note_title)
            self._popup = Popup(title='Select Subject and Unit', content=content, size_hint=(0.6, 0.4))
            self._popup.open()

        async def reject_sr():
            dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            await gv.reject_share_req(share_req.req_from, share_req.sent_on, share_req.note_id, share_req.note_title, dt)
            self._popup.dismiss()
            self.on_pre_enter()

        content = ShareRequestInfo(share_req=share_req, sent_on=dt, accept_callback=accept_sr, reject_callback=reject_sr)
        self._popup = Popup(title='Share Request', content=content, size_hint=(0.5, 0.5))
        self._popup.open()
        return
    
    def open_note(self, notetile):
        ind = self.ids.list_view.children.index(notetile)
        note = self.recent_notes[len(self.recent_notes)-1-ind]
        print(self.recent_notes[len(self.recent_notes)-1-ind].note_title)
        link = ''
        async def get_link():
            nonlocal link
            link = await gv.get_link_for_latest(note.subject_id, note.unit_id, note.note_id)
        asynckivy.start(get_link())
        webbrowser.open(link)
        # first_space = str(notetile.secondary_text).index(' ')
        # last_space = str(notetile.secondary_text).rindex(' ')
        # unit_name = notetile.secondary_text[first_space:second_space]
        # sub_name = notetile.secondary_text[second_space:third_space]
        # note_title = notetile.text
        # print(sub_name, 'dfs', unit_name, 'fdsdf', note_title)
        # link = ''
        # async def get_link():
        #     await gv.get_quick_links_from_names(sub_name, unit_name, note_title)
        # asynckivy.start(get_link())
        # query - select s.sub_name, u.unit_name, n.note_title, n.link from notes n inner join units u on n.unit_id=u.unit_id inner join subject s on s.sub_id=u.sub_id;
        # add - where s.uid = 1 or n.uid = 1;
        # either store this as a view - quick_links_and_names - and query the view
        # or add where clause at the end of the query
    
    def open_notif(self, tile):

        async def delete_notif():
            dt = datetime.strptime(tile.secondary_text, r"%m/%d/%Y, %H:%M:%S")
            await gv.delete_notif(dt.strftime(r"%Y-%m-%d %H:%M:%S"))
            self.on_pre_enter()
            self._popup.dismiss()
            
        content = NotificationPopup(content=tile, delete_notif_callback=delete_notif)
        self._popup = Popup(title='Notification', content=content, size_hint=(0.6, 0.6))
        self._popup.open()

class NotificationPopup(FloatLayout):
    content = ObjectProperty()
    delete_notif_callback = ObjectProperty()

    def delete_notif(self):
        asynckivy.start(self.delete_notif_callback())

class ShareRequestInfo(FloatLayout):
    share_req = ObjectProperty()
    sent_on = StringProperty()
    accept_callback = ObjectProperty()
    reject_callback = ObjectProperty()

    def choice(self, option):
        if option == 'accept':
            asynckivy.start(self.accept_callback())
        else:
            asynckivy.start(self.reject_callback())

class SelectSubAndUnit(FloatLayout):
    subs = ListProperty()
    finish = ObjectProperty()
    og_name = StringProperty()
    units = []
    selected_sub = None
    selected_unit = None
    new_name = ''

    def set_sub(self, sub):
        self.selected_sub = sub
        self.ids.units.values = [x.unit_name for x in gv.units[sub]]
        self.ids.units.text = 'Select Unit'
    
    def set_unit(self, unit):
        self.selected_unit = unit
    
    def choice(self):
        if self.selected_sub is not None and self.selected_unit is not None:
            al_exists = True
            self.new_name = self.ids.file_name.text
            print(self.new_name)
            if self.new_name != '':

                async def check_if_already_exists():
                    nonlocal al_exists
                    if self.selected_sub in gv.notes.keys():
                        if self.selected_unit in gv.notes[self.selected_sub].keys():
                            if self.new_name not in [x.note_title for x in gv.notes[self.selected_sub][self.selected_unit]]:
                                al_exists = False
                                return
                            else:
                                print('Note with the same name Already Exists in this Unit')
                                return
                    sub_id = [x for x in gv.subjects if x.subject_name == self.selected_sub][0].subject_id
                    unit_id = [x for x in gv.units[self.selected_sub] if x.unit_name == self.selected_unit][0].unit_id
                    await gv.get_notes_for(gv.user.uid, sub_id, unit_id, self.selected_unit, self.selected_sub)
                    if self.new_name not in [x.note_title for x in gv.notes[self.selected_sub][self.selected_unit]]:
                        al_exists = False    
                    else:
                        print('Note with the same name Already Exists in this Unit')
            else:
                print('Enter file name')

            asynckivy.start(check_if_already_exists())
            if not al_exists:
                asynckivy.start(self.finish(self.selected_sub, self.selected_unit, self.new_name))


class OverviewBox(MDBoxLayout):
    pass
