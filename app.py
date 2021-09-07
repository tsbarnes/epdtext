import time
import epd

from screens import affirmations, calendar, uptime

from settings import TIME


def handle_btn0_press():
    app.handle_btn0_press()


def handle_btn1_press():
    app.handle_btn1_press()


def handle_btn2_press():
    app.handle_btn2_press()


def handle_btn3_press():
    app.handle_btn3_press()


class App:
    last_pressed = 0

    def handle_btn0_press(self):
        self.last_pressed = 0
        affirmations.handle_btn_press()

    def handle_btn1_press(self):
        self.last_pressed = 1
        calendar.handle_btn_press()

    def handle_btn2_press(self):
        self.last_pressed = 2

    def handle_btn3_press(self):
        self.last_pressed = 3
        uptime.handle_btn_press()

    def __init__(self):
        btns = epd.get_buttons()
        btns[0].when_pressed = handle_btn0_press
        btns[1].when_pressed = handle_btn1_press
        btns[2].when_pressed = handle_btn2_press
        btns[3].when_pressed = handle_btn3_press

    def loop(self):
        while True:
            if self.last_pressed == 0:
                affirmations.print_to_display()
            if self.last_pressed == 1:
                calendar.print_to_display()
            if self.last_pressed == 3:
                uptime.print_to_display()
            time.sleep(TIME)


app = App()
app.loop()
