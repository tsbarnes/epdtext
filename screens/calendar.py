import epd
import humanize
from icalevents.icalevents import events
from icalendar import Event
from settings import CALENDAR_URLS


def get_latest_event():
    text = ''

    for CALENDAR_URL in CALENDAR_URLS:
        try:
            timeline = events(CALENDAR_URL)
            event: Event
            for event in timeline:
                text += humanize.naturalday(event.start) + '\n'
                text += event.summary.replace('\n', ' ') + '\n'
        except ValueError:
            print('Error reading calendar "{0}"'.format(CALENDAR_URL))
            pass

    return text


def print_to_display():
    text = get_latest_event()
    if text != '':
        epd.print_to_display(text, fontsize=16)
    else:
        epd.print_to_display('No current\nevents', fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
