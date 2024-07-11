import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys
import bluetooth
import logging





def log_error(error_message):
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            logging.error(error_message)

def display_text(text):

    # Set up
    fontSize=35

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
        Font = ImageFont.truetype("SourceSansPro.ttf", fontSize)
        draw.text((70, 50), ' '.join(text), fill = (255,255,255),font = Font)  # Change fill color to white
        image1 = ImageOps.mirror(image1)
        disp.ShowImage(image1)
        time.sleep(10)
        exit()
    except KeyboardInterrupt:
        disp.module_exit()
        exit()



def main():
    display_text(sys.argv[1:])

if __name__ == "__main__":
    main()