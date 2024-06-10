import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont



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
    draw.text((70, 50), 'AR-Brille', fill = (255,255,255),font=Font)  # Change fill color to white
    
    disp.ShowImage(image1)
    time.sleep(50000)
except KeyboardInterrupt:
    disp.module_exit()
    exit()