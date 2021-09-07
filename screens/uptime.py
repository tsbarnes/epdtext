import time
import datetime
import epd
import humanize


def print_to_display():
    string = '\tSystem Uptime:\n'
    string += humanize.naturaldelta(datetime.timedelta(seconds=time.clock_gettime(time.CLOCK_BOOTTIME)))
    epd.print_to_display(string, fontsize=20)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
