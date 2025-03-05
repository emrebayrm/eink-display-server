from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont, ImageOps
import time
import logging

logging.basicConfig(level=logging.DEBUG)

class EInkDisplay:
    def __init__(self):
        pass

    def init(self):
        self.epd = epd7in5_V2.EPD()
        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear()
        self.sleep()
        font24 = ImageFont.truetype('static/Font.ttc', 24)

        logging.info("Drawing on the Horizontal image...")
        self.epd.init_fast()
        
        Himage = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), 'hello world', font = font24, fill = 0)
        draw.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
        draw.text((150, 0), u'微雪电子', font = font24, fill = 0)
        draw.line((20, 50, 70, 100), fill = 0)
        draw.line((70, 50, 20, 100), fill = 0)
        draw.rectangle((20, 50, 70, 100), outline = 0)
        draw.line((165, 50, 165, 100), fill = 0)
        draw.line((140, 75, 190, 75), fill = 0)
        draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
        draw.rectangle((80, 50, 130, 100), fill = 0)
        draw.chord((200, 50, 250, 100), 0, 360, fill = 0)

        self.epd.display(self.epd.getbuffer(Himage))
        self.sleep()

    def clear(self):
        self.epd.Clear()

    def show_image(self, image_path):
        self.clear()
        self.epd.init_fast()
        # Open image and convert to grayscale
        image = Image.open(image_path).convert("L")  # "L" mode = 8-bit grayscale
  #      image = Image.open(image_path)
        # Resize while maintaining aspect ratio
        image = ImageOps.fit(image, (self.epd.width, self.epd.height), Image.LANCZOS)

        # Convert to black & white using dithering (better contrast for E Ink)
        image = image.convert("1", dither=Image.FLOYDSTEINBERG)

        # Display image
        self.epd.display(self.epd.getbuffer(image))

        self.sleep()

    def sleep(self):
        time.sleep(2)

    def close(self):
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
