import time
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont,ImageOps
import sys
import os
import bluetooth
import logging
import subprocess

def open_bluetooth_server_socket():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "00001101-0000-1000-8000-00805F9B34FB"  # Replace "your-uuid-here" with your service's UUID
    print("Trying to connect")
    try:
        bluetooth.advertise_service(server_sock, "SampleServer",
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
    except Exception as e:
        print("ERROR: " + repr(e))


    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received: %s" % data)
            messages = preProcessText(data.decode())
            for message in messages:
                process = subprocess.Popen(['python3', 'test.py', f'{message}'])
                time.sleep(10)
                process.terminate()
                
    except IOError:
        pass
    except KeyboardInterrupt:
        print("Server is closing.")
    finally:
        client_sock.close()
        server_sock.close()

def preProcessText(text):
    words = text.split(",")
    words = [word.strip("_*").strip() for word in words if word.strip("_*").strip()]
    return words


def main():
    
    print("HIIIII")
    subprocess.Popen(['python3', 'test.py', 'NO Starting'])
    #display_text("YO Starting")
    #display_text("NO Starting")
    print("Starting")
    try:
        print("Connecting")
        #display_text("Connecting")
        open_bluetooth_server_socket()
        #display_text("Connected")
    except:
        print("Error:" + sys.exc_info()[0])
        #display_text("Error")   
    
    
    #display_text("Wierd")


if __name__ == "__main__":
    main()