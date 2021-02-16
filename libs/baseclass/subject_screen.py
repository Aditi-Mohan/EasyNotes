from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, ColorProperty, ObjectProperty
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from libs.baseclass.root_screen import RallyRootScreen
from libs.baseclass.file_chooser import ChooseFile
import utils.file_extensions as fe

import os
from datetime import datetime

class SubjectScreen(MDScreen):
    title = StringProperty()
    color = ColorProperty()
    btn_color = ColorProperty()

    notes = [{'title': 'LESSON 1', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 2', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 3', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 4', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
            {'title': 'LESSON 5', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},]
    
    def on_pre_enter(self, *args):
        self.btn_color = (self.color[0], self.color[1], self.color[2], 0.4)
        list_view = self.ids.list_view
        for i in self.notes:
            item = TwoLineIconListItem(
                text= i['title'],
                secondary_text= i['time'],
            )
            icon = IconLeftWidget(
                icon="note",
                theme_text_color="Custom",
                text_color=(self.color[0], self.color[1], self.color[2], 0.75),
            )
            item.add_widget(icon)
            list_view.add_widget(item)
    
    def back(self):
        sc = self.parent
        sc.switch_to(RallyRootScreen(), transition=SlideTransition(), direction='right')

    def upload(self, file_type):
        content = ChooseFile(select=self.select_file, cancel=self.dismiss_popup, file_filter=fe.file_extensions[file_type])
        self._popup = Popup(title="Choose File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        return
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def select_file(self, path, selection):
        print('selected file: ')
        print(path)
        print(selection)

        self._popup.dismiss()

        # text=''
        # for i in selection:
        #     text+=i+'\n'
        # content = Label(text=text)

        # self._popup = Popup(title='Chosen File', content=content, size_hint=(0.9, 0.9))
        # self._popup.open()