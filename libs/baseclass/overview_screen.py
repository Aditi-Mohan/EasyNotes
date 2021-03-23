from kivy.properties import ListProperty, StringProperty, ObjectProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivymd.utils import asynckivy

from kivymd.uix.list import MDList, OneLineListItem, ThreeLineIconListItem, IconLeftWidget

import global_vars as gv
import webbrowser


class RallyOverviewScreen(MDScreen):
    username = StringProperty('')
    recent_notes = []

    def on_pre_enter(self, *args):
        print('dfs')
        self.username = gv.user.name
        if len(gv.latest_notes) == 0:
            asynckivy.start(gv.get_latest_notes())
        self.recent_notes = gv.latest_notes
        if len(self.children) != 0:
            lst = self.ids.list_view
            lst.clear_widgets()
            lst.add_widget(
                OneLineListItem(
                    text='Recent Notes',
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
                    on_release = lambda x: self.open_note(i.link),
                )
                icon = IconLeftWidget(
                    icon="note",
                    theme_text_color="Custom",
                    text_color=gv.get_color_for_sub(i.subject_id),
                )
                item.add_widget(icon)
                lst.add_widget(item)
    
    def scan_for_pending_requests(self):
        return
    
    def scan_for_pending_shares(self):
        return
    
    def open_note(self, notetile):
        first_space = str(notetile.text).index(' ')
        second_space = str(notetile.text).index(' ', first_space+1)
        third_space = str(notetile.text).index(' ', second_space+1)
        # query - select s.sub_name, u.unit_name, n.note_title, n.link from notes n inner join units u on n.unit_id=u.unit_id inner join subject s on s.sub_id=u.sub_id;
        # add - where s.uid = 1 or n.uid = 1;
        # either store this as a view - quick_links_and_names - and query the view
        # or add where clause at the end of the query
        webbrowser.open(link)

class OverviewBox(MDBoxLayout):
    pass
