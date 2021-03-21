from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ColorProperty

class Bookmark(BoxLayout):
    file_type = StringProperty()

    def video_press_callback(self, btn):
        if self.file_type == 'video':
            print(btn.text)
        else:
            pass
    
    def audio_press_callback(self, btn):
        print(btn.text)

    def audio_bookmark_content(self):
        return Label(text='Audio Bookmark')
    
    def video_bookmark_content(self):
        return Label(text='Video Bookmark')
            
        
        # TabbedPanelItem:
        #     id: video
        #     text: 'video tab'
        #     background_color: root.video_color
        #     content: root.video_bookmark_content()