## Author: Jordan Meidinger
## Date: Fall 2019
## Networking Class

import time
import bluetooth
## Import GPIO Library
import RPi.GPIO as GPIO

## Setup Pins
GPIO.setmode(GPIO.BOARD)
inputPin = 7
GPIO.setup(inputPin, GPIO.IN)

## Setup Socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

## How to read and write through bluetooth
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            #protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        if GPIO.input(inputPin)== 0:
            print("No Rider - 0")
            sendMessage = "0"
            client_sock.send(sendMessage)
        else:
            print("On Seat - 1")
            client_sock.send(sendMessage)
            sendMessage = "1"
        time.sleep(2)
        
except IOError:
    pass
finally:
    GPIO.cleanup()
    print("Disconnected.")
    client_sock.close()
    server_sock.close()
    print("All done.")
