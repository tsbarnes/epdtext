import epd
import textwrap
import caldav
import logging
from datetime import date, datetime
from settings import CALENDAR_URLS


def sort_by_date(obj):
    return obj["due"]


def get_tasks_from_caldav(url, username, password):
    objects = []

    client = caldav.DAVClient(url=url, username=username, password=password)
    principal = client.principal()
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

            objects.append({
                'due': due,
                'summary': summary
            })

    return objects


def get_current_tasks():
    logging.debug("Started reading tasks...")
    objects = []

    for connection in CALENDAR_URLS:
        if str(connection['type']).lower() == 'caldav':
            objects.extend(get_tasks_from_caldav(connection["url"],
                                                 connection["username"], connection["password"]))
        elif str(connection['type']).lower() == 'webcal':
            logging.debug("calendar type doesn't support tasks")
        else:
            logging.error("calendar type not recognized: {0}".format(str(connection["type"])))

    objects.sort(key=sort_by_date)

    logging.debug("done!")
    return objects


def print_to_display():
    epd.print_to_display('Loading tasks...', fontsize=25)
    text = ''

    objects = get_current_tasks()
    for obj in objects:
        summary = obj["summary"].replace('\n', ' ')
        lines = textwrap.wrap(summary, width=28)
        for line in lines:
            text += line + '\n'

    if text != '':
        epd.print_to_display(text, fontsize=16)
    else:
        epd.print_to_display('No tasks', fontsize=30)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
