from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty

class SaveFile(BoxLayout):
    sub_name = StringProperty()
    file_name = StringProperty()
    finish = ObjectProperty()
    go_to_bookmark = ObjectProperty()
    options = ListProperty()
    unit = None

    def pre_save(self, btn):
        if self.ids.file_name.text != '' and self.unit is not None:
            self.file_name = self.ids.file_name.text
            if btn == 'next':
                self.go_to_bookmark()
            else:
                self.finish()

    def select_unit(self, unit):
        self.unit = unit