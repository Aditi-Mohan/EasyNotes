import cv2
import numpy as np
import pyautogui

from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window

class RecordScreen(App):
    def __init__(self, **kwargs):
        super(RecordScreen, self).__init__(**kwargs)

    def record(self, event):
        # SCREEN_SIZE = Window.size
        SCREEN_SIZE = (1366, 768)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("output.avi", fourcc, 24.0, SCREEN_SIZE)

        while True:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            cv2.imshow("screenshot", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        cv2.destroyAllWindows()
        out.release()
    
    def build(self):
        btn = Button(text="Start Recording", size=(100, 200), background_color=(255, 0, 0, 1), color=(0, 0, 0, 1))
        btn.bind(on_press=self.record)
        return btn
    


def main():
    RecordScreen().run()


if __name__ == '__main__':
    main()
