import logging
from datetime import date, datetime, timedelta

import caldav
import humanize
import pytz
from icalevents.icalevents import events
from requests.exceptions import SSLError

import settings
from settings import CALENDAR_URLS, TIMEZONE

timezone = pytz.timezone(TIMEZONE)


def sort_by_date(obj: dict):
    """
    Sort the events or tasks by date
    :param obj: dict containing sumary and start/due date
    :return: the same object, with time added if needed
    """
    if obj.get("start"):
        if isinstance(obj["start"], date) and not isinstance(obj["start"], datetime):
            return datetime.combine(obj["start"], datetime.min.time(), timezone)
        if not obj["start"].tzinfo:
            return timezone.localize(obj["start"])
        return obj["start"]
    elif obj.get("due"):
        if not obj["due"]:
            return datetime.fromisocalendar(4000, 1, 1)
        if isinstance(obj["due"], date) and not isinstance(obj["due"], datetime):
            return datetime.combine(obj["due"], datetime.min.time(), timezone)
        if not obj["due"].tzinfo:
            return timezone.localize(obj["due"])
        return obj["due"]
    else:
        raise ValueError("Object has no start or due date")


class Calendar:
    """
    This class handles the calendar events and tasks
    """
    timezone = None
    refresh_interval: int = settings.CALENDAR_REFRESH
    events: list = []
    tasks: list = []

    def __init__(self):
        """
        Initialize the timezone
        """
        self.timezone = pytz.timezone(TIMEZONE)

    def standardize_date(self, arg):
        """
        Adds time to dates to make datetimes as needed
        :param arg: an object containing a summary and date
        :return: a new datetime object, or the same object if no changes were needed
        """
        if isinstance(arg, datetime) and not arg.tzinfo:
            logging.debug("Object has no timezone")
            return self.timezone.localize(arg)
        elif isinstance(arg, date) and not isinstance(arg, datetime):
            logging.debug("Object has no time")
            return datetime.combine(arg, datetime.min.time(), self.timezone)
        else:
            return arg

    def get_events_from_webcal(self, url):
        """
        Retrieve events from webcal and append them to the list
        :param url: the URL of the webcal
        :return: list of events
        """
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
        """
        Retrieve events and tasks from CalDAV
        :param url: URL of CalDAV server
        :param username: CalDAV user name
        :param password: CalDAV password
        :return: the list of events
        """
        try:
            client = caldav.DAVClient(url=url, username=username, password=password)
            principal = client.principal()
        except SSLError:
            logging.error("SSL error connecting to CalDAV server")
            return self.events

        calendars = principal.calendars()

        for cal in calendars:
            calendar_events = cal.date_search(start=datetime.today(),
                                              end=datetime.today() + timedelta(days=7),
                                              expand=True)
            for event in calendar_events:
                start = self.standardize_date(event.vobject_instance.vevent.dtstart.value)
                summary = event.vobject_instance.vevent.summary.value

                self.events.append({
                    'start': start,
                    'summary': summary
                })

            todos = cal.todos()

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
        """
        Force update of events
        :return:
        """
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
        """
        Get the current events as a string
        :return: list of events
        """
        text = ''

        for obj in self.events:
            text += self.humanized_datetime(obj["start"]) + '\n'
            text += obj["summary"].replace('\n', ' ') + '\n'

        return text

    def tasks_as_string(self):
        """
        Get the current tasks as a string
        :return: list of tasks
        """
        text = ''

        for obj in self.tasks:
            text += "* " + obj["summary"].replace('\n', ' ') + '\n'
            if obj["due"]:
                text += "  - Due: " + self.humanized_datetime(obj["due"]) + "\n"

        return text

    def humanized_datetime(self, dt: datetime):
        """
        Get a human-readable interpretation of a datetime
        :param dt: datetime to humanize
        :return: str
        """
        try:
            obj = self.timezone.localize(dt)
        except ValueError:
            obj = dt
        return '-- ' + humanize.naturaltime(obj, when=datetime.now(self.timezone)) + ' --'


calendar = Calendar()


def get_calendar():
    """
    Retrieve main Calendar object
    :return: Calendar
    """
    return calendar


def update_calendar():
    """
    Update calendar events and tasks
    :return: None
    """
    calendar.get_latest_events()
