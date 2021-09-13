from screens import AbstractScreen
import python_weather
import asyncio
from PIL import Image
import settings
import logging


class Weather:
    weather = None

    async def get_weather(self):
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()


class Screen(AbstractScreen):
    weather = Weather()
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def __init__(self):
        self.loop.run_until_complete(self.weather.get_weather())
        super().__init__()

    def handle_btn_press(self, button_number: int = 1):
        if button_number == 1:
            pass
        elif button_number == 2:
            pass

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

    def iterate_loop(self):
        if self.reload_wait >= self.reload_interval:
            self.loop.run_until_complete(self.weather.get_weather())

        super().iterate_loop()
