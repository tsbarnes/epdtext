import humanize
import caldav
import logging
import pytz
from datetime import date, datetime, timedelta, tzinfo
from icalevents.icalevents import events
from requests.exceptions import SSLError

from settings import CALENDAR_URLS, TIMEZONE


def sort_by_date(obj: dict):
    if isinstance(obj["start"], date) and not isinstance(obj["start"], datetime):
        return datetime.combine(obj["start"], datetime.min.time())
    return obj["start"]


class Calendar:
    timezone: tzinfo = None
    refresh_interval: int = 0
    events: list = []
    tasks: list = []

    def __init__(self):
        if isinstance(TIMEZONE, tzinfo):
            self.timezone = TIMEZONE
        else:
            self.timezone = pytz.timezone(TIMEZONE)

    def standardize_date(self, arg, ignore_timezone=False):
        if isinstance(arg, datetime) and (not arg.tzinfo or ignore_timezone):
            return datetime.combine(arg.date(), arg.time(), self.timezone)
        elif isinstance(arg, date) and not isinstance(arg, datetime):
            logging.debug("Object has no time")
            return datetime.combine(arg, datetime.min.time(), self.timezone)
        else:
            return arg

    def get_events_from_webcal(self, url):
        try:
            timeline: list = events(url)
            for event in timeline:
                start = event.start
                summary = event.summary

                self.events.append({
                    'start': start,
                    'summary': summary
                })
        except ValueError:
            logging.error('Error reading calendar "{0}"'.format(url))
            pass

        return self.events

    def get_events_from_caldav(self, url, username, password):
        try:
            client = caldav.DAVClient(url=url, username=username, password=password)
            principal = client.principal()
        except SSLError:
            logging.error("SSL error connecting to CalDAV server")
            return self.events

        calendars = principal.calendars()

        for calendar in calendars:
            calendar_events = calendar.date_search(start=datetime.today(),
                                                   end=datetime.today() + timedelta(days=7),
                                                   expand=True)
            for event in calendar_events:
                start = self.standardize_date(event.vobject_instance.vevent.dtstart.value)
                summary = event.vobject_instance.vevent.summary.value

                self.events.append({
                    'start': start,
                    'summary': summary
                })

            todos = calendar.todos()

            for todo in todos:
                try:
                    due = self.standardize_date(todo.vobject_instance.vtodo.due.value)
                except AttributeError:
                    due = None

                summary = todo.vobject_instance.vtodo.summary.value

                self.tasks.append({
                    'due': due,
                    'summary': summary
                })

        return self.events

    def get_latest_events(self):
        logging.debug("Started reading calendars...")
        self.events = []
        self.tasks = []

        for connection in CALENDAR_URLS:
            if str(connection["type"]).lower() == 'webcal':
                self.get_events_from_webcal(connection["url"])
            elif str(connection['type']).lower() == 'caldav':
                self.get_events_from_caldav(connection["url"],
                                            connection["username"], connection["password"])
            else:
                logging.error("calendar type not recognized: {0}".format(str(connection["type"])))

        self.events.sort(key=sort_by_date)

        logging.debug("done!")

        return self.events

    def events_as_string(self):
        text = ''

        for obj in self.events:
            if obj["start"].date() > datetime.today().date():
                text += '-- ' + humanize.naturaldate(obj["start"]) + ' --\n'
            else:
                text += '-- ' + humanize.naturaltime(obj["start"], when=datetime.now(self.timezone)) + ' --\n'

            text += obj["summary"].replace('\n', ' ') + '\n'

        return text

    def tasks_as_string(self):
        text = ''

        for obj in self.tasks:
            text += "* " + obj["summary"].replace('\n', ' ') + '\n'
            if obj["due"]:
                text += "  - Due: " + humanize.naturalday(obj["due"]) + "\n"

        return text


calendar = Calendar()


def get_calendar():
    return calendar
