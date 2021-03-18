from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivymd.utils import asynckivy

class AddUnitDialog(BoxLayout):
    add_unit = ObjectProperty()

    def finish(self):
        name = self.ids.unit_name.text
        if name != '':
            self.add_unit(name)
        