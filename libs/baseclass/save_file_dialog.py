from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
import global_vars as gv
from kivymd.utils import asynckivy

class SaveFile(BoxLayout):
    sub_name = StringProperty()
    sub_id = NumericProperty()
    file_name = StringProperty()
    finish = ObjectProperty()
    go_to_bookmark = ObjectProperty()
    options = ListProperty()
    unit = None

    def pre_save(self, btn):
        if self.ids.file_name.text != '' and self.unit is not None:
            self.file_name = self.ids.file_name.text
            al_exists = True

            async def check_if_already_exists():
                nonlocal al_exists
                if self.sub_name in gv.notes.keys():
                    if self.unit in gv.notes[self.sub_name].keys():
                        if self.file_name not in [x.note_title for x in gv.notes[self.sub_name][self.unit]]:
                            al_exists = False
                            return
                        else:
                            print('Note with the same name Already Exists in this Unit')
                            return
                unit_id = [x for x in gv.units[self.sub_name] if x.unit_name == self.unit][0].unit_id
                await gv.get_notes_for(gv.user.uid, sub_id, unit_id, self.unit, self.sub_name)
                if self.file_name not in [x.note_title for x in gv.notes[self.sub_name][self.unit]]:
                    al_exists = False    
                else:
                    print('Note with the same name Already Exists in this Unit')

            asynckivy.start(check_if_already_exists())
            if not al_exists:
                if btn == 'next':
                    self.go_to_bookmark()
                else:
                    self.finish()

    def select_unit(self, unit):
        self.unit = unit