import importlib
import time
import logging
import threading

from PIL import Image
from gpiozero import Button

from settings import DRIVER

try:
    driver = importlib.import_module("waveshare_epd." + DRIVER)
except ImportError:
    logging.error("Driver '{0}' couldn't be loaded".format(DRIVER))
    raise ImportError("Couldn't load driver")

logger = logging.getLogger("epdtext.libs.epd")


class EPD(threading.Thread):
    """
    This class provides threaded access to the e-paper display
    """
    epd: driver.EPD = driver.EPD()
    dirty: bool = False
    image: Image = Image.new("1", (driver.EPD_HEIGHT, driver.EPD_WIDTH), 255)
    thread_lock = threading.Lock()

    def __init__(self):
        """
        Initialize the display and image buffer
        """
        super().__init__()
        self.image = Image.new("1", self.get_size(), 255)
        self.epd.init()  # initialize the display
        self.buttons = [Button(5), Button(6), Button(13), Button(19)]
        self.name = "EPD"

    def run(self):
        """
        Creates and starts the thread process, don't call this directly.
        Instead use EPD.start(), which will call this method on it's own.
        """
        self.epd.Clear()
        thread_process = threading.Thread(target=self.process_epd)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()

    def process_epd(self):
        """
        Main display loop, handled in a separate thread
        """
        while True:
            time.sleep(1)
            if self.dirty and self.image:
                self.dirty = False
                logger.debug("Writing image to display")
                red_image = Image.new("1", get_size(), 255)
                self.epd.display(self.epd.getbuffer(self.image), self.epd.getbuffer(red_image))

    def show(self, image: Image):
        """
        Draws an image to the image buffer
        :param image: image to be displayed
        """
        logger.debug("Image sent to EPD")
        self.image = image
        self.dirty = True

    def get_size(self):
        """
        Get EPD size
        :return: tuple of height and width
        """
        return driver.EPD_HEIGHT, driver.EPD_WIDTH


epd = EPD()


def get_epd():
    """
    Get the EPD instance
    :return: EPD instance
    """
    return epd


def get_size():
    """
    Get the EPD size
    :return: tuple of height and width
    """
    return driver.EPD_HEIGHT, driver.EPD_WIDTH


def get_buttons():
    """
    Gets the buttons from the EPD
    :return: list of buttons
    """
    return epd.buttons
