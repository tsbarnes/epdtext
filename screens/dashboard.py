import logging
from PIL import Image

import settings
from screens import AbstractScreen
from libs.calendar import Calendar, get_calendar
from libs.weather import Weather, get_weather


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()

        logo = Image.open(settings.LOGO)  # TODO: replace with weather images
        self.image.paste(logo, (10, 10))

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=48, position=(60, 5))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=14, position=(150, 20))

        text = str(self.calendar.events[0]['summary'])
        self.text(text, font_size=14, position=(5, 60))

    def handle_btn_press(self, button_number=1):
        if button_number == 0:
            pass
        elif button_number == 1:
            self.calendar.get_latest_events()
            self.weather.update()
            self.reload()
            self.show()
        elif button_number == 2:
            pass
        elif button_number == 3:
            pass
        else:
            logging.error("Unknown button pressed: KEY{}".format(button_number + 1))
