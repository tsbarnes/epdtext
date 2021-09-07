import time
import epd


def print_to_display():
    string = time.clock_gettime(time.CLOCK_BOOTTIME).__str__()
    epd.print_to_display(string)


def handle_btn_press():
    print_to_display()
