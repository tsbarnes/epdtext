"""Example screen to show how to make them"""
from screens import AbstractScreen


# Example of how to include a user setting
try:
    from local_settings import HELLO
except ImportError:
    HELLO = "Hello World!"


class Example:
    """
    Just another class, feel free to make it do whatever you want
    """
    def foobar(self) -> str:
        """
        This method just returns some text, yours can do anything you want
        :return: str
        """
        return HELLO


class Screen(AbstractScreen):
    """
    This class provides the screen methods needed by epdtext
    """

    # Add an instance of our Example class
    example: Example = Example()

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

        # self.blank() resets self.image to a blank image
        self.blank()
        # self.draw_titlebar(str) creates the small title at the top of the screen
        self.draw_titlebar("Example")

        # self.text(text) draws the text to self.image
        # Optional parameters include font, font_size, position, and color
        self.text(self.example.foobar(), font_size=40, position=(50, 50))

    def iterate_loop(self):
        """
        This method is optional, and will be run once per cycle
        """
        # Do whatever you need to do, but try to make sure it doesn't take too long

        # This line is very important, it keeps the auto reload working
        super().iterate_loop()
