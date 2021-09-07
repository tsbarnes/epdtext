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
