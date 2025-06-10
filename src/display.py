from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont, ImageOps
import time
import logging
from enum import Enum
from functools import wraps

logging.basicConfig(level=logging.DEBUG)

class DisplayState(Enum):
    READY = 0
    BUSY = 1
    TURNED_OFF = 2

def processing(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.get_state() is DisplayState.BUSY:
            logging.warning("Device is busy")
            return False
        self._set_state(DisplayState.BUSY)
        try:
            res = method(self, *args, **kwargs)
        finally:
            self._set_state(DisplayState.READY)
        return res
    return wrapper

class EInkDisplay:

    def __init__(self):
        self._state = DisplayState.TURNED_OFF
        self.epd = None
        pass

    def get_state(self) -> DisplayState:
        return self._state

    def _set_state(self, state: DisplayState):
        self._state = state

    @processing
    def init(self) -> bool:
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
        return True

    @processing
    def clear(self) -> bool:
        if self.epd is None:
            logging.error("EPD not initialized")
            return False
        self.epd.Clear()
        return True


    @processing
    def show_image(self, image_path) -> bool:
        self.clear()
        self.epd.init_fast()
        # Open image and convert to grayscale
        image = Image.open(image_path).convert("L")  # "L" mode = 8-bit grayscale

        # Resize while maintaining aspect ratio
        image = ImageOps.fit(image, (self.epd.width, self.epd.height), Image.LANCZOS)

        # Convert to black & white using dithering (better contrast for E Ink)
        image = image.convert("1", dither=Image.FLOYDSTEINBERG)

        # Display image
        self.epd.display(self.epd.getbuffer(image))

        self.sleep()
        return True

    def sleep(self):
        time.sleep(2)

    def close(self) -> bool:
        epd7in5_V2.epdconfig.module_exit(cleanup=True)
        self._set_state(DisplayState.TURNED_OFF)
        return True
