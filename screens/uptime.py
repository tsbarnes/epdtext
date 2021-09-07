import time
import epd
import humanreadable


def print_to_display():
    tm = humanreadable.Time(str(time.clock_gettime(time.CLOCK_BOOTTIME)) + ' seconds')
    string = "{0} days\n{1} hours\n{2} minutes".format(round(tm.days), round(tm.hours), round(tm.minutes))
    epd.print_to_display(string)


def handle_btn_press():
    print_to_display()
