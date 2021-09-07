import time
import epd
from datetime import timedelta


def print_to_display():
    ms = time.clock_gettime(time.CLOCK_BOOTTIME)
    td = timedelta(microseconds=ms)
    string = str(td)
    epd.print_to_display(string)


def handle_btn_press():
    print_to_display()
