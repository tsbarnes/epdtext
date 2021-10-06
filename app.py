import asyncio
import importlib
import logging
import signal
import time

import posix_ipc

import settings
from libs import epd
from libs.calendar import Calendar, get_calendar
from libs.epd import EPD, get_epd
from libs.weather import Weather, get_weather
from settings import TIME, SCREENS, DEBUG, LOGFILE


class App:
    logger = logging.getLogger("epdtext.app")
    current_screen_index: int = 0
    screen_modules: list = []
    screens: list = []
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()
    epd: EPD = get_epd()
    async_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop_time: int = 0

    def current_screen(self):
        return self.screens[self.current_screen_index]

    def current_screen_module(self):
        return self.screen_modules[self.current_screen_index]

    def previous_screen(self):
        if self.current_screen_index > 0:
            self.current_screen_index -= 1
        else:
            self.current_screen_index = len(self.screens) - 1
        self.logger.debug("Current screen: {0}".format(self.current_screen().__module__))
        self.current_screen().reload()
        self.current_screen().show()

    def next_screen(self):
        self.current_screen_index += 1
        if self.current_screen_index >= len(self.screens):
            self.current_screen_index = 0
        self.logger.debug("Current screen: {0}".format(self.current_screen().__module__))
        self.current_screen().reload()
        self.current_screen().show()

    def handle_btn0_press(self):
        if settings.PAGE_BUTTONS:
            self.previous_screen()
        else:
            self.logger.debug("Screen '{0}' handling button 0".format(self.current_screen().__module__))
            self.current_screen().handle_btn_press(button_number=0)

    def handle_btn1_press(self):
        self.logger.debug("Screen '{0}' handling button 1".format(self.current_screen().__module__))
        self.current_screen().handle_btn_press(button_number=1)

    def handle_btn2_press(self):
        self.logger.debug("Screen '{0}' handling button 2".format(self.current_screen().__module__))
        self.current_screen().handle_btn_press(button_number=2)

    def handle_btn3_press(self):
        if settings.PAGE_BUTTONS:
            self.next_screen()
        else:
            self.logger.debug("Screen '{0}' handling button 3".format(self.current_screen().__module__))
            self.current_screen().handle_btn_press(button_number=3)

    def add_screen(self, screen_name):
        try:
            screen_module = importlib.import_module("screens." + screen_name)
        except ImportError:
            try:
                screen_module = importlib.import_module(screen_name)
            except ImportError:
                screen_module = None
        if screen_module:
            new_screen = screen_module.Screen()
            self.screens.append(new_screen)
            self.screen_modules.append(screen_module)
        else:
            self.logger.error("Failed to load app: {}".format(screen_name))

    def find_screen_index_by_name(self, screen_name):
        for index in range(0, len(self.screens)):
            name = self.screens[index].__module__
            if name == screen_name or name.split('.')[-1] == screen_name:
                return index
        self.logger.error("Screen '{0}' doesn't exist".format(screen_name))
        return -1

    def get_screen_by_name(self, screen_name):
        index = self.find_screen_index_by_name(screen_name)
        if index >= 0:
            return self.screens[index]
        else:
            self.logger.error("Screen '{0}' not found".format(screen_name))
            return None

    def get_screen_module_by_name(self, screen_name):
        index = self.find_screen_index_by_name(screen_name)
        if index >= 0:
            return self.screen_modules[index]
        else:
            self.logger.error("Screen '{0}' not found".format(screen_name))
            return None

    def __init__(self):
        if DEBUG:
            logging.basicConfig(level=logging.DEBUG, filename=LOGFILE)
            self.logger.info("Debug messages enabled")
        else:
            logging.basicConfig(filename=LOGFILE)

        self.logger.info("Starting epdtext...")
        self.logger.info("Timezone selected: {}".format(settings.TIMEZONE))

        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        self.epd.start()

        self.mq = posix_ipc.MessageQueue("/epdtext_ipc", flags=posix_ipc.O_CREAT)
        self.mq.block = False

        self.calendar.get_latest_events()
        self.calendar.start()
        self.async_loop.run_until_complete(self.weather.update())

        btns = epd.get_buttons()
        btns[0].when_pressed = self.handle_btn0_press
        btns[1].when_pressed = self.handle_btn1_press
        btns[2].when_pressed = self.handle_btn2_press
        btns[3].when_pressed = self.handle_btn3_press

        for module in SCREENS:
            self.add_screen(module)

    def shutdown(self, *args):
        self.logger.info("epdtext shutting down gracefully...")
        while len(self.screens) > 0:
            del self.screens[0]
        exit(0)

    def process_message(self):
        try:
            message = self.mq.receive(timeout=10)
        except posix_ipc.BusyError:
            message = None

        if message:
            parts = message[0].decode().split()

            command = parts[0]
            self.logger.debug("Received IPC command: " + command)
            if command == "button0":
                self.handle_btn0_press()
            elif command == "button3":
                self.handle_btn3_press()
            elif command == "button1":
                self.handle_btn1_press()
            elif command == "button2":
                self.handle_btn2_press()
            elif command == "previous":
                self.previous_screen()
            elif command == "next":
                self.next_screen()
            elif command == "reload":
                self.current_screen().reload()
                self.current_screen().show()
            elif command == "screen":
                self.logger.debug("Attempting switch to screen '{0}'".format(parts[1]))
                self.current_screen_index = self.find_screen_index_by_name(parts[1])
                if self.current_screen_index < 0:
                    self.logger.error("Couldn't find screen '{0}'".format(parts[1]))
                    self.current_screen_index = 0
                self.current_screen().reload()
                self.current_screen().show()
            elif command == "remove_screen":
                self.logger.debug("Attempting to remove screen '{0}'".format(parts[1]))
                if self.current_screen_index == self.find_screen_index_by_name(parts[1]):
                    self.current_screen_index = 0
                    self.current_screen().reload()
                self.screens.remove(self.get_screen_by_name(parts[1]))
                self.screen_modules.remove(self.get_screen_module_by_name(parts[1]))
            elif command == "add_screen":
                self.logger.debug("Attempting to add screen '{0}'".format(parts[1]))
                if self.get_screen_by_name(parts[1]):
                    self.logger.error("Screen '{0}' already added".format(parts[1]))
                else:
                    self.add_screen(parts[1])

            else:
                self.logger.error("Command '{0}' not recognized".format(command))

    def loop(self):
        while True:
            self.process_message()

            time.sleep(1)

            self.weather.refresh_interval -= 1
            if self.weather.refresh_interval < 1:
                asyncio.get_event_loop().run_until_complete(self.weather.update())
                self.weather.refresh_interval = settings.WEATHER_REFRESH

            self.current_screen().iterate_loop()

            if self.loop_time >= TIME:
                self.loop_time = 0

            self.loop_time += 1

            if self.loop_time == 1:
                self.current_screen().show()


if __name__ == '__main__':
    app = App()
    app.loop()
