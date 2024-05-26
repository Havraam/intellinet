import socket
from threading import Thread
from zlib import compress

from mss import mss
import ctypes

# Set process to be DPI aware
windll = ctypes.windll
user32 = windll.user32
user32.SetProcessDPIAware(1)

# Now use GetSystemMetrics
WIDTH = user32.GetSystemMetrics(0)
HEIGHT = user32.GetSystemMetrics(1)



def retreive_screenshot(conn):
    with mss() as sct:
        try:
            # The region to capture
            rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

            while 'recording':
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 6)

                # Send the size of the pixels length
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                conn.send(bytes([size_len]))

                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                conn.send(size_bytes)

                # Send pixels
                conn.sendall(pixels)
        except ConnectionAbortedError:
            print("connection closed")


def main(host=fr'{socket.gethostname()}.local', port=5000):    
    print(socket.gethostname())
    sock = socket.socket()
    sock.bind((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            resolution = fr"{WIDTH},{HEIGHT}"
            conn.send (resolution.encode())
            thread = Thread(target=retreive_screenshot, args=(conn,))
            thread.start()
            thread.join()
    

    finally:
        sock.close()


if __name__ == '__main__':
    main()
