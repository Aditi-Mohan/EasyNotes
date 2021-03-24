from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivymd.utils import asynckivy

from utils.random_color import random_kivy_colors
from libs.baseclass.subject_screen import SubjectScreen
from libs.baseclass.add_subject_dialog import AddSubjectDialog
import global_vars as gv
import dbconn as db

class RallyAccountsScreen(MDScreen):
    # subs = [{'sub': 'DAA', 'faculty': 'Abhay Kolhe'},
    #     {'sub': 'DBMS', 'faculty': 'Vijayetha T.'},
    #     {'sub': 'DLD', 'faculty': 'Anjana Rodrigues'},
    #     {'sub': 'EM-4', 'faculty': 'Minirani S.'},
    #     {'sub': 'MP', 'faculty': 'Sumita Nainan'},
    #     {'sub': 'PE', 'faculty': 'Neerja Kalluri'},
    #     {'sub': 'OB', 'faculty': 'Anand Rajwat'},
    #     {'sub': 'WT', 'faculty': 'VRG'}]
    subs = []
    new_name = StringProperty()
    new_color = ColorProperty()
    
    def go_to_sub_screen(self, tile):
        # sc = self.ids.scr_manager
        sc = self.parent.parent.parent.parent
        sub = self.subs[len(self.subs) - 1 - self.ids.list_view.children.index(tile)]
        sc.switch_to(SubjectScreen(sub_id=sub.subject_id, title=tile.text, color=tile.text_color), transition=SlideTransition(), direction='up')
        # print(sc.current)

    def add_subject(self):
        content = AddSubjectDialog(add_sub=self.add_sub_callback)
        self._popup = Popup(title='Add Subject', content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def add_sub_callback(self, name, fac_name, color):
        if name not in [x.subject_name for x in gv.subjects]:
            item = TwoLineIconListItem(
                    text=name,
                    secondary_text=fac_name,
                    theme_text_color="Custom",
                    text_color= color,
                    on_release= self.go_to_sub_screen
                    )
            icon = IconLeftWidget(
                    icon='book',
                    theme_text_color="Custom",
                    text_color= color,
                    )
            item.add_widget(icon)
            self.ids.list_view.add_widget(item)
            asynckivy.start(gv.add_subject(name, gv.user.uid, fac_name, color))
            asynckivy.start(gv.get_subs(gv.user.uid))
            self.subs = gv.subjects
        else:
            print('Subject '+name+' already exists')
        self._popup.dismiss()
        

    def on_pre_enter(self, *args):
        list_view = self.ids.list_view
        list_view.clear_widgets()
        self.subs = gv.subjects
        for i in self.subs:
            # color = random_kivy_colors()
            item = TwoLineIconListItem(
                    text=i.subject_name,
                    secondary_text=i.faculty_name,
                    theme_text_color="Custom",
                    text_color= i.color,
                    on_release= self.go_to_sub_screen
                    )
            icon = IconLeftWidget(
                    icon='book',
                    theme_text_color="Custom",
                    text_color= i.color,
                    )
            item.add_widget(icon)
            list_view.add_widget(item)
            # self.sc.add_widget(SubjectScreen(name=i['sub']))
