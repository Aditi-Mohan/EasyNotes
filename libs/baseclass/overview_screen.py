from kivy.properties import ListProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton


class RallyOverviewScreen(MDScreen):
    pass


class OverviewBox(MDBoxLayout):
    title = StringProperty()
    money = StringProperty()
    text = ListProperty(["", "", ""])
    secondary_text = ListProperty(["", "", ""])
    tertiary_text = ListProperty(["", "", ""])
    bar_color = ListProperty([(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)])
