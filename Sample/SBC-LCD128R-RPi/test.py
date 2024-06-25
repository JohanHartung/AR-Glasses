import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys
import bluetooth


def open_bluetooth_server_socket():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Bluetooth Server Socket Opened")
    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received: %s" % data)
    except IOError:
        pass
    except KeyboardInterrupt:
        print("Server is closing.")
    finally:
        client_sock.close()
        server_sock.close()


def display_text(text):
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
        draw.text((70, 50), ' '.join(text), fill = (255,255,255),font=Font)  # Change fill color to white

        image1 = ImageOps.mirror(image1)

        disp.ShowImage(image1)
        time.sleep(50000)
    except KeyboardInterrupt:
        disp.module_exit()
        exit()

def main():
    try:
        open_bluetooth_server_socket()
        display_text("Connected")
    except:
        display_text("Error")


    #display_text(sys.argv[1:])

if __name__ == "__main__":
    main()