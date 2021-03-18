from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty

class SaveFile(BoxLayout):
    sub_name = StringProperty()
    file_name = StringProperty()
    save = ObjectProperty()
    cancel = ObjectProperty()
    options = ListProperty()
    unit = None

    def pre_save(self):
        if self.ids.file_name.text != '' and self.unit is not None:
            self.file_name = self.ids.file_name.text
            self.save()

    def select_unit(self, unit):
        self.unit = unit