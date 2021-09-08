import epd
import humanize
import textwrap
import caldav
from datetime import datetime, timedelta
from icalevents.icalevents import events
from settings import CALENDAR_URLS


def sort_by_date(e):
    return e.start


def get_events_from_webcal(url):
    objects = []
    try:
        timeline = events(url)
        for event in timeline:
            objects.append(event)
    except ValueError:
        print('Error reading calendar "{0}"'.format(url))
        pass

    return objects


def get_events_from_caldav(url, username, password):
    objects = []

    client = caldav.DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()

    for calendar in calendars:
        calendar_events = calendar.date_search(start=datetime.today(), end=datetime.today() + timedelta(days=7),
                                               expand=True)
        for event in calendar_events:
            objects.append(event)

    return objects


def get_latest_events():
    print("Started reading calendars...")
    objects = []

    for connection in CALENDAR_URLS:
        if str(connection["type"]).lower() == 'webcal':
            objects.extend(get_events_from_webcal(connection["url"]))
        elif str(connection['type']).lower() == 'caldav':
            objects.extend(get_events_from_caldav(connection["url"],
                                                  connection["username"], connection["password"]))

    objects.sort(key=sort_by_date)

    print("done!")
    return objects


def print_to_display():
    epd.print_to_display('Loading calendars...', fontsize=25)
    text = ''

    objects = get_latest_events()
    for obj in objects:
        text += '\t' + humanize.naturalday(obj.start) + '\n'
        summary = obj.summary.replace('\n', ' ')
        lines = textwrap.wrap(summary, width=28)
        for line in lines:
            text += line + '\n'

    if text != '':
        epd.print_to_display(text, fontsize=16)
    else:
        epd.print_to_display('No current\nevents', fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
