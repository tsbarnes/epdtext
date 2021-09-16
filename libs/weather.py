from PIL import Image

import python_weather
import settings


class Weather:
    """
    This class provides access to the weather info
    """
    weather = None
    refresh_interval: int = settings.WEATHER_REFRESH

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
        return Image.open("sun.png")


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
    weather.update()
