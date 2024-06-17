import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys

def main():
    # Raspberry Pi pin configuration:
    RST = 27
    DC = 25
    BL = 18
    bus = 0 
    device = 0 
    try:
        # display with hardware SPI:
        disp = LCD_1inch28.LCD_1inch28()
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()

        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image1)

        # Reference font file and draw text
        Font = ImageFont.truetype("SourceSansPro.ttf",35)
        draw.text((70, 50), ' '.join(sys.argv[1:]), fill = (255,255,255),font=Font)  # Change fill color to white

        image1 = ImageOps.mirror(image1)

        disp.ShowImage(image1)
        time.sleep(50000)
    except KeyboardInterrupt:
        disp.module_exit()
        exit()

if __name__ == "__main__":
    main()