from screens import AbstractScreen
import python_weather
import asyncio
from PIL import Image
import settings


class Weather:
    weather = None

    async def getweather(self):
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()


class Screen(AbstractScreen):
    weather = Weather()
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def __init__(self):
        self.loop.run_until_complete(self.weather.getweather())
        super().__init__()

    def handle_btn_press(self, button_number: int = 1):
        if button_number == 1:
            pass
        elif button_number == 2:
            pass

    def reload(self):
        self.blank()
        logo = Image.open(settings.LOGO)
        self.image.paste(logo, (100, 5))
        text = str(self.weather.weather.current.temperature) + '°'
        self.text(text, font_size=40, position=(10, 10))

    def iterate_loop(self):
        if self.reload_wait >= self.reload_interval:
            self.loop.run_until_complete(self.weather.getweather())

        super().iterate_loop()
