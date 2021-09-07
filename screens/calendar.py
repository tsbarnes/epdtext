import epd
import humanize
import textwrap
import caldav
from datetime import datetime
from icalevents.icalevents import events
from icalendar import Event
from settings import CALENDAR_URLS


def get_events_from_webcal(url):
    text = ''

    try:
        timeline = events(url)
        event: Event
        for event in timeline:
            text += '\t' + humanize.naturalday(event.start) + '\n'
            summary = event.summary.replace('\n', ' ')
            lines = textwrap.wrap(summary, width=28)
            for line in lines:
                text += line + '\n'
    except ValueError:
        print('Error reading calendar "{0}"'.format(url))
        pass

    return text


def get_events_from_caldav(url, username, password):
    text = ''

    client = caldav.DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()

    for calendar in calendars:
        calendar_events = calendar.date_search(start=datetime.today(), end=datetime.today(), expand=True)
        for event in calendar_events:
            text += '\t' + humanize.naturalday(event.start) + '\n'
            summary = event.summary.replace('\n', ' ')
            lines = textwrap.wrap(summary, width=28)
            for line in lines:
                text += line + '\n'

    return text


def get_latest_events():
    print("Started reading calendars...")
    text = ''

    for connection in CALENDAR_URLS:
        if str(connection["type"]).lower() == 'webcal':
            text += get_events_from_webcal(connection["url"])
        elif str(connection.type).lower() == 'caldav':
            text += get_events_from_caldav(connection["url"], connection["username"], connection["password"])

    print("done!")
    return text


def print_to_display():
    text = get_latest_events()
    if text != '':
        epd.print_to_display(text, fontsize=16)
    else:
        epd.print_to_display('No current\nevents', fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
