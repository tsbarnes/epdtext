import threading
import time
import python_weather
import asyncio
import logging
import settings
from PIL import Image


class Weather(threading.Thread):
    """
    This class provides access to the weather info
    """
    weather = None
    refresh_interval: int = settings.WEATHER_REFRESH
    loop = asyncio.get_event_loop()

    def __init__(self):
        super().__init__()
        self.name = "Weather"

    def run(self) -> None:
        thread_process = threading.Thread(target=self.weather_loop)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()

    def weather_loop(self):
        while True:
            self.refresh_interval -= 1
            time.sleep(1)
            if self.refresh_interval < 1:
                self.loop.run_until_complete(self.update())
                self.refresh_interval = settings.WEATHER_REFRESH

    async def update(self):
        """
        Update the weather info
        :return: None
        """
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()

    def get_icon(self):
        """
        Get the icon for the current weather
        :return: Image of the icon
        """
        # TODO: this function should check the sky code and choose the icon accordingly
        # For now it just uses the sun icon for all weather
        if self.weather.current.sky_code == 0:
            return Image.open("images/sun.png")
        elif self.weather.current.sky_code == 26:
            return Image.open("images/cloud.png")
        elif self.weather.current.sky_code == 28:
            return Image.open("images/cloud.png")
        elif self.weather.current.sky_code == 30:
            return Image.open("images/cloud_sun.png")
        else:
            logging.debug("Unable to find icon for sky code: {}".format(self.weather.current.sky_code))
            return Image.open("images/sun.png")


weather: Weather = Weather()


def get_weather():
    """
    Get the main weather object
    :return: Weather
    """
    return weather


def update_weather():
    """
    Update the weather info
    :return: None
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(weather.update())
