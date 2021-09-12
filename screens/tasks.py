from requests.exceptions import SSLError

import humanize
import caldav
import logging
from datetime import date, datetime
from settings import CALENDAR_URLS, CALENDAR_REFRESH
from screens import AbstractScreen


def sort_by_date(obj):
    if obj["due"]:
        return obj["due"]
    return datetime(4000, 1, 1)


class Tasks:
    tasks = []
    refresh_interval = 0

    def get_tasks_from_caldav(self, url, username, password):
        try:
            client = caldav.DAVClient(url=url, username=username, password=password)
            principal = client.principal()
        except SSLError:
            logging.error("SSL error loading calendar: " + url)
            return self.tasks

        calendars = principal.calendars()

        for calendar in calendars:
            todos = calendar.todos()

            for todo in todos:
                try:
                    due = todo.vobject_instance.vtodo.due.value
                except AttributeError:
                    due = None
                summary = todo.vobject_instance.vtodo.summary.value

                if isinstance(due, date):
                    due = datetime.combine(due, datetime.min.time())

                self.tasks.append({
                    'due': due,
                    'summary': summary
                })

        return self.tasks

    def get_current_tasks(self):
        logging.debug("Started reading tasks...")
        self.tasks = []

        for connection in CALENDAR_URLS:
            if str(connection['type']).lower() == 'caldav':
                self.get_tasks_from_caldav(connection["url"],
                                           connection["username"], connection["password"])
            elif str(connection['type']).lower() == 'webcal':
                logging.debug("calendar type doesn't support tasks")
            else:
                logging.error("calendar type not recognized: {0}".format(str(connection["type"])))

        self.tasks.sort(key=sort_by_date)

        logging.debug("done!")
        return self.tasks


class Screen(AbstractScreen):
    tasks = Tasks()

    def reload(self):
        self.blank()

        text = ''

        for obj in self.tasks.tasks:
            text += "* " + obj["summary"].replace('\n', ' ') + '\n'
            if obj["due"]:
                text += "  - Due: " + humanize.naturalday(obj["due"]) + "\n"

        if text != '':
            self.text(text, font_size=16)
        else:
            self.text('No tasks', font_size=30)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            self.iterate_loop(force_update=True)
            self.show()

    def iterate_loop(self, force_update=False):
        self.tasks.refresh_interval -= 1

        if self.tasks.refresh_interval <= 0 or force_update:
            self.tasks.refresh_interval = CALENDAR_REFRESH
            self.tasks.get_current_tasks()
            self.reload()
