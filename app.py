import time
import epd

import affirmations as af
import uptime as up

from settings import TIME


def handle_btn0_press():
    app.handle_btn0_press()


def handle_btn3_press():
    app.handle_btn3_press()


class App:
    last_pressed = 0

    def handle_btn0_press(self):
        self.last_pressed = 0
        af.handle_btn_press()

    def handle_btn3_press(self):
        self.last_pressed = 3
        up.handle_btn_press()

    def __init__(self):
        btns = epd.get_buttons()
        btns[0].when_pressed = handle_btn0_press
        btns[3].when_pressed = handle_btn3_press

    def loop(self):
        while True:
            if self.last_pressed == 0:
                af.print_to_display()
            if self.last_pressed == 3:
                up.print_to_display()
            time.sleep(TIME)


app = App()
app.loop()
