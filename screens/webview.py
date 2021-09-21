from PIL import Image
from htmlwebshot import WebShot

from screens import AbstractScreen

try:
    from local_settings import WEBVIEW_URL
except ImportError:
    WEBVIEW_URL = "http://tsbarnes.com/"


class Screen(AbstractScreen):
    """
    This class provides the screen methods needed by epdtext
    """

    # Add an instance of our Example class
    webshot: WebShot = WebShot()

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
        size = self.display.get_size()
        self.image = Image.open(self.webshot.create_pic(url=WEBVIEW_URL, size=(size[1], size[0])))

    def iterate_loop(self):
        """
        This method is optional, and will be run once per cycle
        """
        # Do whatever you need to do, but try to make sure it doesn't take too long

        # This line is very important, it keeps the auto reload working
        super().iterate_loop()
