import time
import epd
import importlib
import logging
import posix_ipc
import asyncio

import settings
from settings import TIME, SCREENS, DEBUG, LOGFILE
from libs.calendar import Calendar, get_calendar
from libs.weather import Weather, get_weather


def handle_btn0_press():
    app.handle_btn0_press()


def handle_btn1_press():
    app.handle_btn1_press()


def handle_btn2_press():
    app.handle_btn2_press()


def handle_btn3_press():
    app.handle_btn3_press()


class App:
    current_screen_index: int = 0
    screen_modules: list = []
    screens: list = []
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()
    async_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop_time: int = 0

    def current_screen(self):
        return self.screens[self.current_screen_index]

    def current_screen_module(self):
        return self.screen_modules[self.current_screen_index]

    def handle_btn0_press(self):
        if settings.PAGE_BUTTONS:
            if self.current_screen_index > 0:
                self.current_screen_index -= 1
            else:
                self.current_screen_index = len(self.screens) - 1
            logging.debug("Current screen: {0}".format(self.current_screen().__module__))
            self.current_screen().show()
        else:
            logging.debug("Screen '{0}' handling button 0".format(self.current_screen().__module__))
            self.current_screen().handle_btn_press(button_number=0)

    def handle_btn1_press(self):
        logging.debug("Screen '{0}' handling button 1".format(self.current_screen().__module__))
        self.current_screen().handle_btn_press(button_number=1)

    def handle_btn2_press(self):
        logging.debug("Screen '{0}' handling button 2".format(self.current_screen().__module__))
        self.current_screen().handle_btn_press(button_number=2)

    def handle_btn3_press(self):
        if settings.PAGE_BUTTONS:
            self.current_screen_index += 1
            if self.current_screen_index >= len(self.screens):
                self.current_screen_index = 0
            logging.debug("Current screen: {0}".format(self.current_screen().__module__))
            self.current_screen().show()
        else:
            logging.debug("Screen '{0}' handling button 3".format(self.current_screen().__module__))
            self.current_screen().handle_btn_press(button_number=3)

    def add_screen(self, screen_name):
        screen_module = importlib.import_module("screens." + screen_name)
        self.screens.append(screen_module.Screen())
        self.screen_modules.append(screen_module)

    def find_screen_index_by_name(self, screen_name):
        for index in range(0, len(self.screens)):
            name = self.screens[index].__module__
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

    def get_screen_module_by_name(self, screen_name):
        index = self.find_screen_index_by_name(screen_name)
        if index >= 0:
            return self.screen_modules[index]
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

        self.calendar.get_latest_events()
        self.async_loop.run_until_complete(self.weather.update())

        epd.clear_screen()

        btns = epd.get_buttons()
        btns[0].when_pressed = handle_btn0_press
        btns[1].when_pressed = handle_btn1_press
        btns[2].when_pressed = handle_btn2_press
        btns[3].when_pressed = handle_btn3_press

        for module in SCREENS:
            self.add_screen(module)

    def process_message(self):
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
                self.current_screen().reload()
                self.current_screen().show()
            elif command == "screen":
                logging.debug("Attempting switch to screen '{0}'".format(parts[1]))
                self.current_screen_index = self.find_screen_index_by_name(parts[1])
                if self.current_screen_index < 0:
                    logging.error("Couldn't find screen '{0}'".format(parts[1]))
                    self.current_screen_index = 0
            elif command == "remove_screen":
                logging.debug("Attempting to remove screen '{0}'".format(parts[1]))
                if self.current_screen_index == self.find_screen_index_by_name(parts[1]):
                    self.current_screen_index = 0
                    self.current_screen().reload()
                self.screens.remove(self.get_screen_by_name(parts[1]))
                self.screen_modules.remove(self.get_screen_module_by_name(parts[1]))

            elif command == "add_screen":
                logging.debug("Attempting to add screen '{0}'".format(parts[1]))
                if self.get_screen_by_name(parts[1]):
                    logging.error("Screen '{0}' already added".format(parts[1]))
                else:
                    self.add_screen(parts[1])

            else:
                logging.error("Command '{0}' not recognized".format(command))

    def update_weather(self):
        self.weather.refresh_interval = settings.WEATHER_REFRESH
        self.async_loop.run_until_complete(self.weather.update())

    def update_calendar(self):
        self.calendar.refresh_interval = settings.CALENDAR_REFRESH
        self.calendar.get_latest_events()

    def loop(self):
        while True:
            self.process_message()

            for screen in self.screens:
                screen.iterate_loop()

            self.calendar.refresh_interval -= 1
            if self.calendar.refresh_interval <= 0:
                self.update_calendar()

            self.weather.refresh_interval -= 1
            if self.weather.refresh_interval < 0:
                self.update_weather()

            time.sleep(1)

            if self.loop_time == TIME:
                self.loop_time = 0

            self.loop_time += 1

            if self.loop_time == 1:
                self.current_screen().show()


app = App()
app.loop()
