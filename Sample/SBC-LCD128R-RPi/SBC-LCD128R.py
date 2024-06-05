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

    # Create circle outline
    draw.arc((1,1,239,239),0, 360, fill =(39,92,107))

    # Create outer lines
    draw.line([(120, 1),(120, 12)], fill = (39,92,107),width = 4)
    draw.line([(120, 227),(120, 239)], fill = (39,92,107),width = 4)
    draw.line([(1,120),(12,120)], fill = (39,92,107),width = 4)
    draw.line([(227,120),(239,120)], fill = (39,92,107),width = 4)

    # Reference font file and draw text
    Font = ImageFont.truetype("SourceSansPro.ttf",35)
    draw.text((70, 50), 'Joy-IT', fill = (39,92,107),font=Font)
    
    # Create lines
    draw.line([(120, 120),(70, 70)], fill = (255,255,255),width = 7)
    draw.line([(120, 120),(176, 64)], fill = (255,255,255),width = 5)
    draw.line([(120, 120),(120 ,210)], fill = (255,255,255),width = 3)   
 
    disp.ShowImage(image1)
    time.sleep(5)
    image = Image.open('SampleImage.jpg')	
    disp.ShowImage(image)
    time.sleep(5)
    disp.module_exit()
except KeyboardInterrupt:
    disp.module_exit()
    exit()