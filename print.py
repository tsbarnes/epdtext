import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

from waveshare_epd import epd2in7b

from PIL import Image, ImageDraw, ImageFont


def printToDisplay(string):
    HBlackImage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    HRedImage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(HBlackImage) # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30) # Create our font, passing in the font file and font size
    draw.text((25, 65), string, font = font, fill = 0)
    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))


epd = epd2in7b.EPD() # get the display
epd.init()           # initialize the display

printToDisplay('TODO: Affirmations') # TODO: Affirmations
