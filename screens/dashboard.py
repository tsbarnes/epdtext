import logging
from PIL import Image

import settings
from screens import AbstractScreen
from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()

        logo = self.weather.get_icon()
        self.image.paste(logo, (20, 20))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=48, position=(60, 5))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=14, position=(150, 20))

        start = self.calendar.standardize_date(self.calendar.events[0]["start"])
        text = self.calendar.humanized_datetime(start)
        self.text(text, font_size=16, position=(5, 60))

        text = str(self.calendar.events[0]['summary'])
        self.text(text, font_size=14, position=(5, 80))

    def handle_btn_press(self, button_number=1):
        if button_number == 0:
            pass
        elif button_number == 1:
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
