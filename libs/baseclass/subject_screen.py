from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivy.properties import StringProperty, ColorProperty, ObjectProperty, NumericProperty
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, TwoLineIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.utils import asynckivy
from kivy.core.audio import SoundLoader
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.clipboard import Clipboard

from libs.baseclass.root_screen import RallyRootScreen
from libs.baseclass.add_unit_dialog import AddUnitDialog
from libs.baseclass.file_chooser import ChooseFile
from libs.baseclass.save_file_dialog import SaveFile
from libs.baseclass.bookmark import Bookmark
from functions.ibmspeechtotext import generate_transcript
from functions.write_transcript_to_notion import write_transcript, write_transcript_with_bookmarks, write_transcript_with_frames_and_bookmarks, validate_page, create_page_from_link, add_summary, get_text_from
from functions.audio_from_video import audio_from_video
import utils.file_extensions as fe
import global_vars as gv
from functions.summarize import get_summary

import os
import asyncio
from datetime import datetime
import webbrowser
import cv2

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
                on_touch_down=self.show_notes,
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
            if name not in [x.unit_name for x in gv.units[self.title]]:
                self.new_unit = name
                asynckivy.start(gv.add_unit(self.new_unit, self.title, self.sub_id, gv.user.uid))
                asynckivy.start(gv.get_units_for(gv.user.uid, self.sub_id, self.title))
                self.units = gv.units[self.title]
                item = OneLineIconListItem(
                    text= name,
                    on_touch_down=self.show_notes,
                )
                icon = IconLeftWidget(
                    icon="note",
                    theme_text_color="Custom",
                    text_color=(self.color[0], self.color[1], self.color[2], 0.75),
                )
                item.add_widget(icon)
                self.ids.list_view.add_widget(item, 1)
                self.unit_nos = str(int(self.unit_nos) + 1)
            else:
                print('Unit '+name+' already exists in '+self.title)
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
    
    def get_transcript_with_bookmarks(self, transcript, bookmark_indexes):
        self.new_transcript = transcript

    def update_ui(self, file_name, unit_name, dt_of_creation, num_of_bookmarks, unit_id):
        if unit_name in self.notes_shown:
            unittiles = [x for x in self.ids.list_view.children if type(x) == type(OneLineIconListItem())]
            unittile = [x for x in unittiles if x.text == unit_name][0]
            ind = self.ids.list_view.children.index(unittile)

            item = TwoLineIconListItem(
                text = file_name,
                secondary_text = 'On '+dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S")+'    '+str(num_of_bookmarks)+(' bookmarks' if num_of_bookmarks>1 else ' bookmark'),
                bg_color=[40/255, 44/255, 64/255,1],
                on_touch_down = self.open_note,
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
        print('selected file: ')
        print(path)
        print(selection)
        file_name = None
        unit_name = None
        unit_id = None
        dt_of_creation = None
        link = ''
        num_of_bookmarks = 0

        def finish():
            file_name = self._popup.content.file_name
            unit_name = self._popup.content.unit
            unit_id = [x for x in gv.units[self.title] if x.unit_name == unit_name][0].unit_id
            dt_of_creation = datetime.now()
            self._popup.dismiss()
            print(file_name, unit_name, unit_id, dt_of_creation)
            asynckivy.start(process_file())
            asynckivy.start(write_file())
            self.update_ui(file_name, unit_name, dt_of_creation, num_of_bookmarks, unit_id)
        
        def add_bookmarks():
            file_name = self._popup.content.file_name
            unit_name = self._popup.content.unit
            unit_id = [x for x in gv.units[self.title] if x.unit_name == unit_name][0].unit_id
            dt_of_creation = datetime.now()

            async def write_file_with_bm(transcript, num_of_bookmarks):
                self._popup.dismiss()
                # print(self.ids.fl.children)
                link = await write_transcript_with_bookmarks(file_name, transcript, gv.user.token, gv.user.homepage_url, self.title, unit_name, dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"))
                num_of_bookmarks = num_of_bookmarks
                await gv.add_note(self.sub_id, gv.user.uid, unit_id, file_name, dt_of_creation.strftime(r"%Y-%m-%d %H:%M:%S"), link, num_of_bookmarks, 0)
                self.update_ui(file_name, unit_name, dt_of_creation, num_of_bookmarks, unit_id)

            async def write_file_with_bm_and_frames(frames, transcript, num_of_bookmarks, frame_dir):
                self._popup.dismiss()
                # print(self.ids.fl.children)
                link = await write_transcript_with_frames_and_bookmarks(file_name, frames, transcript, gv.user.token, gv.user.homepage_url, self.title, unit_name, dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"))
                num_of_bookmarks = num_of_bookmarks
                await gv.add_note(self.sub_id, gv.user.uid, unit_id, file_name, dt_of_creation.strftime(r"%Y-%m-%d %H:%M:%S"), link, num_of_bookmarks, 0)
                print('Cache generated during conversion store at: '+frame_dir+'\n'+'You can delete this folder after process is complete')
                # os.remove(frame_dir) # todo: figure out how to delete directory after done
                self.update_ui(file_name, unit_name, dt_of_creation, num_of_bookmarks, unit_id)

            sound = None
            audio_file = None
            video_file = 'none'
            vid = None
            vidcap = None
            temp_folder = ''
            if self.file_type == 'video':
                video_file = selection[0]
                audio_file = audio_from_video(selection[0])
                sound = SoundLoader.load(audio_file)
                vid = VideoPlayer(source=video_file, state='pause')
                vidcap = cv2.VideoCapture(video_file)
                temp_folder = os.path.join(path, os.path.join('easy_notes_cache','temp_'+self.title+'_'+unit_name+'_'+file_name))
                os.mkdir(temp_folder)
            else:
                audio_file = selection[0]
                sound = SoundLoader.load(selection[0])
            self._popup.dismiss()
            content = Bookmark(
                file_type=self.file_type,
                sound=sound, vid=vid, vidcap=vidcap,
                audio_file=audio_file, video_file=video_file, temp_folder=temp_folder,
                finish_up=write_file_with_bm if self.file_type == 'audio' else write_file_with_bm_and_frames)
            self._popup = Popup(title='Add Bookmarks', content=content, size_hint=(1, 1))
            self._popup.open()
        
        async def write_file():
            file_name = self._popup.content.file_name
            unit_name = self._popup.content.unit
            unit_id = [x for x in gv.units[self.title] if x.unit_name == unit_name][0].unit_id
            dt_of_creation = datetime.now()
            link = await write_transcript(file_name, self.new_transcript, gv.user.token, gv.user.homepage_url, self.title, unit_name, dt_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S"))
            await gv.add_note(self.sub_id, gv.user.uid, unit_id, file_name, dt_of_creation.strftime(r"%Y-%m-%d %H:%M:%S"), link, num_of_bookmarks, 0)

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
        # asynckivy.start(process_file())

        self._popup.dismiss()
        
        content = SaveFile(finish=finish, go_to_bookmark=add_bookmarks, options=[x.unit_name for x in self.units], sub_name=self.title, sub_id=self.sub_id)
        self._popup = Popup(title='Save File', content=content, size_hint=(0.8,0.5))
        self._popup.open()
    
    def show_notes(self, unittile, touch):
        if unittile.collide_point(*touch.pos):
            print('move')
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
                            secondary_text = 'On '+i.datetime_of_creation.strftime(r"%m/%d/%Y, %H:%M:%S")+"    "+str(i.num_of_bookmarks)+(' bookmarks' if i.num_of_bookmarks>1 else ' bookmark'),
                            bg_color=[40/255, 44/255, 64/255,1],
                            on_touch_down = self.open_note,
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
            return True
    
    def open_note(self, notetile, touch):
        if notetile.collide_point(*touch.pos):
            print(touch.button)
            unittiles = [x for x in self.ids.list_view.children 
                if type(x) == type(OneLineIconListItem()) and x.text in self.notes_shown 
                and self.ids.list_view.children.index(x) > self.ids.list_view.children.index(notetile)]
            # print([x.text for x in unittiles])
            unittile = unittiles[0]
            unit_name = unittiles[0].text
            print(unit_name)
            note = [x for x in self.notes[unit_name] if x.note_title == notetile.text][0]
            if touch.button == 'left':
                # bxlay = notetile.parent.parent
                webbrowser.open(note.link)
            if touch.button == 'right':
                def share_callback():
                    async def send_share_req(fid):
                        print('sending request...')
                        dt = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
                        await gv.send_share_req(fid, note.note_id, self.title, unit_name, dt, note.note_title)
                        self._popup.dismiss()

                    content = ShareInfoPopup(note_id=note.note_id, send_share=send_share_req, link=note.link)
                    self._popup.dismiss()
                    self._popup = Popup(title='Share Information', content=content, size_hint=(0.5, 0.5))
                    self._popup.open()
                
                def delete_callback():
                    async def confirm_deletion(opt):
                        if opt == 'yes':
                            print('in')
                            deleted = await gv.delete_note(note.note_id)
                            if deleted:
                                del gv.notes[self.title][unit_name]
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
                            print('cancelled')
                        self._popup.dismiss()
                    
                    content = Confirmation(delete=confirm_deletion)
                    self._popup.dismiss()
                    self._popup = Popup(title='Confirm', content=content, size_hint=(0.5, 0.3))
                    self._popup.open()

                async def summarise_callback():
                    
                    async def generate_and_add_summary(num_of_lines):
                            # generate summary
                        text = await get_text_from(gv.user.token, gv.user.homepage_url, self.title, unit_name, note.note_title)
                        summ = get_summary(text, num_of_lines)
                        # write summary
                        await add_summary(gv.user.token, gv.user.homepage_url, self.title, unit_name, note.note_title, summ)
                        # change status in db
                        await gv.set_summarised(note.note_id)
                        self._popup.dismiss()
                        
                    # check status in db
                    summ = await gv.check_if_summarised(note.note_id)
                    if not summ:
                        content = SetNum(finish=generate_and_add_summary)
                        self._popup.dismiss()
                        self._popup = Popup(title='Set Parameters', content=content, size_hint=(0.5, 0.5))
                        self._popup.open()
                    else:
                        print('Note Already Summarised')
            
                content=OptionsPopup(share=share_callback, delete=delete_callback, summarise=summarise_callback)
                self._popup = Popup(title='Options', content=content, size_hint=(0.2, 0.35), pos=touch.pos)
                self._popup.open()
            return True
    
    def upload_link(self):

        def create_note_from_link():
            old_link = self._popup.content.link
            self._popup.dismiss()

            def finish_callback():
                file_name = self._popup.content.file_name
                unit_name = self._popup.content.unit
                unit_id = [x for x in gv.units[self.title] if x.unit_name == unit_name][0].unit_id
                dt_of_creation = datetime.now()
                num_of_bookmarks = 0
                
                async def process():
                    self._popup.dismiss()
                    # print(self.ids.fl.children)
                    link = await create_page_from_link(old_link, gv.user.token, gv.user.homepage_url, self.title, unit_name, file_name, dt_of_creation)
                    await gv.add_note(self.sub_id, gv.user.uid, unit_id, file_name, dt_of_creation.strftime(r"%Y-%m-%d %H:%M:%S"), link, num_of_bookmarks, 0)
                asynckivy.start(process())
                self.update_ui(file_name, unit_name, dt_of_creation, num_of_bookmarks, unit_id)
            
            content = SaveFile(finish=finish_callback, options=[x.unit_name for x in self.units], sub_name=self.title, sub_id=self.sub_id, disable_bm=True)
            self._popup = Popup(title='Save File', content=content, size_hint=(0.8,0.5))
            self._popup.open()

        content = UploadLinkPopup(finish_callback=create_note_from_link)
        self._popup = Popup(title='Upload Note', content=content, size_hint=(0.6, 0.6))
        self._popup.open()


class OptionsPopup(FloatLayout):
    share = ObjectProperty()
    delete = ObjectProperty()
    summarise = ObjectProperty()

    def summ(self):
        asynckivy.start(self.summarise())

class ShareInfoPopup(FloatLayout):
    note_id = NumericProperty()
    send_share = ObjectProperty()
    delete = ObjectProperty()
    link = StringProperty()

    def send_share_callback(self):
        nm = self.ids.fid.text
        fid = None
        is_fid_friend = False
        async def validate_req():
            nonlocal is_fid_friend, fid
            fid = await gv.get_uid_for_nm(nm)
            valid = fid is not None
            if valid:
                is_fid_friend = await gv.check_if_fid_friend(int(fid), self.note_id)
            else:
                print('Username not valid')
        asynckivy.start(validate_req())
        if is_fid_friend:
            asynckivy.start(self.send_share(int(fid)))

class Confirmation(FloatLayout):
    delete = ObjectProperty()
    
    def delete_callback(self, opt):
        asynckivy.start(self.delete(opt))

class UploadLinkPopup(FloatLayout):
    finish_callback = ObjectProperty()
    link = StringProperty()

    def validate(self):
        link = self.ids.link.text
        valid = False
        async def link_valid():
            nonlocal valid
            valid = await validate_page(gv.user.token, link)
        asynckivy.start(link_valid())
        if valid:
            self.link = self.ids.link.text
            self.finish_callback()

class SetNum(FloatLayout):
    finish = ObjectProperty()
    num_of_lines = 5

    def inc_lines(self):
        self.num_of_lines += 1
        self.ids.nol.text = str(self.num_of_lines)

    def dec_lines(self):
        self.num_of_lines -= 1
        self.ids.nol.text = str(self.num_of_lines)
    
    def complete(self):
        asynckivy.start(self.finish(self.num_of_lines))
