import epd
from icalevents.icalevents import events
from settings import CALENDAR_URL


def get_latest_event():
    timeline = events(CALENDAR_URL)
    text = ''
    for event in timeline:
        text += event.summary + '\n'

    return text


def print_to_display():
    text = get_latest_event()
    if text != '':
        epd.print_to_display(text, fontsize=20)
    else:
        epd.print_to_display('No current\nevents', fontsize=30)


def handle_btn_press():
    print_to_display()
