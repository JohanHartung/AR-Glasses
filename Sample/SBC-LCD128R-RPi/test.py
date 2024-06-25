import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys
import bluetooth
import logging


def open_bluetooth_server_socket():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "00001101-0000-1000-8000-00805F9B34FB"  # Replace "your-uuid-here" with your service's UUID

    bluetooth.advertise_service(server_sock, "SampleServer",
                                service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

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


def log_error(error_message):
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            logging.error(error_message)

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
        log_error("An error occurred.")


    #display_text(sys.argv[1:])

if __name__ == "__main__":
    main()