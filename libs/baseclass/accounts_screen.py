from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from utils.random_color import random_kivy_colors
from libs.baseclass.subject_screen import SubjectScreen
from libs.baseclass.root_screen import RallyRootScreen

class RallyAccountsScreen(MDScreen):
    subs = [{'sub': 'DAA', 'faculty': 'Abhay Kolhe'},
        {'sub': 'DBMS', 'faculty': 'Vijayetha T.'},
        {'sub': 'DLD', 'faculty': 'Anjana Rodrigues'},
        {'sub': 'EM-4', 'faculty': 'Minirani S.'},
        {'sub': 'MP', 'faculty': 'Sumita Nainan'},
        {'sub': 'PE', 'faculty': 'Neerja Kalluri'},
        {'sub': 'OB', 'faculty': 'Anand Rajwat'},
        {'sub': 'WT', 'faculty': 'VRG'}]
    
    def go_to_sub_screen(self, tile):
        # sc = self.ids.scr_manager
        print(tile.text)
        sc = self.parent.parent.parent.parent
        sc.switch_to(SubjectScreen(name=tile.text), transition=SlideTransition(), direction='up')
        # print(sc.current)


    def on_pre_enter(self, *args):
        list_view = self.ids.list_view
        list_view.clear_widgets()
        for i in self.subs:
            color = random_kivy_colors()
            item = TwoLineIconListItem(
                    text=i['sub'],
                    secondary_text=i['faculty'],
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
            list_view.add_widget(item)
            # self.sc.add_widget(SubjectScreen(name=i['sub']))
