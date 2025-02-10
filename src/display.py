from waveshare_epd import epd7in5b_V2
from PIL import Image

class EInkDisplay:
    def __init__(self):
        self.epd = epd7in5b_V2.EPD()
        self.epd.init()

    def clear(self):
        self.epd.Clear()

    def show_image(self, image_path):
        image = Image.open(image_path).convert("1")  # Convert to black & white
        self.epd.display(self.epd.getbuffer(image))

    def sleep(self):
        self.epd.sleep()
