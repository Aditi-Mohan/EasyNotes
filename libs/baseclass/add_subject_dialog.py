from kivy.uix.boxlayout import BoxLayout
from libs.baseclass.color_picker_popup import ColorPickerPopup
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivymd.utils import asynckivy
import asyncio

class AddSubjectDialog(BoxLayout):
    add_sub = ObjectProperty()
    
    def popup_dismiss(self):
        self._popup.dismiss()

    # To monitor changes, we can bind to color property changes
    def on_color(self):
        instance = self._popup.content.ids.clr_picker
        self.ids.clr_disp.my_color = instance.color #  or value
        self.popup_dismiss()

    def choose_color(self):
        async def cp_popup():
            content = ColorPickerPopup(select=self.on_color)
            self._popup = Popup(title='Pick A Color', content=content, size_hint=(0.5, 0.5))
            self._popup.open()
        asynckivy.start(cp_popup())
        
    def finish(self):
        name = self.ids.sub_name.text
        color = self.ids.clr_disp.my_color
        fac_name = self.ids.fac_name.text
        if name != '' and fac_name != '':
            print(color)
            self.add_sub(name, fac_name, color)
        