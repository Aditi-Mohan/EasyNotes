from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, ColorProperty, ObjectProperty, NumericProperty
from kivymd.uix.list import OneLineIconListItem, TwoLineIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivymd.utils import asynckivy

from libs.baseclass.root_screen import RallyRootScreen
from libs.baseclass.add_unit_dialog import AddUnitDialog
from libs.baseclass.file_chooser import ChooseFile
from libs.baseclass.save_file_dialog import SaveFile
from functions.ibmspeechtotext import generate_transcript
from functions.write_transcript_to_notion import write_transcript
from functions.audio_from_video import audio_from_video
import utils.file_extensions as fe
import global_vars as gv

import os
import asyncio
from datetime import datetime

class SubjectScreen(MDScreen):
    title = StringProperty()
    color = ColorProperty()
    btn_color = ColorProperty()
    sub_id = NumericProperty()
    # notes = [{'title': 'LESSON 1', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 2', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 3', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 4', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 5', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},]
    units = []
    new_transcript = []
    file_type = ''
    new_unit = None
    
    def on_pre_enter(self, *args):
        self.btn_color = (self.color[0], self.color[1], self.color[2], 0.4)
        list_view = self.ids.list_view
        if self.title in gv.units.keys():
            self.units = gv.units[self.title]
        else:
            print('loading...')
            asynckivy.start(gv.get_units_for(gv.user.uid, self.sub_id, self.title))
            self.units = gv.units[self.title]
        for i in self.units:
            item = OneLineIconListItem(
                text= i.unit_name,
                on_release=self.show_notes,
            )
            icon = IconLeftWidget(
                icon="note",
                theme_text_color="Custom",
                text_color=(self.color[0], self.color[1], self.color[2], 0.75),
            )
            item.add_widget(icon)
            list_view.add_widget(item)
        item = OneLineIconListItem(
            text= 'Add Unit',
            on_release=self.add_unit
        )
        icon = IconLeftWidget(
            icon="plus",
            theme_text_color="Custom",
            text_color=(self.color[0], self.color[1], self.color[2], 0.75),
        )
        item.add_widget(icon)
        list_view.add_widget(item)
    
    def back(self):
        sc = self.parent
        sc.switch_to(RallyRootScreen(back_press='SUBJECTS'), transition=SlideTransition(), direction='right')

    def add_unit(self, listitem):
        def add_unit_callback(name):
            self.new_unit = name
            asynckivy.start(gv.add_unit(self.new_unit, self.title, self.sub_id, gv.user.uid))
            asynckivy.start(gv.get_units_for(gv.user.uid, self.sub_id, self.title))
            item = OneLineIconListItem(
                text= name,
                on_release=self.show_notes,
            )
            icon = IconLeftWidget(
                icon="note",
                theme_text_color="Custom",
                text_color=(self.color[0], self.color[1], self.color[2], 0.75),
            )
            item.add_widget(icon)
            self.ids.list_view.add_widget(item, 1)
            self._popup.dismiss()
        content = AddUnitDialog(add_unit=add_unit_callback)
        self._popup = Popup(title='Add Unit', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def upload(self, file_type):
        self.file_type = file_type
        print(fe.file_extensions[file_type])
        if(len(self.new_transcript) != 0):
            self.new_transcript = []
        content = ChooseFile(select=self.select_file, cancel=self.dismiss_popup, file_filter=fe.file_extensions[file_type])
        self._popup = Popup(title="Choose File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        return
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def save(self):
        file_name = self._popup.content.file_name
        async def write_file():
            write_transcript(file_name, self.new_transcript, self.title)
            # add note to database
        asynckivy.start(write_file())
        self._popup.dismiss()
        item = TwoLineIconListItem(
            text= file_name,
            secondary_text=  datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S"),
        )
        icon = IconLeftWidget(
            icon="note",
            theme_text_color="Custom",
            text_color=(self.color[0], self.color[1], self.color[2], 0.75),
        )
        item.add_widget(icon)
        self.ids.list_view.add_widget(item)

    def select_file(self, path, selection):

        content = ProgressBar()
        self._popup._popup = Popup(title='Processing', content=content, size_hint=(0.5,0.6))
        self._popup._popup.open()
        print('selected file: ')
        print(path)
        print(selection)

        async def process_file():
            if(self.file_type == 'audio'):
                for i in selection:
                    block = generate_transcript(i)
                    self.new_transcript = [*self.new_transcript, *block]
            elif(self.file_type == 'video'):
                for i in selection:
                    audio_file = audio_from_video(i)
                    block = generate_transcript(audio_file)
                    self.new_transcript = [*self.new_transcript, *block]
        asynckivy.start(process_file())

        self._popup.dismiss()
        
        content = SaveFile(cancel=self.dismiss_popup, save=self.save)
        self._popup = Popup(title='Save File', content=content, size_hint=(0.9,0.9))
        self._popup.open()
    
    def show_notes(self, unittile):
        self.ids.list_view.add_widget(OneLineIconListItem(text='trial'), self.ids.list_view.children.index(unittile)+1)