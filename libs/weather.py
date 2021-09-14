import python_weather
import settings


class Weather:
    weather = None
    refresh_interval: int = settings.WEATHER_REFRESH

    async def update(self):
        client = python_weather.Client(format=settings.WEATHER_FORMAT)
        self.weather = await client.find(settings.WEATHER_CITY)
        await client.close()


weather: Weather = Weather()


def get_weather():
    return weather


def update_weather():
    weather.update()
