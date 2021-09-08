import time
import epd
import importlib

from settings import TIME, SCREENS
from utils import log


def handle_btn0_press():
    app.handle_btn0_press()


def handle_btn1_press():
    app.handle_btn1_press()


def handle_btn2_press():
    app.handle_btn2_press()


def handle_btn3_press():
    app.handle_btn3_press()


class App:
    current_screen = 0

    def handle_btn0_press(self):
        if self.current_screen > 0:
            self.current_screen -= 1
        else:
            self.current_screen = len(self.screens) - 1
        log("Current screen: {0}".format(self.current_screen))
        self.screens[self.current_screen].print_to_display()

    def handle_btn1_press(self):
        self.screens[self.current_screen].handle_btn_press(button_number=1)

    def handle_btn2_press(self):
        self.screens[self.current_screen].handle_btn_press(button_number=2)

    def handle_btn3_press(self):
        self.current_screen += 1
        if self.current_screen >= len(self.screens):
            self.current_screen = 0
        log("Current screen: {0}".format(self.current_screen))
        self.screens[self.current_screen].print_to_display()

    def __init__(self):
        epd.clear_screen()
        btns = epd.get_buttons()
        btns[0].when_pressed = handle_btn0_press
        btns[1].when_pressed = handle_btn1_press
        btns[2].when_pressed = handle_btn2_press
        btns[3].when_pressed = handle_btn3_press
        self.screens = []
        for module in SCREENS:
            self.screens.append(importlib.import_module("screens." + module))

    def loop(self):
        loop = 1
        while True:
            if loop == 1:
                self.screens[self.current_screen].print_to_display()
            if loop == TIME:
                loop = 0
            time.sleep(1)
            loop += 1


app = App()
app.loop()
