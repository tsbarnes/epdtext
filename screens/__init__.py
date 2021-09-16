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

    def line(self, position: tuple, fill: any = "black", width: int = 5):
        """
        Draw a line onto the buffer
        :param position: tuple position to draw line
        :param fill: color to fill line with
        :param width: width of line
        :return: None
        """
        draw = ImageDraw.Draw(self.image)
        draw.line(position, fill, width)

    def text(self, text, position=(5, 5), font_name=None, font_size=20, color="black", wrap=True, max_lines=None):
        """
        Draws text onto the app's image
        :param text: string to draw
        :param position: tuple representing where to draw the text
        :param font_name: filename of font to use, None for default
        :param font_size: integer font size to draw
        :param color: color of the text
        :param wrap: boolean whether to wrap the text
        :param max_lines: number of lines to draw maximum
        :return: integer number of lines drawn
        """
        if not font_name:
            font_name = settings.FONT
        if not self.image:
            raise ValueError("self.image is None")

        font: ImageFont = ImageFont.truetype(font_name, font_size)
        draw: ImageDraw = ImageDraw.Draw(self.image)
        number_of_lines: int = 0
        scaled_wrapped_text: str = ''

        if wrap:
            avg_char_width: int = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count: int = int((self.image.size[0] * .95) / avg_char_width)

            for line in text.split('\n'):
                new_wrapped_text = textwrap.fill(text=line, width=max_char_count) + '\n'
                for wrapped_line in new_wrapped_text.split('\n'):
                    if not max_lines or number_of_lines < max_lines:
                        number_of_lines += 1
                        scaled_wrapped_text += wrapped_line + '\n'
        else:
            for line in text.split('\n'):
                if not max_lines or number_of_lines < max_lines:
                    number_of_lines += 1
                    scaled_wrapped_text += line + '\n'

        draw.text(position, scaled_wrapped_text, font=font, fill=color)

        return number_of_lines

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
        number_of_lines = 0
        for line in text.split('\n'):
            centered_position = (self.image.size[0] / 2) - (avg_char_width * len(line) / 2)
            position = (centered_position, y + (number_of_lines * font_size))
            self.text(text, font_size=font_size, position=position, wrap=False)
            number_of_lines += 1

        return number_of_lines


# When run as main, this module gets the available screens and exits
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_screens()
