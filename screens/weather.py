from screens import AbstractScreen
from libs.weather import Weather, get_weather
from PIL import Image
import settings
import logging
import asyncio


class Screen(AbstractScreen):
    weather: Weather = get_weather()
    async_loop = asyncio.get_event_loop()

    def handle_btn_press(self, button_number: int = 1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            self.async_loop.run_until_complete(self.weather.update())
            self.reload()
            self.show()

    def reload(self):
        self.blank()
        logo = Image.open(settings.LOGO)  # TODO: replace with weather images
        self.image.paste(logo, (20, 30))

        centered_position: int = round(self.image.size[0] / 2 - 60)

        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=60, position=(centered_position, 10))

        text = str(self.weather.weather.current.sky_text)
        self.text(text, font_size=30, position=(centered_position, 70))

        text = str(self.weather.weather.location_name)
        self.text(text, font_size=20, position=(centered_position, 100))

        logging.debug("Sky Code: " + str(self.weather.weather.current.sky_code))
