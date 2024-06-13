import socket
from tkinter import Tk, Label, Entry, Button
import time
from ctypes import wintypes
from threading import *
import pywinauto
from zlib import compress
from mss import mss
import ctypes
import tkinter as tk
import tkinter.filedialog as filedialog
import os
from win10toast import ToastNotifier
import login_page_test as login

class HelpWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Need help?")
        self.root.geometry("400x200")

        label = tk.Label(self.root, text="Need help?")
        label.pack(pady=10)

        call_help_button = tk.Button(self.root, text="Call Help", command=send_help_request)
        call_help_button.pack(pady=5)
        send_file_button = tk.Button(self.root, text="Send File", command=self.send_file_dialog)
        send_file_button.pack(pady=5)
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_window)

    def minimize_window(self):
        self.root.iconify()

    def send_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            admin_addr = get_admin_addr()
            send_file(file_path, admin_addr, 5003)

    def show(self):
        self.root.mainloop()
    
    def destroy(self):
        self.root.destroy()

class FileReceiver:
    def __init__(self):
        self.downloads_path = os.path.join(os.path.expanduser("~"), os.path.join("Downloads"))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname() + ".local", 5004))
        self.sock.listen(1)
        print("File receiving server started.")

    def receive_file(self):
        while (True):
            conn, addr = self.sock.accept()
            print(f'Connection from {addr}')

            # Receive file info
            file_name = conn.recv(1024).decode('latin-1').replace('\0', '')
            file_size_bytes = conn.recv(4)
            file_size = int.from_bytes(file_size_bytes, byteorder='big')
            print(file_name)
            # Receive file data
            with open(os.path.join(self.downloads_path, file_name), 'wb') as f:
                bytes_read = 0
                while bytes_read < file_size:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_read += len(data)

            print(f'File {file_name} received successfully')
            # Show Windows notification
            toaster = ToastNotifier()
            toaster.show_toast("File Received", f"File '{file_name}' has been received and saved to {self.downloads_path}.", duration=5)
            

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
        print(host,port)        
        try:
            sock.listen(5)
            print('screen share server started.')

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
    global admin_verified
    admin_verified =False
    computer_name = entry.get()
    # Process the computer name here (e.g., store it)
    print(f"Admin computer name: {computer_name}")
    f = open("config.txt", "w")   
    try: 
        sock = socket.socket()
        sock.connect((fr"{computer_name}.local",5003))
        message = ("n!ADMIN?").encode()
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
                admin_verified=True
    
    except:
        admin_unavailable()
        
    setup_window.destroy()  # Close the setup_window after processing

def send_file(file_path, host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        client_socket.send((fr"{socket.gethostname()}!SEND_FILE").encode('latin-1'))
        response = client_socket.recv(1024).decode()
        if(response == "OK"):
            file_name = os.path.basename(file_path).replace('\0', '')
            file_size = os.path.getsize(file_path)

            # Send file info
            client_socket.send(file_name.encode())
            client_socket.send(file_size.to_bytes(4, byteorder='big'))

            # Send file data
            with open(file_path, 'rb') as f:
                data = f.read(1024)
                while data:
                    client_socket.send(data)
                    data = f.read(1024)

            print(f'File {file_name} sent successfully')
            client_socket.close()
    except:
        print("file sending connection failed")


def send_help_request():
    try:
        f = open("config.txt", "r")
        admin_addr=f.read()
        sock = socket.socket()
        sock.connect((fr"{admin_addr}.local",5001))
        com_name = socket.gethostname()
        request = (fr"{com_name}!HELPME").encode()
        sock.send(request)
        print("help request sent")
    except:
        print("help request connection failed")

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


def admin_unavailable():
    global root
    root = Tk()
    root.title("Admin Unavailable")
    root.geometry("300x100")  # Adjust window size as needed

    label = Label(root, text="Admin unavailable now, please try again later.")
    label.pack()

    ok_button = Button(root, text="OK", command=root.destroy)
    ok_button.pack()
    if help_window:
        help_window.root.withdraw() 

    recconnect_thread = Thread(target=listen_for_admin_reconnection)
    recconnect_thread.start()
    root.mainloop()

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
    print('blackout server started.')
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
                        break 
                else:
                    raise RuntimeError('Input is already blocked by another thread!')
            else:
                print("invalid request")


def get_admin_addr ():
    try:
        f = open("config.txt", "r")
        admin_addr=f.read()
        return admin_addr
    except:
        print("error reading configuration file")

def start_help_window():
    global help_window
    help_window = HelpWindow()
    help_window.show()


def start_services():
    admin_addr = get_admin_addr()
    print(admin_addr)
    keep_alive_thread = Thread(target=intial_admin_connect , args = (admin_addr,))
    keep_alive_thread.start()
    screensharing_thread = Thread(target=start_screensharing_server)
    screensharing_thread.start()
    blackout_thread = Thread(target=start_blackout_server)
    blackout_thread.start()
    time.sleep(1)
    help_window_thread = Thread(target=start_help_window)
    help_window_thread.start()
    file_receiving_server = FileReceiver()
    file_receiving_thread = Thread(target=file_receiving_server.receive_file)
    file_receiving_thread.start()



    

    

def intial_admin_connect(admin_addr) :
    try:
        sock = socket.socket()
        sock.connect((fr"{admin_addr}.local",5003))
        sock.send((fr"{socket.gethostname()}!online").encode())

        while True:
            try:
                sock.send((fr"{socket.gethostname()}!KEEP_ALIVE").encode())
                time.sleep(2)
            except:
                print("connection ended - admin went offline")
                admin_unavailable()
                break
    except:
        print("admin not available right now , try again later")
        admin_unavailable()

def listen_for_admin_reconnection():
    admin_addr = get_admin_addr()
    if admin_addr:
        sock = socket.socket()
        sock.bind((fr"{socket.gethostname()}.local", 5005))
        sock.listen(5)
        print('Listening for admin connection...')

        while True:
            print("Waiting for admin connection...")
            conn, addr = sock.accept()
            print('connected:', addr)
            message = conn.recv(1024).decode()
            if(message == "IAMADMIN"):
                print("admin reconnected")
                help_window.root.deiconify()  # Show the help_window again

            conn.close()
            break
    else:
        print("Error: Unable to get admin address")
    
    

if (__name__=="__main__"):
    global admin_verified
    login_window = login.LoginWindow()
    print("hello")
    admin_addr= get_admin_addr()
    if (admin_addr==""):
        admin_setup()
        if(admin_verified):
            start_services()
    else:
        start_services()
        
        

            


