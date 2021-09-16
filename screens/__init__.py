import logging
import uuid
from string import ascii_letters
from PIL import Image, ImageDraw, ImageFont
from epd import EPD, get_epd, get_size
from utils import get_screens
import textwrap
import settings


class AbstractScreen:
    """
    Abstract screen class, screens should inherit from this
    """
    display: EPD = get_epd()
    image: Image = None
    filename: str = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self):
        """
        This method creates the image for the screen and sets up the class
        """
        self.filename = "/tmp/{0}_{1}.png".format(self.__module__, str(uuid.uuid4()))
        self.blank()
        self.reload()

    def blank(self):
        """
        This method clears the image by recreating it
        """
        self.image = Image.new("1", get_size(), 255)

    def show(self):
        """
        This method copies the image to the display
        """
        if not self.image:
            logging.error("show() called with no image defined!")
            return

        if settings.SAVE_SCREENSHOTS:
            self.image.save(self.filename)

        self.display.show(self.image)

    def reload(self):
        """
        This method redraws the contents of the image
        """
        raise NotImplementedError()

    def handle_btn_press(self, button_number=1):
        """
        This method handles the button presses.
        Buttons 0 and 3 are generally used to switch screens, while buttons 1 and 2 are passed
        to this method. If there's only one screen, or if you set the "NO_WRAP_TEXT" setting to True
        :param button_number: default is 1
        """
        raise NotImplementedError()

    def iterate_loop(self):
        """
        Called once per cycle (roughly every one second). If you need to do something in the main loop,
        do it here. Make sure to call super().iterate_loop() if you override this.
        :return: None
        """
        self.reload_wait += 1
        if self.reload_wait >= self.reload_interval:
            self.reload_wait = 0
            self.reload()

    def paste(self, image: Image, position: tuple = (0, 0)):
        """
        Paste an image onto the buffer
        :param image: Image to paste
        :param position: tuple position to paste at
        :return: None
        """
        self.image.paste(image, position)

    def line(self, position: tuple, fill: any, width: int):
        """
        Draw a line onto the buffer
        :param position: tuple position to draw line
        :param fill: color to fill line with
        :param width: width of line
        :return: None
        """
        draw = ImageDraw.Draw(self.image)
        draw.line(position, fill, width)

    def text(self, text: str, font_name: str = settings.FONT, font_size: int = 20, position: tuple = (5, 5), color: any = "black"):
        """
        Draws text onto the buffer
        :param text: str text to display
        :param font_name: str font filename
        :param font_size: int font size
        :param position: tuple position to draw text
        :param color: color to draw text
        :return: None
        """
        wrapped_text = ''
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font_name, font_size)

        avg_char_width: int = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count: int = int((self.image.size[0] * .95) / avg_char_width)
        logging.debug("Size: {0} x {1}, font size: {2}, line wrap: {3}".format(get_size()[0], get_size()[1],
                                                                               font_size, max_char_count))

        for text_line in str(text).split('\n'):
            lines = textwrap.wrap(text_line, width=max_char_count)
            for line in lines:
                wrapped_text += line + '\n'

        draw.text(position, wrapped_text, font=font, fill=color)

    def centered_text(self, text: str, y: int, font_size: int = 20):
        """
        Draws text centered horizontally
        :param text: str text to be displayed
        :param y: vertical starting position
        :param font_size: size of font
        :return: None
        """
        font = ImageFont.truetype(settings.FONT, font_size)
        avg_char_width: int = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        centered_position = (self.image.size[0] / 2) - (avg_char_width * len(text) / 2)
        self.text(text, font_size=font_size, position=(centered_position, y))


# When run as main, this module gets the available screens and exits
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_screens()
