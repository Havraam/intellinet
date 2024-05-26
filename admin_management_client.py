import socket
from tkinter import Tk, Label, Entry, Button
import time
from ctypes import wintypes
import socket
from threading import *
import pywinauto
from zlib import compress
from mss import mss
import ctypes

class Screenshare:
# Set process to be DPI aware
    # Now use GetSystemMetrics
    def __init__(self) -> None:
        windll = ctypes.windll
        user32 = windll.user32
        user32.SetProcessDPIAware(1)
        self.WIDTH = user32.GetSystemMetrics(0)
        self.HEIGHT = user32.GetSystemMetrics(1)


    def retreive_screenshot(self,conn):
        with mss() as sct:
            try:
                # The region to capture
                rect = {'top': 0, 'left': 0, 'width': self.WIDTH, 'height': self.HEIGHT}

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


    def start_server(self,host=fr'{socket.gethostname()}.local', port=5000):    
        print(socket.gethostname())
        sock = socket.socket()
        sock.bind((host, port))
        try:
            sock.listen(5)
            print('Server started.')

            while 'connected':
                conn, addr = sock.accept()
                print('Client connected IP:', addr)
                resolution = fr"{self.WIDTH},{self.HEIGHT}"
                conn.send (resolution.encode())
                thread = Thread(target=self.retreive_screenshot, args=(conn,))
                thread.start()
                thread.join()
        

        finally:
            sock.close()


def get_computer_name():
    computer_name = entry.get()
    # Process the computer name here (e.g., store it)
    print(f"Admin computer name: {computer_name}")
    f = open("config.txt", "w")    
    sock = socket.socket()
    sock.connect((fr"{computer_name}.local",5003))
    message = ("ADMIN?").encode()
    sock.send(message)
    response = sock.recv(1024).decode() 
    if (response == "YES"):
        f.write(computer_name)
        message = ("OK").encode()
        sock.send(message)
        response = sock.recv(1024).decode()
        if(response == "NAME?"):
            message = (socket.gethostname()).encode()
            sock.send(message)
            print("admin verified and linked")
    
    setup_window.destroy()  # Close the setup_window after processing


def send_help_request():
    f = open("config.txt", "r")
    admin_addr=f.read()
    sock = socket.socket()
    sock.connect((fr"{admin_addr}.local",5003))
    com_name = socket.gethostname()
    request = (fr"{com_name}!HELPME").encode()
    sock.send(request)

def admin_setup():
    global setup_window
    global entry
    setup_window = Tk()
    setup_window.title("Admin Setup")

    welcome_message = Label(setup_window, text="Greetings friend !")
    welcome_message.pack()

    instruction_message = Label(setup_window, text="Please insert admin computer name:")
    instruction_message.pack()

    entry = Entry(setup_window)
    entry.pack()

    submit_button = Button(setup_window, text="Submit", command=get_computer_name)
    submit_button.pack()

    setup_window.mainloop()

def start_screensharing_server():
    screenshare = Screenshare()
    screenshare.start_server()



def start_blackout_server():    
    #setting up the blockinput variable
    BlockInput = ctypes.windll.user32.BlockInput
    #starting up the server
    sock = socket.socket()
    sock.bind((fr"{socket.gethostname()}.local",5002))
    sock.listen(5)
    print('Server started.')
    while 'connected':
        #client acceptance
        conn,addr = sock.accept()
        print("client connected IP:",addr)
        while (True):
            #endless loop to always recieve requests 
            request = conn.recv(1024).decode()
            #if request == BEB - begin blackout than --->
            if request == "BEB":
                #stop all currently playing media
                hllDll = ctypes.WinDLL("User32.dll")
                VK_STOPMEDIA = 0xB2
                hllDll.keybd_event(VK_STOPMEDIA,0,1,0)
                hllDll.keybd_event(VK_STOPMEDIA,0,2,0)
                #press winkey+d to minimize to desktop
                pywinauto.keyboard.send_keys("{VK_LWIN down}d{VK_LWIN up}")
                #completley block all input until told otherwise
                blocked = BlockInput(True)
                if blocked:
                    blackout = True
                    try:
                        #while loop that runs as long as STB - stop blackout request hasnt been recieved 
                        while(blackout):
                            dis_request = conn.recv(1024).decode()
                            if (dis_request == "STB"):
                                blackout = False
                    finally:
                        unblocked = BlockInput(False) # unblock when STB request recieved 
                else:
                    raise RuntimeError('Input is already blocked by another thread!')


def get_admin_addr ():
    try:
        f = open("config.txt", "r")
        admin_addr=f.read()
        return admin_addr
    except:
        print("error reading configuration file")

def start_services():
    screensharing_thread = Thread(target=start_screensharing_server)
    screensharing_thread.start()
    blackout_thread = Thread(target=start_blackout_server)
    blackout_thread.start()
    

if (__name__=="__main__"):
    f = open("config.txt", "r")
    admin_addr=f.read()
    if (admin_addr==""):
        admin_setup()
    else:
        connection_monitor()
        start_services()
        

            


