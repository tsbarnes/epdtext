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
        'calendar',
        'fortune',
        'uptime',
    ]

try:
    from local_settings import AFFIRMATIONS
except ImportError:
    AFFIRMATIONS = [
        "You are\nenough",
        "You are loved",
        "You are safe",
        "Be yourself",
        "They can't\nhurt you\nanymore",
        "You are\nbeautiful",
        "You are\nstrong",
        "You have\ncome a\nlong way"
    ]
