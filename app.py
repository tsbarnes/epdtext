import time
import epd
import importlib
import logging
import posix_ipc

from settings import TIME, SCREENS, DEBUG, LOGFILE


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
    screens = []

    def handle_btn0_press(self):
        if self.current_screen > 0:
            self.current_screen -= 1
        else:
            self.current_screen = len(self.screens) - 1
        logging.debug("Current screen: {0}".format(self.current_screen))
        self.screens[self.current_screen].print_to_display()

    def handle_btn1_press(self):
        logging.debug("Screen '{0}' handling button 1".format(self.current_screen))
        self.screens[self.current_screen].handle_btn_press(button_number=1)

    def handle_btn2_press(self):
        logging.debug("Screen '{0}' handling button 2".format(self.current_screen))
        self.screens[self.current_screen].handle_btn_press(button_number=2)

    def handle_btn3_press(self):
        self.current_screen += 1
        if self.current_screen >= len(self.screens):
            self.current_screen = 0
        logging.debug("Current screen: {0}".format(self.current_screen))
        self.screens[self.current_screen].print_to_display()

    def __init__(self):
        self.mq = posix_ipc.MessageQueue("/epdtext_ipc", flags=posix_ipc.O_CREAT)
        self.mq.block = False

        epd.clear_screen()
        btns = epd.get_buttons()
        btns[0].when_pressed = handle_btn0_press
        btns[1].when_pressed = handle_btn1_press
        btns[2].when_pressed = handle_btn2_press
        btns[3].when_pressed = handle_btn3_press

        for module in SCREENS:
            self.screens.append(importlib.import_module("screens." + module))

    def loop(self):
        loop = 1
        while True:
            try:
                message = self.mq.receive(timeout=10)
            except posix_ipc.BusyError:
                message = None

            if message:
                parts = message[0].decode().split()

                command = parts[0]
                logging.debug("Received IPC command: " + command)
                if command == "previous" or command == "button0":
                    self.handle_btn0_press()
                elif command == "next" or command == "button3":
                    self.handle_btn3_press()
                elif command == "button1":
                    self.handle_btn1_press()
                elif command == "button2":
                    self.handle_btn2_press()
                elif command == "reload":
                    loop = 0
                elif command == "screen":
                    logging.debug("Attempting switch to screen '{0}'".format(parts[1]))
                    was_set = False
                    for index in range(0, len(self.screens)):
                        if self.screens[index].__name__.split('.')[1] == parts[1]:
                            self.current_screen = index
                            was_set = True
                    if not was_set:
                        logging.error("Screen '{0}' doesn't exist".format(parts[1]))
                else:
                    logging.error("Command '{0}' not recognized".format(command))

            time.sleep(1)

            if loop == TIME:
                loop = 0

            loop += 1

            if loop == 1:
                self.screens[self.current_screen].print_to_display()


if DEBUG:
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)

app = App()
app.loop()
