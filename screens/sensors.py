"""Sensors screen"""
from libs import system
from screens import AbstractScreen


class Screen(AbstractScreen):
    """
    This class provides the screen methods needed by epdtext
    """
    system = system.get_system()

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

        text = "Temperature:\t" + str(round(self.system.temperature)) + '°\n'
        text += "Voltage:   \t" + str(self.system.voltage)
        self.text(text, font_size=16, position=(5, 30))

    def iterate_loop(self):
        """
        This method is optional, and will be run once per cycle
        """
        # Do whatever you need to do, but try to make sure it doesn't take too long

        # This line is very important, it keeps the auto reload working
        super().iterate_loop()
