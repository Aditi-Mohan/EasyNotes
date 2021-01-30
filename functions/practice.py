from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

Config.set('graphics', 'resizable', True)

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
    
    def build(self):
        Fl = FloatLayout()
        btn1 = Button(text ='btn1', size_hint=(0.2, 0.1), pos_hint={'x':0.15, 'y':0.45})
        btn2 = Button(text ='btn2', size_hint=(0.2, 0.1), pos_hint={'x':0.65, 'y':0.45})
        Fl.add_widget(btn1)
        Fl.add_widget(btn2)

        return Fl

def main():
    MyApp().run()


if __name__ == '__main__':
    main()