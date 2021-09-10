from datetime import datetime


try:
    from local_settings import DEBUG
except ImportError:
    DEBUG = False

try:
    from local_settings import LOGFILE
except ImportError:
    LOGFILE = None

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
    TIMEZONE = datetime.now().astimezone().tzinfo

try:
    from local_settings import SCREENS
except ImportError:
    SCREENS = [
        'affirmations',
        'fortune',
        'uptime',
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
