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
    current_screen_index = 0
    screens = []

    def current_screen(self):
        return self.screens[self.current_screen_index]

    def handle_btn0_press(self):
        if self.current_screen_index > 0:
            self.current_screen_index -= 1
        else:
            self.current_screen_index = len(self.screens) - 1
        logging.debug("Current screen: {0}".format(self.current_screen().__name__))
        self.current_screen().print_to_display()

    def handle_btn1_press(self):
        logging.debug("Screen '{0}' handling button 1".format(self.current_screen_index))
        self.current_screen().handle_btn_press(button_number=1)

    def handle_btn2_press(self):
        logging.debug("Screen '{0}' handling button 2".format(self.current_screen_index))
        self.current_screen().handle_btn_press(button_number=2)

    def handle_btn3_press(self):
        self.current_screen_index += 1
        if self.current_screen_index >= len(self.screens):
            self.current_screen_index = 0
        logging.debug("Current screen: {0}".format(self.current_screen_index))
        self.current_screen().print_to_display()

    def add_screen(self, screen_name):
        screen = importlib.import_module("screens." + screen_name)
        self.screens.append(screen)

    def find_screen_index_by_name(self, screen_name):
        for index in range(0, len(self.screens)):
            name = self.screens[index].__name__
            if name == screen_name or name.split('.')[-1] == screen_name:
                return index
        logging.error("Screen '{0}' doesn't exist".format(screen_name))
        return -1

    def get_screen_by_name(self, screen_name):
        index = self.find_screen_index_by_name(screen_name)
        if index >= 0:
            return self.screens[index]
        else:
            logging.error("Screen '{0}' not found".format(screen_name))
            return None

    def __init__(self):
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG, filename=LOGFILE)
            logging.info("Debug messages enabled")
        else:
            logging.basicConfig(filename=LOGFILE)

        logging.info("Starting epdtext...")

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
        loop = 0
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
                    self.current_screen_index = self.find_screen_index_by_name(parts[1])
                    if self.current_screen_index < 0:
                        self.current_screen_index = 0
                    loop = 0
                elif command == "remove_screen":
                    logging.debug("Attempting to remove screen '{0}'".format(parts[1]))
                    if self.current_screen_index == self.find_screen_index_by_name(parts[1]):
                        self.current_screen_index = 0
                        self.screens[self.current_screen_index].print_to_display()
                    self.screens.remove(self.get_screen_by_name(parts[1]))

                elif command == "add_screen":
                    logging.debug("Attempting to add screen '{0}'".format(parts[1]))
                    if self.get_screen_by_name(parts[1]):
                        logging.error("Screen '{0}' already added".format(parts[1]))
                    else:
                        self.add_screen(parts[1])

                else:
                    logging.error("Command '{0}' not recognized".format(command))

            time.sleep(1)

            if loop == TIME:
                loop = 0

            loop += 1

            if loop == 1:
                self.current_screen().print_to_display()


app = App()
app.loop()
