import logging
import threading

from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather
from screens import AbstractScreen


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()
        self.draw_titlebar("Dashboard")

        logo = self.weather.get_icon()
        self.image.paste(logo, (15, 30))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=35, position=(60, 25))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=14, position=(150, 35))

        self.line((0, 70, self.image.size[0], 70), width=1)

        if len(self.calendar.events) > 0:
            start = self.calendar.standardize_date(self.calendar.events[0]["start"])
            text = ' -- ' + self.calendar.humanized_datetime(start) + ' -- '
            self.text(text, font_size=16, position=(5, 75))

            text = str(self.calendar.events[0]['summary'])
            self.text(text, font_size=14, position=(5, 95), max_lines=2)
        else:
            text = "No calendar events"
            self.centered_text(text, font_size=14, y=85)

        self.line((0, 130, self.image.size[0], 130), width=1)

        if len(self.calendar.tasks) > 0:
            text = str(self.calendar.tasks[0]['summary'])
            self.text(text, font_size=14, position=(5, 135), max_lines=2)

            if self.calendar.tasks[0].get('due'):
                text = ' - Due: ' + self.calendar.humanized_datetime(self.calendar.tasks[0]['due'])
                self.text(text, font_size=14, position=(5, 170), max_lines=1)
        else:
            text = "No current tasks"
            self.centered_text(text, font_size=14, y=145)

    def handle_btn_press(self, button_number=1):
        thread_lock = threading.Lock()
        thread_lock.acquire()
        if button_number == 0:
            pass
        elif button_number == 1:
            self.blank()
            self.text("Please wait...", font_size=40)
            self.show()
            update_calendar()
            update_weather()
            self.reload()
            self.show()
        elif button_number == 2:
            pass
        elif button_number == 3:
            pass
        else:
            logging.error("Unknown button pressed: KEY{}".format(button_number + 1))
        thread_lock.release()
