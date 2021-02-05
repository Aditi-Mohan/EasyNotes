from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget

from datetime import datetime

class SubjectScreen(MDScreen):
    title = StringProperty()

    notes = [{'title': 'LESSON 1', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 2', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 3', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 4', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 5', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},]
    
    def on_pre_enter(self, *args):
        self.title = self.name
        list_view = self.ids.list_view
        for i in self.notes:
            item = TwoLineIconListItem(
                text= i['title'],
                secondary_text= i['time']
            )
            icon = IconLeftWidget(
                icon="note-outline",
                size=(10, 40)
            )
            item.add_widget(icon)
            list_view.add_widget(item)
