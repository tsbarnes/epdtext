import logging

from libs.calendar import Calendar, get_calendar, update_calendar
from libs.weather import Weather, get_weather, update_weather
from screens import AbstractScreen


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

        self.line((0, 60, self.image.size[0], 60), width=1)

        if len(self.calendar.events) > 0:
            start = self.calendar.standardize_date(self.calendar.events[0]["start"])
            text = self.calendar.humanized_datetime(start)
            self.text(text, font_size=16, position=(5, 65))

            text = str(self.calendar.events[0]['summary'])
            self.text(text, font_size=14, position=(5, 85), max_lines=2)

        self.line((0, 120, self.image.size[0], 120), width=1)

        if len(self.calendar.tasks) > 0:
            text = str(self.calendar.tasks[0]['summary'])
            self.text(text, font_size=14, position=(5, 125), max_lines=2)

            if self.calendar.tasks[0].get('due'):
                text = self.calendar.humanized_datetime(self.calendar.tasks[0]['due'])
                self.text(text, font_size=14, position=(5, 160), max_lines=1)

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
