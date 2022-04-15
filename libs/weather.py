import threading
import time
import python_weather
import asyncio
import xml
import logging
from PIL import Image


try:
    from local_settings import WEATHER_FORMAT
except ImportError:
    WEATHER_FORMAT = python_weather.IMPERIAL

try:
    from local_settings import WEATHER_CITY
except ImportError:
    WEATHER_CITY = "Richmond, VA"

try:
    from local_settings import WEATHER_REFRESH
except ImportError:
    WEATHER_REFRESH = 900


logger = logging.getLogger("pitftmanager.libs.weather")


class Weather(threading.Thread):
    """
    This class provides access to the weather info
    """
    weather = None
    refresh_interval: int = WEATHER_REFRESH
    loop = asyncio.get_event_loop()

    def __init__(self):
        super().__init__()
        self.name = "Weather"
        self.shutdown = threading.Event()

    def run(self) -> None:
        thread_process = threading.Thread(target=self.weather_loop)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()
        self.shutdown.wait()

    def weather_loop(self):
        while not self.shutdown.is_set():
            self.refresh_interval -= 1
            time.sleep(1)
            if self.refresh_interval < 1:
                try:
                    self.loop.run_until_complete(self.update())
                except xml.parsers.expat.ExpatError as error:
                    logger.warning(error)
                self.refresh_interval = WEATHER_REFRESH

    def stop(self):
        self.shutdown.set()

    async def update(self):
        """
        Update the weather info
        :return: None
        """
        self.thread_lock.acquire()
        client = python_weather.Client(format=WEATHER_FORMAT)
        self.weather = await client.find(WEATHER_CITY)
        await client.close()
        self.thread_lock.release()

    def get_temperature(self):
        """
        Get the temperature
        :return: String of the temperature
        """
        if not self.weather:
            return "--"

        return self.weather.current.temperature

    def get_sky_code(self):
        """
        Get the sky code
        :return: String of the sky code
        """
        if not self.weather:
            return 0

        return self.weather.current.sky_code

    def get_sky_text(self):
        """
        Get the sky text
        :return: String of the sky text
        """
        if not self.weather:
            return "--"

        return self.weather.current.sky_text

    def get_location_name(self):
        """
        Get the location name
        :return: String of the location name
        """
        if not self.weather:
            return "--"

        return self.weather.location_name

    def get_icon(self):
        """
        Get the icon for the current weather
        :return: Image of the icon
        """
        if not self.weather:
            return Image.open("images/sun.png")

        if self.weather.current.sky_code == 0:
            image = Image.open("images/sun.png")
            return image.resize((32, 32))
        elif self.weather.current.sky_code == 26:
            image = Image.open("images/cloud.png")
            return image.resize((32, 32))
        elif self.weather.current.sky_code == 28:
            image = Image.open("images/cloud.png")
            return image.resize((32, 32))
        elif self.weather.current.sky_code == 30:
            image = Image.open("images/cloud_sun.png")
            return image.resize((32, 32))
        elif self.weather.current.sky_code == 32:
            image = Image.open("images/sun.png")
            return image.resize((32, 32))
        else:
            logger.warning("Unable to find icon for sky code: {}".format(self.weather.current.sky_code))
            image = Image.open("images/sun.png")
            return image.resize((32, 32))


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    update_weather()
    logger.info(weather.weather.current.sky_text)
