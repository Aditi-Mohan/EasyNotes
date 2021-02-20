from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

class SaveFile(BoxLayout):
    sub_name = StringProperty()
    file_name = StringProperty()
    save = ObjectProperty()
    cancel = ObjectProperty()

    def pre_save(self):
        self.sub_name = self.ids.sub_name.text
        self.save()