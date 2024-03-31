import threading
from PIL import ImageGrab
import socket
import io
import base64
import PIL.Image as Image 



serverAddressPort = ("127.0.0.1", 20001)

bufferSize = 65535


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def send_image(packet_number, packet_data):
    try:
        UDPClientSocket.sendto(packet_number + packet_data, serverAddressPort)
    except Exception as e:
        print(f"Error sending data: {e}")






for i in range(200):
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer , format= "JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    packet_size = 32768 
    num_packets = (len(img_str) // packet_size) + 1

    for i in range(num_packets - 1):
        packet_number = str(i).zfill(4).encode()
        packet_data = img_str[i * packet_size: (i + 1) * packet_size]

        threading.Thread(target=send_image, args=(packet_number, packet_data)).start()

    UDPClientSocket.sendto(b'LAST' + img_str[(num_packets - 1) * packet_size:], serverAddressPort)







