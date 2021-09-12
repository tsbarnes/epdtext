from requests.exceptions import SSLError
import humanize
import caldav
import logging
import pytz
from datetime import date, datetime, timedelta, tzinfo
from icalevents.icalevents import events
from settings import CALENDAR_URLS, TIMEZONE, CALENDAR_REFRESH
from screens import AbstractScreen


def sort_by_date(obj):
    return obj["start"]


class Calendar:
    timezone = None
    refresh_interval = 0
    events = []

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
            timeline = events(url)
            for event in timeline:
                start = self.standardize_date(event.start)
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
            logging.error("SSL error loading calendar: " + url)
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

        return self.events

    def get_latest_events(self):
        logging.debug("Started reading calendars...")
        self.events = []

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

    def as_string(self):
        text = ''

        for obj in self.events:
            if obj["start"].date() > datetime.today().date():
                text += '-- ' + humanize.naturaldate(obj["start"]) + ' --\n'
            else:
                text += '-- ' + humanize.naturaltime(obj["start"], when=datetime.now(self.timezone)) + ' --\n'

            text += obj["summary"].replace('\n', ' ') + '\n'

        return text

    def __str__(self):
        self.as_string()


class Screen(AbstractScreen):
    calendar = Calendar()

    def reload(self):
        self.blank()

        text = self.calendar.as_string()

        if text != '':
            self.text(text, font_size=16)
        else:
            self.text('No current\nevents', font_size=25)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            self.iterate_loop(force_update=True)
            self.show()

    def iterate_loop(self, force_update=False):
        self.calendar.refresh_interval -= 1
        if self.calendar.refresh_interval <= 0 or force_update:
            self.calendar.refresh_interval = CALENDAR_REFRESH
            self.calendar.get_latest_events()
            self.reload()
