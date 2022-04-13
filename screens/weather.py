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

        self.draw_titlebar("Weather")

        logo = self.weather.get_icon()
        self.image.paste(logo, (30, 60))

        if self.weather.weather:
            text = str(self.weather.get_temperature()) + '°'
            self.centered_text(text, 40, 60)

            text = str(self.weather.get_sky_text())
            self.centered_text(text, 105, 30)

            text = str(self.weather.get_location_name())
            self.centered_text(text, 140, 20)

            logging.debug("Sky Code: " + str(self.weather.get_sky_code()))
        else:
            self.centered_text("No data", 105, 30)
