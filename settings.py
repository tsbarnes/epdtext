from datetime import datetime

import tzlocal
import python_weather

try:
    from local_settings import DRIVER
except ImportError:
    DRIVER = "epd2in7b"

try:
    from local_settings import DEBUG
except ImportError:
    DEBUG = False

try:
    from local_settings import SAVE_SCREENSHOTS
except ImportError:
    SAVE_SCREENSHOTS = False

try:
    from local_settings import LOGFILE
except ImportError:
    LOGFILE = None

try:
    from local_settings import PAGE_BUTTONS
except ImportError:
    PAGE_BUTTONS = True

try:
    from local_settings import LOGO
except ImportError:
    LOGO = '/home/pi/epdtext/logo.png'

try:
    from local_settings import FONT
except ImportError:
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

try:
    from local_settings import TIME
except ImportError:
    TIME = 900

try:
    from local_settings import CALENDAR_URLS
except ImportError:
    CALENDAR_URLS = []

try:
    from local_settings import CALENDAR_REFRESH
except ImportError:
    CALENDAR_REFRESH = 900

try:
    from local_settings import TIMEZONE
except ImportError:
    TIMEZONE = tzlocal.get_localzone().key

try:
    from local_settings import SCREENS
except ImportError:
    SCREENS = [
        'uptime',
        'fortune',
        'affirmations',
    ]

try:
    from local_settings import AFFIRMATIONS
except ImportError:
    AFFIRMATIONS = [
        "You are enough",
        "You are loved",
        "You are safe",
        "Be yourself",
        "They can't hurt you anymore",
        "You are beautiful",
        "You are strong",
        "You have come a long way"
    ]

try:
    from local_settings import WEATHER_CITY
except ImportError:
    WEATHER_CITY = "Richmond, VA"

try:
    from local_settings import WEATHER_FORMAT
except ImportError:
    WEATHER_FORMAT = python_weather.IMPERIAL

try:
    from local_settings import WEATHER_REFRESH
except ImportError:
    WEATHER_REFRESH = 900
