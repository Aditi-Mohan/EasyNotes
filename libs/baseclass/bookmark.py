from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader

from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton

from functions.ibmspeechtotext import print_text

from pydub import AudioSegment
import io
import re

class Bookmark(BoxLayout):
    file_type = StringProperty()
    playing = False
    sound = ObjectProperty()
    temp_folder = StringProperty()
    audio_file = StringProperty()
    forward_backward_color = (1, 1, 1, 1)
    bookmarks = []
    start_enable = True
    stop_enable = False
    
    # def on_stop(self, arg):
    #     self.playing = False
    #     if self.stop_enable:
    #         self.bookmarks[-1].append(self.sound.length)
    #     self.stop_enable = False
    #     self.start_enable = False
    #     print(self.bookmarks)
    
    def play_pause_audio(self, btn):
        if self.playing:
            self.sound.stop()
            self.start_enable = False
            self.stop_enable = False
        else:
            self.sound.play()
            # self.sound.bind(on_stop=self.on_stop)
            if len(self.bookmarks) > 0:
                if len(self.bookmarks[-1]) == 1:
                    self.stop_enable = True
                else:
                    self.start_enable = True
        self.playing = not self.playing
        # print(self.playing)

    def forward_backward(self, btn):
        if self.playing:
            name = btn.icon
            pos = self.sound.get_pos()
            if re.search('forward', name) is not None:
                print('going forward 10s')
                self.sound.seek(pos+10 if pos+10 < self.sound.length else self.sound.length)
            else:
                print('going back 10s')
                self.sound.seek(pos-10 if pos-10 >=0 else 0)
    
    def start_bookmark(self, btn):
        pos = self.sound.get_pos()
        if self.start_enable:
            if len(self.bookmarks) > 0:
                valid = True
                for x, y in self.bookmarks:
                    if x <= pos and pos <= y:
                        valid = False
                if valid:
                    self.bookmarks.append([pos])
                    self.start_enable = False
                    self.stop_enable = True
            else:
                self.bookmarks.append([pos])
                self.start_enable = False
                self.stop_enable = True
    
    def stop_bookmark(self, btn):
        pos = self.sound.get_pos()
        if self.stop_enable:
            if len(self.bookmarks) > 1:
                valid = True
                for x, y in self.bookmarks[:len(self.bookmarks)-2]:
                    if x <= pos and pos >= y:
                        valid = False
                if valid:
                    if pos > self.bookmarks[-1][0]:
                        self.bookmarks[-1].append(pos)
                    else:
                        self.bookmarks.remove(self.bookmarks[-1])
            elif pos > self.bookmarks[-1][0]:
                self.bookmarks[-1].append(pos)
            else:
                self.bookmarks.remove(self.bookmarks[-1])
            self.start_enable = True
            self.stop_enable = False
    
    def split_audio(self, btn):
        if len(self.bookmarks) > 0:
            i = 0
            sections = []
            for a, b in self.bookmarks:
                if i != a:
                    sections.append([i, a])
                    sections.append([a, b])
                    i = b
                else:
                    sections.append([a, b])
                    i = b
            if i != self.sound.length:
                sections.append([i, self.sound.length])
            transcript = []
            for start, stop in sections:
                start = start * 1000 #Works in milliseconds
                stop = stop * 1000
                newAudio = AudioSegment.from_wav(self.audio_file)
                newAudio = newAudio[start:stop]
                buf = io.BytesIO()
                newAudio.export(buf, format='wav')
                print_text(buf.getvalue())
                # newAudio.export('newSong.wav', format="wav")

    def audio_bookmark_content(self):
        
        bx = BoxLayout(orientation='vertical')
        bx1 = BoxLayout(orientation='horizontal', spacing=100)
        bx2 = BoxLayout(orientation='vertical', spacing=50)

        p = ProgressBar()
        bx1.add_widget(p)

        control_panel = BoxLayout(orientation='horizontal', spacing=50, padding=[200, 0, 50, 200])
        play_pause_btn = MDIconButton(
            icon = 'play-pause',
            on_release = self.play_pause_audio,
        )
        ten_sec_forward = MDIconButton(
            icon = 'step-forward-2',
            theme_text_color = "Custom",
            text_color = self.forward_backward_color,
            on_release = self.forward_backward,
        )
        ten_sec_backward = MDIconButton(
            icon = 'step-backward-2',
            theme_text_color = "Custom",
            text_color = self.forward_backward_color,
            on_release = self.forward_backward,
        )
        control_panel.add_widget(ten_sec_backward)
        control_panel.add_widget(play_pause_btn)
        control_panel.add_widget(ten_sec_forward)
        # bx1.add_widget(control_panel)

        start = MDFillRoundFlatButton(
            text = 'Start',
            on_release = self.start_bookmark,
        )
        stop = MDFillRoundFlatButton(
            text = 'Stop',
            on_release = self.stop_bookmark,
        )
        done = MDFillRoundFlatButton(
            text='DONE',
            on_release= self.split_audio,
        )
        bx2.add_widget(start)
        bx2.add_widget(stop)
        bx2.add_widget(done)

        bx1.add_widget(bx2)
        bx.add_widget(bx1)
        bx.add_widget(control_panel)
        return bx
    
    def video_bookmark_content(self):
        return Label(text='Video Bookmark')
            
        
        # TabbedPanelItem:
        #     id: video
        #     text: 'video tab'
        #     background_color: root.video_color
        #     content: root.video_bookmark_content()
