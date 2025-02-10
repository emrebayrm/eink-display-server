from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageOps

class EInkDisplay:
    def __init__(self):
        self.epd = epd7in5b_V2.EPD()
        self.epd.init()

    def clear(self):
        self.epd.Clear()

    def show_image(self, image_path):
        # Open image and convert to grayscale
        image = Image.open(image_path).convert("L")  # "L" mode = 8-bit grayscale

        # Resize while maintaining aspect ratio
        image = ImageOps.fit(image, (self.epd.width, self.epd.height), Image.LANCZOS)

        # Convert to black & white using dithering (better contrast for E Ink)
        image = image.convert("1", dither=Image.FLOYDSTEINBERG)

        # Display image
        self.epd.display(self.epd.getbuffer(image))

    def sleep(self):
        self.epd.sleep()
