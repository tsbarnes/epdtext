import epd
from screens import AbstractScreen
from libs.calendar import Calendar, get_calendar
from libs.weather import Weather, get_weather


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()
    weather: Weather = get_weather()

    def reload(self):
        self.blank()

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=50)

    def handle_btn_press(self, button_number=1):
        pass
