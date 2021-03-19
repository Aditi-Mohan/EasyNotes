from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivy.properties import StringProperty, ColorProperty, ObjectProperty, NumericProperty
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, TwoLineIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.boxlayout import BoxLayout
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
import webbrowser

class SubjectScreen(MDScreen):
    title = StringProperty()
    color = ColorProperty()
    btn_color = ColorProperty()
    unit_nos = StringProperty()
    sub_id = NumericProperty()
    # notes = [{'title': 'LESSON 1', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 2', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 3', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 4', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},
    #         {'title': 'LESSON 5', 'time': datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")},]
    units = []
    new_transcript = []
    file_type = ''
    notes = {}
    new_unit = None
    notes_shown = []
    
    def on_pre_enter(self, *args):
        self.btn_color = (self.color[0], self.color[1], self.color[2], 0.4)
        list_view = self.ids.list_view
        self.notes_shown = []
        if self.title in gv.units.keys():
            self.units = gv.units[self.title]
        else:
            print('loading...')
            asynckivy.start(gv.get_units_for(gv.user.uid, self.sub_id, self.title))
            self.units = gv.units[self.title]
        self.unit_nos = str(len(self.units))
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
            self.units = gv.units[self.title]
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
            self.unit_nos = str(int(self.unit_nos) + 1)
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
        unit_name = self._popup.content.unit
        unit_id = [x for x in gv.units[self.title] if x.unit_name == unit_name][0].unit_id
        dt_of_creation = datetime.now()
        link = ''
        async def write_file():
            link = await write_transcript(file_name, self.new_transcript, gv.user.token, gv.user.homepage_url, self.title, unit_name, dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"))
            await gv.add_note(self.sub_id, gv.user.uid, unit_id, file_name, dt_of_creation.strftime(r"%Y-%m-%d %H:%M:%S"), link)
        asynckivy.start(write_file())
        self._popup.dismiss()
        if unit_name in self.notes_shown:
            unittiles = [x for x in self.ids.list_view.children if type(x) == type(OneLineIconListItem())]
            unittile = [x for x in unittiles if x.text == unit_name][0]
            ind = self.ids.list_view.children.index(unittile) - 1

            item = TwoLineIconListItem(
                text = file_name,
                secondary_text = dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"),
                bg_color=[40/255, 44/255, 64/255,1],
                on_release = self.open_note,
            )
            icon = IconLeftWidget(
                icon="subdirectory-arrow-right",
                theme_text_color="Custom",
                text_color=(self.color[0], self.color[1], self.color[2], 0.75),
            )
            item.add_widget(icon)
            if type(self.ids.list_view.children[ind]) == type(OneLineListItem()):
                nt = self.ids.list_view.children[ind]
                self.ids.list_view.remove_widget(nt)
                self.ids.list_view.add_widget(item, ind)
            else:
                # nt = self.ids.list_view.children[ind+1]
                self.ids.list_view.add_widget(item, ind)
        #     if type(bxlay) == type(OneLineListItem()):
        #         self.ids.list_view.remove_widget(bxlay)
        #         bxlay = BoxLayout(padding=[15,0,0,0])
        #         new_list = MDList()
        #         new_list.add_widget(item)
        #         bxlay.add_widget(new_list)
        #         self.ids.list_view.add_widget(bxlay, self.ids.list_view.children.index(unittile))
        #     else:
        #         bxlay.children[0].add_widget(item)
        asynckivy.start(gv.get_notes_for(gv.user.uid, self.sub_id, unit_id, unit_name, self.title))
        self.notes[unit_name] = gv.notes[self.title][unit_name]

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
        
        content = SaveFile(cancel=self.dismiss_popup, save=self.save, options=[x.unit_name for x in self.units])
        self._popup = Popup(title='Save File', content=content, size_hint=(0.9,0.9))
        self._popup.open()
    
    def show_notes(self, unittile):
        if unittile.text in self.notes_shown:
            # bxlay = self.ids.list_view.children[self.ids.list_view.children.index(unittile)-1]
            ind = self.ids.list_view.children.index(unittile) - 1
            while ind >= 1:
                nt = self.ids.list_view.children[ind]
                if type(nt) == type(OneLineIconListItem()):
                    break
                self.ids.list_view.remove_widget(nt)
                ind -= 1
            # self.ids.list_view.remove_widget(bxlay)
            self.notes_shown.remove(unittile.text)
        else:
            unit = [x for x in self.units if x.unit_name == unittile.text][0]
            if self.title in gv.notes.keys():
                if unit.unit_name in gv.notes[self.title].keys():
                    self.notes[unit.unit_name] = gv.notes[self.title][unit.unit_name]
                else:
                    asynckivy.start(gv.get_notes_for(gv.user.uid, self.sub_id, unit.unit_id, unit.unit_name, self.title))
                    self.notes[unit.unit_name] = gv.notes[self.title][unit.unit_name]
            else:
                asynckivy.start(gv.get_notes_for(gv.user.uid, self.sub_id, unit.unit_id, unit.unit_name, self.title))
                self.notes[unit.unit_name] = gv.notes[self.title][unit.unit_name]
            if len(self.notes[unit.unit_name]) == 0:
                self.ids.list_view.add_widget(
                    OneLineListItem(
                        text='No Notes For '+unittile.text,
                        theme_text_color='Custom',
                        text_color=[158/255, 160/255, 163/255, 1]
                    ),
                    self.ids.list_view.children.index(unittile)
                )
            else:
                # new_list = MDList()
                ind = self.ids.list_view.children.index(unittile)
                for i in self.notes[unit.unit_name]:
                    item = TwoLineIconListItem(
                        text = i.note_title,
                        secondary_text = i.datetime_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"),
                        bg_color=[40/255, 44/255, 64/255,1],
                        on_release = self.open_note,
                    )
                    icon = IconLeftWidget(
                        icon="subdirectory-arrow-right",
                        theme_text_color="Custom",
                        text_color=(self.color[0], self.color[1], self.color[2], 0.75),
                    )
                    item.add_widget(icon)
                    self.ids.list_view.add_widget(item, ind)
                    ind += 1
                    # new_list.add_widget(item)
                # bxlay = BoxLayout(padding=[15,0,0,0])
                # bxlay.add_widget(new_list)
                # self.ids.list_view.add_widget(bxlay, self.ids.list_view.children.index(unittile))
            self.notes_shown.append(unittile.text)
    
    def open_note(self, notetile):
        # bxlay = notetile.parent.parent
        unittiles = [x for x in self.ids.list_view.children 
                        if type(x) == type(OneLineIconListItem()) and x.text in self.notes_shown 
                        and self.ids.list_view.children.index(x) > self.ids.list_view.children.index(notetile)]
        unit_name = unittiles[-1].text
        print(unit_name)
        note = [x for x in self.notes[unit_name] if x.note_title == notetile.text][0]
        webbrowser.open(note.link)
    
    # def open_unit(self, unittile):