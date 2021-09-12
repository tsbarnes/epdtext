import logging
from PIL import Image
from waveshare_epd.epd2in7b import EPD
from epd import get_epd, get_size
from utils import get_screens


class AbstractScreen:
    display: EPD = get_epd()
    image: Image = None
    reload_interval: int = 60
    reload_wait: int = 0

    def __init__(self):
        self.image = Image.new("RGBA", get_size(), 0)
        self.reload()

    def blank(self):
        self.image = Image.new("RGBA", get_size(), 0)

    def show(self):
        red_image = Image.new("1", get_size(), 0)
        self.display.display(self.image, red_image)

    def reload(self):
        raise NotImplementedError()

    def handle_btn_press(self):
        raise NotImplementedError()

    def iterate_loop(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_screens()
