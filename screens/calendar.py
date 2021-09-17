import logging

from libs.calendar import Calendar, get_calendar, update_calendar
from screens import AbstractScreen


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()

    def reload(self):
        self.blank()

        if len(self.calendar.events) < 1:
            self.text('No current events', font_size=25)
            return

        current_line = 0
        for event in self.calendar.events:
            text = self.calendar.humanized_datetime(event["start"])
            current_line += self.text(text, (5, 5 + current_line * 20), font_size=15, wrap=False)
            text = event["summary"].strip('\n')
            current_line += self.text(text, (5, 5 + current_line * 20), font_size=15)

    def handle_btn_press(self, button_number=1):
        if button_number == 0:
            pass
        elif button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            update_calendar()
            self.reload()
            self.show()
        elif button_number == 3:
            pass
        else:
            logging.error("Unknown button pressed: KEY{}".format(button_number + 1))
