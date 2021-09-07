try:
    from local_settings import FONT
except ImportError:
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

try:
    from local_settings import TIME
except ImportError:
    TIME = 1000

try:
    from local_settings import CALENDAR_URLS
except ImportError:
    CALENDAR_URLS = []

try:
    from local_settings import SCREENS
except ImportError:
    SCREENS = [
        'affirmations',
        # The calendar app is a work in progress!
        'calendar',
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
