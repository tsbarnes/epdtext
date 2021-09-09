import epd
import humanize
import caldav
import logging
import pytz
from datetime import date, datetime, timedelta
from icalevents.icalevents import events
from settings import CALENDAR_URLS, TIMEZONE


def sort_by_date(obj):
    return obj["start"]


class Calendar:
    timezone = pytz.timezone(TIMEZONE)

    def standardize_date(self, arg, ignore_timezone=False):
        if isinstance(arg, datetime) and (not arg.tzinfo or ignore_timezone):
            return datetime.combine(arg.date(), arg.time(), self.timezone)
        elif isinstance(arg, date) and not isinstance(arg, datetime):
            logging.debug("Object has no time")
            return datetime.combine(arg, datetime.min.time(), self.timezone)
        else:
            return arg

    def get_events_from_webcal(self, url):
        objects = []
        try:
            timeline = events(url)
            for event in timeline:
                start = self.standardize_date(event.start)
                summary = event.summary

                objects.append({'start': start, 'summary': summary})
        except ValueError:
            logging.error('Error reading calendar "{0}"'.format(url))
            pass

        return objects

    def get_events_from_caldav(self, url, username, password):
        objects = []

        client = caldav.DAVClient(url=url, username=username, password=password)
        principal = client.principal()
        calendars = principal.calendars()

        for cal in calendars:
            calendar_events = cal.date_search(start=datetime.today(),
                                              end=datetime.today() + timedelta(days=7),
                                              expand=True)
            for event in calendar_events:
                start = self.standardize_date(event.vobject_instance.vevent.dtstart.value)
                summary = event.vobject_instance.vevent.summary.value

                objects.append({
                    'start': start,
                    'summary': summary
                })

        return objects

    def get_latest_events(self):
        logging.debug("Started reading calendars...")
        objects = []

        for connection in CALENDAR_URLS:
            if str(connection["type"]).lower() == 'webcal':
                objects.extend(self.get_events_from_webcal(connection["url"]))
            elif str(connection['type']).lower() == 'caldav':
                objects.extend(self.get_events_from_caldav(connection["url"],
                                                           connection["username"], connection["password"]))
            else:
                logging.error("calendar type not recognized: {0}".format(str(connection["type"])))

        objects.sort(key=sort_by_date)

        logging.debug("done!")
        return objects

    def __str__(self):
        text = ''

        objects = calendar.get_latest_events()
        for obj in objects:
            if obj["start"].date() > datetime.today().date():
                text += '* ' + humanize.naturaldate(obj["start"]) + '\n'
            else:
                text += '* ' + humanize.naturaltime(obj["start"], when=datetime.now(self.timezone)) + '\n'

            text += obj["summary"].replace('\n', ' ') + '\n'

        return text


calendar = Calendar()


def print_to_display():
    epd.print_to_display('Loading calendars...', fontsize=25)
    text = str(calendar)

    if text != '':
        epd.print_to_display(text, fontsize=16)
    else:
        epd.print_to_display('No current\nevents', fontsize=25)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
