from kivy.properties import ListProperty, StringProperty, ObjectProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivymd.utils import asynckivy

from kivymd.uix.list import MDList, OneLineListItem, ThreeLineIconListItem, IconLeftWidget,  TwoLineIconListItem
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import global_vars as gv
import webbrowser
from datetime import datetime


class RallyOverviewScreen(MDScreen):
    username = StringProperty('')
    last_active = StringProperty('')
    recent_notes = []
    notifs = []

    def on_pre_enter(self, *args):
        self.username = gv.user.name
        self.last_active = gv.user.last_login.strftime(r"%m/%d/%Y, %H:%M:%S")
        if len(gv.latest_notes) == 0:
            asynckivy.start(gv.get_latest_notes())
        asynckivy.start(gv.get_notifications())
        self.recent_notes = gv.latest_notes
        self.notifs = gv.notifs
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
    
    def scan_for_friend_recom(self):
        return 
    
    def scan_for_pending_shares(self):
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

class OverviewBox(MDBoxLayout):
    pass
