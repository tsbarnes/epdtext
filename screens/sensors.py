"""Sensors screen"""
import sensors

from screens import AbstractScreen


class Screen(AbstractScreen):
    """
    This class provides the screen methods needed by epdtext
    """

    def __init__(self):
        """
        Initialize sensors library
        """
        sensors.init()
        super().__init__()

    def handle_btn_press(self, button_number: int = 1):
        """
        This method receives the button presses
        """

        # Buttons 0 and 3 are used to switch screens
        if button_number == 1:
            pass
        elif button_number == 2:
            pass

    def reload(self):
        """
        This method should draw the contents of the screen to self.image
        """

        self.blank()

        self.draw_titlebar("Sensors")

        current_line = 0
        for chip in sensors.iter_detected_chips():
            current_line += self.text(chip.adapter_name, font_size=20, position=(5, 25 + current_line * 20))

            for feature in chip:
                line = "{}: {}".format(feature.label, feature.get_value())
                current_line += self.text(line, font_size=20, position=(5, 25 + current_line * 20))

    def iterate_loop(self):
        """
        This method is optional, and will be run once per cycle
        """
        # Do whatever you need to do, but try to make sure it doesn't take too long

        # This line is very important, it keeps the auto reload working
        super().iterate_loop()
