import time
import epd
import humanreadable


def print_to_display():
    string = humanreadable.Time(time.clock_gettime(time.CLOCK_BOOTTIME))
    epd.print_to_display(string)


def handle_btn_press():
    print_to_display()
