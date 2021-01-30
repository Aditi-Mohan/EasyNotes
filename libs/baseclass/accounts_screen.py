from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.gridlayout import MDGridLayout
from utils.random_color import random_color

class RallyAccountsScreen(MDScreen):
    subs = [{'sub': 'DAA', 'faculty': 'Abhay Kolhe'},
        {'sub': 'DBMS', 'faculty': 'Vijayetha T.'},
        {'sub': 'DLD', 'faculty': 'Anjana Rodrigues'},
        {'sub': 'EM-4', 'faculty': 'Minirani S.'},
        {'sub': 'MP', 'faculty': 'Sumita Nainan'},
        {'sub': 'PE', 'faculty': 'Neerja Kalluri'},
        {'sub': 'OB', 'faculty': 'Anand Rajwat'},
        {'sub': 'WT', 'faculty': 'VRG'}]

    def on_pre_enter(self, *args):
        list_view = self.ids.list_view
        list_view.clear_widgets()
        for i in self.subs:
            item = TwoLineIconListItem(
                    text=i['sub'],
                    secondary_text=i['faculty'],
                    theme_text_color="Custom",
                    text_color= ()
                    )
            icon = IconLeftWidget(
                    icon='minus',
                    theme_text_color="Custom",
                    text_color= 
                    # halign='center',
                    # pos_hint={'center_y':0.5},
                    )
            item.add_widget(icon)
            list_view.add_widget(item)


