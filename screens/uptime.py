import time
import epd
import humanreadable


def print_to_display():
    tm = humanreadable.Time(str(time.clock_gettime(time.CLOCK_BOOTTIME)) + ' seconds')
    days = int(tm.days)
    hours = int(tm.hours) - (days * 24)
    minutes = int(tm.minutes) - (days * 24 * 60) - (hours * 60)
    string = "{0} days\n{1} hours\n{2} minutes".format(days, hours, minutes)
    epd.print_to_display(string)


def handle_btn_press():
    print_to_display()
