from screens import AbstractScreen
from libs.calendar import Calendar, get_calendar
from app import get_app


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()

    def reload(self):
        self.blank()

        text = self.calendar.events_as_string()

        if text != '':
            self.text(text, font_size=16)
        else:
            self.text('No current\nevents', font_size=25)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            get_app().update_calendar()
            self.reload()
            self.show()
