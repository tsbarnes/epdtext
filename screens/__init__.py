import logging
from string import ascii_letters

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd.epd2in7b import EPD
from epd import get_epd, get_size
from utils import get_screens
import textwrap
import settings


class AbstractScreen:
    """Abstract screen class, screens should inherit from this"""
    display: EPD = get_epd()
    image: Image = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self):
        self.image = Image.new("1", get_size(), 255)
        self.reload()

    def blank(self):
        self.image = Image.new("1", get_size(), 255)

    def show(self):
        if self.image:
            red_image = Image.new("1", get_size(), 255)
            self.display.display(self.display.getbuffer(self.image), self.display.getbuffer(red_image))

    def reload(self):
        raise NotImplementedError()

    def handle_btn_press(self):
        raise NotImplementedError()

    def iterate_loop(self):
        self.reload_wait += 1
        if self.reload_wait >= self.reload_interval:
            self.reload_wait = 0
            self.reload()

    def text(self, text, font_name=settings.FONT, font_size=20, position=(5, 5), color="black"):
        wrapped_text = ''
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font_name, font_size)

        avg_char_width: int = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count: int = int((self.image.size[0] * .95) / avg_char_width)
        logging.debug("Size: {0} x {1}, font size: {2}, line wrap: {3}".format(get_size()[0], get_size()[1],
                                                                               font_size, max_char_count))

        for text_line in text.split('\n'):
            lines = textwrap.wrap(text_line, width=max_char_count)
            for line in lines:
                wrapped_text += line + '\n'

        draw.text(position, wrapped_text, font=font, fill=color)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_screens()
