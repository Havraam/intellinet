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
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
import random
import string

def create_AES_key():
    # Define a pool of characters to choose from
    characters = "&%$@Supercalifragilisticexpialidocious!@#)(" + string.ascii_letters + string.digits
    aes_key = "".join(random.choice(characters) for _ in range(16))  # Generate a 16-character key
    print(aes_key)
    return aes_key.encode('utf-8') 

# Generate RSA key pair for the student side
def generate_student_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

AES_KEY = create_AES_key()
student_private_key, student_public_key = generate_student_key_pair()

def encrypt_aes_key(public_key):
    encrypted_aes_key = public_key.encrypt(
        AES_KEY ,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key):
    aes_key = student_private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key


def encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + encrypted_data

def decrypt(encrypted_data):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_data.decode()

def send_encrypted_data(data, conn):
    encrypted_data = encrypt(data)
    conn.send(encrypted_data)

def receive_encrypted_data(conn):
    encrypted_data = conn.recv(4096)
    decrypted_data = decrypt(encrypted_data)
    decrypted_data = decrypted_data.decode()
    return decrypted_data

def receive_public_key(sock):
    public_key_bytes = sock.recv(4096)
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )
    return public_key











class HelpWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Need help?")
        self.root.geometry("200x100")

        label = tk.Label(self.root, text="Need help?")
        label.pack(pady=10)

        call_help_button = tk.Button(self.root, text="Call Help", command=send_help_request)
        call_help_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.minimize_window)

    def minimize_window(self):
        self.root.iconify()

    def show(self):
        self.root.mainloop()


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
                #conn.send (resolution.encode())
                send_encrypted_data(resolution.encode(),conn)
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


def send_help_request():
    f = open("config.txt", "r")
    admin_addr=f.read()
    sock = socket.socket()
    sock.connect((fr"{admin_addr}.local",5001))
    com_name = socket.gethostname()
    request = (fr"{com_name}!HELPME").encode()
    #sock.send(request)
    send_encrypted_data(request,sock)
    print("help request sent")

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
            #request = conn.recv(1024).decode()
            request = receive_encrypted_data(conn)
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
                            #dis_request = conn.recv(1024).decode()
                            dis_request = receive_encrypted_data(conn)
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

def key_exchange(sock):
    teacer_public_key = receive_public_key(sock)
    print("teacher public key recieved")

    student_public_key_bytes = student_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    sock.sendall(student_public_key_bytes)
    print("public key sent")

    teacher_encrypted_aes_key= sock.recv(1024)
    teacher_aes_key= decrypt_aes_key(teacher_encrypted_aes_key)
    print("teacher aes key decrypted")
    
    encrypted_aes_key = encrypt_aes_key(teacer_public_key)
    sock.send(encrypted_aes_key)
    print("encrypted aes key sent")

    
    print(teacher_aes_key)
    return teacher_aes_key
    

def intial_admin_connect(admin_addr) :
    global teacher_aes_key
    try:
        sock = socket.socket()
        sock.connect((fr"{admin_addr}.local",5003))
        sock.send((fr"{socket.gethostname()}!online").encode())
        request = sock.recv(1024).decode()
        if(request == 'Pkey'):
            teacher_aes_key = key_exchange(sock)

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


    
    

if (__name__=="__main__"):
    global admin_verified
    admin_addr= get_admin_addr()
    if (admin_addr==""):
        admin_setup()
        if(admin_verified):
            start_services()
    else:
        start_services()
        
        

            



