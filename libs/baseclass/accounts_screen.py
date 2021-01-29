from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineListItem


class RallyAccountsScreen(MDScreen):
    subs = [{'sub': 'DAA', 'faculty': 'Abhay Kolhe'},
            {'sub': 'DBMS', 'faculty': 'Vijayetha T.'},
            {'sub': 'DLD', 'faculty': 'Anjana Rodrigues'},
            {'sub': 'EM-4', 'faculty': 'Minirani S.'},
            {'sub': 'MP', 'faculty': 'Sumita Nainan'},
            {'sub': 'PE', 'faculty': 'Neerja Kalluri'},
            {'sub': 'OB', 'faculty': 'Anand Rajwat'},
            {'sub': 'WT', 'faculty': 'VRG'}]
    
    def __inti__(self):
        list_view = MDList()
        for i in RallyAccountsScreen.subs:
            list_view.add_widget(TwoLineListItem(
                text=i['sub'], secondary_text=i['faculty']
            ))
        self.add_widget(list_view)
