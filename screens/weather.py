import logging

from libs.weather import Weather, get_weather, update_weather
from screens import AbstractScreen


class Screen(AbstractScreen):
    weather: Weather = get_weather()

    def handle_btn_press(self, button_number: int = 1):
        if button_number == 0:
            pass
        elif button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            update_weather()
            self.reload()
            self.show()
        elif button_number == 3:
            pass
        else:
            logging.error("Unknown button pressed: KEY{}".format(button_number + 1))

    def reload(self):
        self.blank()
        logo = self.weather.get_icon()
        self.image.paste(logo, (30, 40))

        text = str(self.weather.weather.current.temperature) + '°'
        self.centered_text(text, 10, 60)

        text = str(self.weather.weather.current.sky_text)
        self.centered_text(text, 70, 30)

        text = str(self.weather.weather.location_name)
        self.centered_text(text, 100, 20)

        logging.debug("Sky Code: " + str(self.weather.weather.current.sky_code))
