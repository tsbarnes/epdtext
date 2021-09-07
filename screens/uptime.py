import time
import epd
import humanreadable


def print_to_display():
    tm = humanreadable.Time(str(time.clock_gettime(time.CLOCK_BOOTTIME)) + ' seconds')
    days = int(tm.days)
    hours = int(tm.hours) % 24
    minutes = int(tm.minutes) % 60
    string = "{0} days\n{1} hours\n{2} minutes".format(days, hours, minutes)
    epd.print_to_display(string, fontsize=20)


def handle_btn_press(button_number=1):
    if button_number == 1:
        print_to_display()
    elif button_number == 2:
        pass
