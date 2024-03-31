import PIL
import socket
import os
import io
from array import array
import PIL.Image as Image 
import base64
import threading 

 

localIP = "127.0.0.1"
localPort = 20001


msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
recieved_data = b""
img_counter = 0
print("UDP server up and listening")


while True:
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(65507)
        data = bytesAddressPair[0]
        address = bytesAddressPair[1]
    except Exception as e:
        print(f"Error: {e}")

    packet_number, packet_data = data[:4], data[4:]

    if packet_number == b'LAST':

        try:
            img_counter += 1   
            b = base64.b64decode(recieved_data + packet_data)
            clientImg = Image.open(io.BytesIO(b))
            clientImg = clientImg.save(fr"screenshots\{img_counter}.jpeg", format='JPEG')
        except Exception as e:
            print(f"Error decoding image data: {e}")
        finally:
            recieved_data = b""

    else:
        recieved_data += packet_data



    


