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
        # self.ids.nav_bar.set_current(ind)


class RallyListItem(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    bar_color = ColorProperty((1, 0, 0, 1))


class RallySeeAllButton(RectangularRippleBehavior, MDBoxLayout):
    pass

# from kivy.properties import ColorProperty, StringProperty, ObjectProperty

# from kivymd.theming import ThemableBehavior
# from kivymd.uix.behaviors import RectangularRippleBehavior
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.screen import MDScreen
# from kivy.uix.screenmanager import ScreenManager

# import libs.baseclass.overview_screen as overview_screen
# import libs.baseclass.accounts_screen as accounts_screen
# import libs.baseclass.bills_screen as bills_screen
# import libs.baseclass.settings_screen as settings_screen

# class RallyRootScreen(MDScreen):
    
#     current_screen = StringProperty(None)
#     sm = ScreenManager()
#     screen_names = ['HOME', 'SUBJECTS', 'FRIENDS', 'SETTINGS']
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.sm.add_widget(overview_screen.RallyOverviewScreen(name='HOME'))
#         self.sm.add_widget(accounts_screen.RallyAccountsScreen(name='SUBJECTS'))
#         self.sm.add_widget(bills_screen.RallyBillsScreen(name='FRIENDS'))
#         self.sm.add_widget(settings_screen.RallySettingsScreen(name='SETTINGS'))
#         self.sm.current = "HOME"

#     def on_pre_enter(self, *args):
#         self.ids.scr_manager = self.sm
#         print(self.ids.scr_manager.current)
#         if self.current_screen is not None:
#             print('passed: '+self.current_screen)
#             self.ids.scr_manager.current = self.current_screen
#             print(self.ids.scr_manager.current)
    
#     def navigate(self, to_screen):
#         ind = self.screen_names.index(self.ids.scr_manager.current)
#         new_ind = self.screen_names.index(to_screen)
#         if ind < new_ind:
#             self.ids.scr_manager.transition.direction = "right"
#         else:
#             self.ids.scr_manager.transition.direction = "left"
#         self.ids.scr_manager.current = to_screen



# class RallyListItem(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
#     text = StringProperty()
#     secondary_text = StringProperty()
#     tertiary_text = StringProperty()
#     bar_color = ColorProperty((1, 0, 0, 1))


# class RallySeeAllButton(RectangularRippleBehavior, MDBoxLayout):
#     pass
