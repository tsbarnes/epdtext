import humanize
from screens import AbstractScreen
from libs.calendar import Calendar, get_calendar


class Screen(AbstractScreen):
    calendar: Calendar = get_calendar()

    def reload(self):
        self.blank()

        text = ''

        for obj in self.calendar.tasks:
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
            self.show()
