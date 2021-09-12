import logging
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd.epd2in7b import EPD
from epd import get_epd, get_size
from utils import get_screens
import textwrap
import settings


class AbstractScreen:
    display: EPD = get_epd()
    image: Image = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self):
        self.image = Image.new("1", get_size(), 0)
        self.reload()

    def blank(self):
        self.image = Image.new("1", get_size(), 0)

    def show(self):
        red_image = Image.new("1", get_size(), 0)
        self.display.display(self.image, red_image)

    def reload(self):
        raise NotImplementedError()

    def handle_btn_press(self):
        raise NotImplementedError()

    def iterate_loop(self):
        self.reload_wait += 1
        if self.reload_wait >= self.reload_interval:
            self.reload_wait = 0
            self.reload()

    def text(self, text, font=settings.FONT, font_size=20, position=(5, 5), color="black"):
        wrapped_text = ''
        line_width = (get_size()[1] / (font_size / 2.5))
        logging.debug("Size: {0} x {1}, font size: {2}, line wrap: {3}".format(get_size()[0], get_size()[1],
                                                                               font_size, line_width))
        for text_line in text.split('\n'):
            lines = textwrap.wrap(text_line, width=line_width)
            for line in lines:
                wrapped_text += line + '\n'

        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font, font_size)
        draw.text(position, wrapped_text, font=font, fill=color)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_screens()
