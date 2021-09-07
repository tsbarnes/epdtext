import epd
from icalevents.icalevents import events
from settings import CALENDAR_URLS


def get_latest_event():
    text = ''

    for CALENDAR_URL in CALENDAR_URLS:
        timeline = events(CALENDAR_URL)
        for event in timeline:
            text += event.summary + '\n'

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
