from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

class SubjectScreen(MDScreen):
    title = StringProperty()
    
    def on_pre_enter(self, *args):
        self.title = self.name
