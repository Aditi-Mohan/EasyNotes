from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivymd.utils import asynckivy
from kivy.uix.videoplayer import VideoPlayer

from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.list import MDList,TwoLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView

from functions.ibmspeechtotext import print_text

from pydub import AudioSegment
import io
import re
import cv2

class Bookmark(BoxLayout):
    file_type = StringProperty()
    playing = False
    sound = ObjectProperty()
    vid = ObjectProperty()
    vidcap = ObjectProperty()
    audio_file = StringProperty()
    video_file = StringProperty()
    finish_up = ObjectProperty()
    forward_backward_color = (1, 1, 1, 1)
    bookmarks = []
    frames = []
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
    
    def done(self, btn):
        asynckivy.start(self.split_audio())

    async def split_audio(self):
        if len(self.bookmarks) > 0:
            i = 0
            sections = []
            for a, b in self.bookmarks:
                if i != a:
                    sections.append([i, a, 0])
                    sections.append([a, b, 1])
                    i = b
                else:
                    sections.append([a, b, 1])
                    i = b
            if i != self.sound.length:
                sections.append([i, self.sound.length, 0])
            transcript = []
            for start, stop, is_bm in sections:
                start = start * 1000 #Works in milliseconds
                stop = stop * 1000
                newAudio = AudioSegment.from_wav(self.audio_file)
                newAudio = newAudio[start:stop]
                buf = io.BytesIO()
                newAudio.export(buf, format='wav')
                text = await print_text(buf.getvalue())
                transcript.append([text, is_bm])
            print(transcript)
            asynckivy.start(self.finish_up(transcript, len(self.bookmarks)))
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
            on_release= self.done,
        )
        list_of_bookmarks = MDList()
        bx2.add_widget(start)
        bx2.add_widget(stop)
        bx2.add_widget(list_of_bookmarks)
        bx2.add_widget(done)

        bx1.add_widget(bx2)
        bx.add_widget(bx1)
        bx.add_widget(control_panel)
        return bx
    
    def remove_bookmark(self, elm, x):
        print(ind)
        print(self.frames)
        self.frames.remove(elm)
        lst = self.children[0].current_tab.content.children[1].children[0].children[0]
        lst.remove_widget(x)
    
    def capture_frame(self, btn):
        pos = self.vid.position
        fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        ind = round(pos*fps)
        if len(self.frames) > 0:
            if ind not in self.frames[:][0]:
                print(ind)
                elm = [ind, pos]
                self.frames.append(elm)
                lst = self.children[0].current_tab.content.children[1].children[0].children[0]
                item = TwoLineIconListItem(
                    text='Bookmark at '+str(pos)+' seconds',
                    secondary_text = 'Click to remove',
                    on_release=lambda x: self.remove_bookmark(elm, x),
                )
                icon = IconLeftWidget(
                    icon = 'bookmark-remove'
                )
                item.add_widget(icon)
                lst.add_widget(item)
        else:
            elm = [ind, pos]
            self.frames.append(elm)
            lst = self.children[0].current_tab.content.children[1].children[0].children[0]
            item = TwoLineIconListItem(
                text='Bookmark at '+str(pos)+' seconds',
                secondary_text = 'Click to remove',
                on_release=lambda x: self.remove_bookmark(elm, x),
            )
            icon = IconLeftWidget(
                icon = 'bookmark-remove'
            )
            item.add_widget(icon)
            lst.add_widget(item)
    
    
    def get_frames(self, btn):
        
        cap = self.vidcap

        # get total number of frames
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_img = []
        for ind, pos in self.frames:

            # check for valid frame number
            if ind >= 0 & ind <= totalFrames:
                # set frame position
                cap.set(cv2.CAP_PROP_POS_FRAMES,ind)
                ret, frame = cap.read()
                frame_img.append(frame)
                # cv2.imwrite("frame"+str(count)+".jpg", frame)
                # cv2.imshow("Frame", frame)
        # print(frame_img)
        #     if cv2.waitKey(20) & 0xFF == ord('q'):
        #         break

        # cv2.destroyAllWindows()

    def video_bookmark_content(self):
                
        bx1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.9))
        control_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=50)
        bx = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        capture = MDFillRoundFlatButton(
            text = 'Capture Frame',
            on_release= self.capture_frame,
        )
        done = MDFillRoundFlatButton(
            text = 'Complete with Audio Bookmarks',
            on_release= self.get_frames,
        )
        self.vid.keep_ratio = True
        self.vid.size_hint = (0.7, 0.8)
        scrvw = ScrollView(size_hint=(0.3, 1))
        list_of_bookmarks = MDList()
        list_of_bookmarks.add_widget(TwoLineIconListItem(text='hi there'))
        scrvw.add_widget(list_of_bookmarks)
        bx1.add_widget(self.vid)
        bx1.add_widget(scrvw)
        bx.add_widget(bx1)
        control_panel.add_widget(capture)
        control_panel.add_widget(done)
        bx.add_widget(control_panel)
        return bx
