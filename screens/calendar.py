import epd
import humanize
import textwrap
import caldav
import logging
from datetime import date, datetime, timedelta
from icalevents.icalevents import events
from settings import CALENDAR_URLS


def sort_by_date(obj):
    return obj["start"]


def get_events_from_webcal(url):
    objects = []
    try:
        timeline = events(url)
        for event in timeline:
            start = event.start
            summary = event.summary

            if isinstance(start, date):
                start = datetime.combine(start, datetime.min.time())

            objects.append({'start': start, 'summary': summary})
    except ValueError:
        logging.error('Error reading calendar "{0}"'.format(url))
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
            start = event.vobject_instance.vevent.dtstart.value
            summary = event.vobject_instance.vevent.summary.value

            if isinstance(start, date):
                start = datetime.combine(start, datetime.min.time())

            objects.append({
                'start': start,
                'summary': summary
            })

    return objects


def get_latest_events():
    logging.debug("Started reading calendars...")
    objects = []

    for connection in CALENDAR_URLS:
        if str(connection["type"]).lower() == 'webcal':
            objects.extend(get_events_from_webcal(connection["url"]))
        elif str(connection['type']).lower() == 'caldav':
            objects.extend(get_events_from_caldav(connection["url"],
                                                  connection["username"], connection["password"]))
        else:
            logging.error("calendar type not recognized: {0}".format(str(connection["type"])))

    objects.sort(key=sort_by_date)

    logging.debug("done!")
    return objects


def print_to_display():
    epd.print_to_display('Loading calendars...', fontsize=25)
    text = ''

    objects = get_latest_events()
    for obj in objects:
        text += '\t' + humanize.naturalday(obj["start"]) + '\n'
        summary = obj["summary"].replace('\n', ' ')
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
