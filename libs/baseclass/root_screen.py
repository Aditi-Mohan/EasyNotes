from kivy.properties import ColorProperty, StringProperty, NumericProperty

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock


class RallyRootScreen(MDScreen):
    back_press = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.back_press:
            pass
        else:
            Clock.schedule_once(lambda x: self.back_press_callback(self.back_press))

    def back_press_callback(self, name):
        for each in self.ids.nav_bar.ids._button_box.children:
            if each.text == name:
                each.dispatch("on_release")


class RallyListItem(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    bar_color = ColorProperty((1, 0, 0, 1))


class RallySeeAllButton(RectangularRippleBehavior, MDBoxLayout):
    pass
