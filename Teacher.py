import socket
import csv
import pandas as pd
import subprocess
import pygame
import ctypes
from threading import Thread
from zlib import decompress
import tkinter as tk
import time
import tkinter as tk
from tkinter import Menu
from tkinter import font   
import tkinter.filedialog as filedialog
import os 
from win10toast import ToastNotifier
import login_page_test as login 
import class_assignment_client as task_client
import datetime

def get_my_active_interface_ip():
    # create an datagram socket (single UDP request and response, then close)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect to an address on the internet, that's likely to always be up 
    # (the Google primary DNS is a good bet)
    sock.connect(("8.8.8.8", 80))
    # after connecting, the socket will have the IP in its address
    ip_addr = sock.getsockname()[0]
    # done
    sock.close()

    return ip_addr



class ComputerIcon:
    def __init__(self, master, color, x, y, computer_name,display_name):
        self.master = master
        self.computer_name = computer_name
        self.display_name = display_name
        self.frame = tk.Frame(master, width=100, height=100)
        self.frame.place(x=x, y=y)

        self.icon = tk.Label(self.frame, text=self.display_name, bg=color, width=12, height=6)
        self.icon.pack()

        self.icon.bind("<Button-3>", self.show_context_menu)

        self.menu = Menu(master, tearoff=0)
        self.menu.add_command(label="watch screen", command=self.activate_function_1)
        self.function_2_menu_item = self.menu.add_command(label="disable computer", command=self.activate_function_2, state='normal')
        # Initially, function 3 is grayed out
        self.function_3_menu_item = self.menu.add_command(label="enable computer", command=self.activate_function_3, state='disabled')
        self.menu.add_command(label="Send File", command=self.send_file_dialog)
        

        self.menu.add_separator()
        self.menu.add_command(label="Remove", command=self.remove_icon)


    def send_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            send_file_to_student(file_path, self.computer_name)

    def show_context_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def activate_function_1(self):
        activate_screensharing(self.computer_name)
        print(f" screen share activated on {self.icon.cget('text')}")

    def activate_function_2(self):
        global_start_blackout(self.computer_name)
        print(f" blackout started on {self.icon.cget('text')}")
        self.menu.entryconfig("disable computer",state = 'disabled')
        self.menu.entryconfig("enable computer",state = 'normal')
        
        
    def activate_function_3(self):
        blackout.stop_blackout()
        self.menu.entryconfig("disable computer",state = 'normal')
        self.menu.entryconfig("enable computer",state = 'disabled')


    def remove_icon(self):
        self.frame.destroy()
        self.master.remove_computer(self.computer_name)

class GlobalComputerIcon(ComputerIcon):
    def __init__(self, master, x, y):
        super().__init__(master, "tomato",x, y, "Global Control", "Global Control")
        self.icon.pack()
        self.menu.entryconfig("disable computer", label="Disable All", command=self.disable_all)
        self.menu.entryconfig("enable computer", label="Enable All", command=self.enable_all)
        self.menu.entryconfig("Send File", label="Send to All", command=self.send_file_to_all_dialog)
    
    def show_context_menu(self, event):
        # Remove the "watch screen" menu item from the context menu
        self.menu.delete("watch screen")
        self.menu.post(event.x_root, event.y_root)

    def send_file_to_all_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            send_file_to_all(file_path)

    def disable_all(self):
        global_start_wide_blackout()
        self.menu.entryconfig("Disable All",state = 'disabled')
        self.menu.entryconfig("Enable All",state = 'normal')

    def enable_all(self):
        global_stop_wide_blackout()
        self.menu.entryconfig("Disable All",state = 'normal')
        self.menu.entryconfig("Enable All",state = 'disabled')


class DesktopApp:
    def __init__(self, master):
        self.master = master
        master.title("intelinet")
        master.geometry("1000x800")  # Adjusted to fit more icons
        self.master.protocol("WM_DELETE_WINDOW", self.minimize_window)

        current_time = datetime.datetime.now()
        if current_time.hour < 12:
            greeting = "Good morning"
        elif current_time.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        
        create_assignment_button = tk.Button(master, text="Create Assignment", command=lambda: task_client.show_assignment_popup(master))
        create_assignment_button.place(relx=0.5, rely=0.95, anchor="center")

        large_font = font.Font(family="Helvetica", size=20, weight="bold")
        # Create the greeting label
        self.greeting_label = tk.Label(master, text=f"{greeting}, {login_window.get_display_name()}", font=large_font)
        self.greeting_label.place(x=10, y=10) 
        # Create the "Hello" label in the top right corner with larger text
        self.hello_label = tk.Label(master, text=socket.gethostname(), font=large_font)
        self.hello_label.place(x=775, y=10) 

        self.computers = []  # Start with an empty list of computers
        self.icons = []
        self.create_global_icon()
    
    def add_computer(self, com_name,display_name):
        self.computers.append((com_name,display_name))
        self.create_icons()
    
    def minimize_window(self):
        self.master.iconify()
    
    def create_global_icon(self):
        x = 25  # Adjust the position as needed
        y = 50
        global_icon = GlobalComputerIcon(self.master, x, y)
        self.icons.append(global_icon)

    def remove_computer(self, computer_name):
        self.computers = [computer for computer in self.computers if computer[0] != computer_name]
        self.create_icons()


    def create_icons(self):
        self.clear_icons()
        self.create_global_icon()
        for i, computer in enumerate(self.computers, start=1):
            x = (i % 6) * 150 + 25  # 6 icons per row
            y = (i // 6) * 150 + 50  # New row every 6 icons
            icon = ComputerIcon(self.master,"lightblue" ,x, y, computer[0],computer[1])
            self.icons.append(icon)

    def clear_icons(self):
        for icon in self.icons:
            icon.frame.destroy()
        self.icons = []





class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)



class FileReciever:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.downloads_path = os.path.join(os.path.expanduser("~"), os.path.join("Downloads"))


    def receive_file(self):
        # Receive file info
        file_name_bytes = b''
        while True:
            byte = conn.recv(1)
            if byte == b'\0':
                break
            file_name_bytes += byte
        file_name = file_name_bytes.decode('utf-8')
        file_size_bytes = self.conn.recv(8)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')
        print(file_name)
        # Receive file data
        # Ensure the downloads path exists
        os.makedirs(self.downloads_path, exist_ok=True)

        with open(os.path.join(self.downloads_path, file_name), 'wb') as f:
            bytes_read = 0
            while bytes_read < file_size:
                data = self.conn.recv(1024)
                if not data:
                    break
                f.write(data)
                bytes_read += len(data)
        print(f'File {file_name} received successfully from {self.addr}')
        # Show Windows notification
        toaster = ToastNotifier()
        toaster.show_toast("File Received", f"File '{file_name}' has been received and saved to {self.downloads_path}.", duration=5)


class ScreenShare:
    # Set process to be DPI aware so that the resolution wont be dependant on screen scaling
    def __init__(self) -> None:
        windll = ctypes.windll
        user32 = windll.user32
        user32.SetProcessDPIAware(1)
        self.WIDTH = user32.GetSystemMetrics(0)# Now use GetSystemMetrics in order to get resolution
        self.HEIGHT = user32.GetSystemMetrics(1)    
    

    def recvall(self, conn, length):
        """ Retreive all pixels. """

        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))
            if not data:
                return data
            buf += data
        return buf


    def watch_screen(self, host, port=5000): #insert wanted computers name 
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) # making pygamae window 
        clock = pygame.time.Clock()
        # setting button properties
        button_width = 100
        button_height = 30
        button_color = (255, 0, 0)  # Red
        button_text = "Stop Share"
        font_size = 20
        # creating button
        button = Button(self.WIDTH - button_width - 10, self.HEIGHT - button_height - 10, button_width, button_height, button_text, button_color, font_size)

        watching = True
        sock = socket.socket()
        sock.connect((socket.gethostbyname(host), port))
        share_res = sock.recv(1024).decode() #reciving target computer's resolution
        share_width = int((share_res.split(","))[0]) #spliting and turning share res to integer 
        share_height = int((share_res.split(","))[1])

        print (share_width + share_height)
        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button.is_clicked(event.pos):
                            watching = False  # Stop sharing on button click
                
                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(sock.recv(1), byteorder='big')
                size = int.from_bytes(sock.recv(size_len), byteorder='big')
                pixels = decompress(self.recvall(sock, size))

                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (share_width, share_height), 'RGB')
                scaled_img = pygame.transform.scale(img, (self.WIDTH,self.HEIGHT)) #scale the image

                # Display the scaled picture
                screen.blit(scaled_img, (0, 0))
                button.draw(screen)
                pygame.display.flip()
                clock.tick(60)
        except ConnectionResetError:
            print("connection closed ")
        except:
            print("something went wrong")
        finally:
            sock.close()
            pygame.quit()


class ClientHandler:
        def __init__(self, conn, addr):
            self.conn = conn
            self.addr = addr
            self.df = pd.read_csv("users.csv")


        def verify_client(self, given_comname):
            for com_name in self.df["COM_NAME"]:
                if(given_comname == com_name):
                    return True
            return False    
        

        def handle_client(self):
            while True:
                try:
                    request = self.conn.recv(1024).decode()
                    if not request:
                        break
                    print("request - ",request)
                    request = request.split('!')
                    com_name = request[0]
                    request = request[1]
                    if not request:
                        break
                    # Handle different client requests
                    if request == "ADMIN?":
                        self.handle_admin_request()

                    elif self.verify_client(com_name) :
                        print("handling user request")
                        self.handle_user_request(com_name,request)

                    else:
                        self.send_error("Invalid request")

                except ConnectionResetError:
                    print("ConnectionResetError - connection ended")
                    self.update_status(com_name, "offline")
                    app.remove_computer(com_name)
                    break
                except IndexError:
                    print ("index error!!!!")
                    
        
        
                
        def handle_admin_request(self):
            self.conn.send(("YES").encode())
            request = self.conn.recv(1024).decode()
            if request == "OK":
                self.conn.send(("NAME?").encode())
                com_name = self.conn.recv(1024).decode()
                print(com_name)
                data = [com_name, 'online']
                with open(fr"users.csv", 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(data)

        def handle_user_request(self, com_name ,request):
            print(request)
            if ("online" in request):
                request = request.split("?")
                self.update_status(com_name, "online")
                self.send_message("Welcome back into the system")
                app.add_computer(com_name,request[1])
            elif ("KEEP_ALIVE" in request):
                pass
            elif "SEND_FILE" == request:
                self.send_message("OK")
                file_reciever = FileReciever(self.conn, self.addr)
                file_reciever.receive_file()

        def update_status(self, com_name, status):
            self.df.loc[self.df["COM_NAME"] == com_name, "Status"] = status
            self.df.to_csv("users.csv", index=False)

        def send_message(self, message):
            self.conn.send(message.encode())

        def send_error(self, error):
            self.conn.send((f"Error: {error}").encode())

        

class Blackout:
    def __init__(self,target) -> None:
        self.active = False
        self.sock = socket.socket()
        self.target = target
        self.sock.connect((socket.gethostbyname(target),5002))
        

    def start_blackout(self):
        message = "BEB"
        message = message.encode()
        self.sock.send(message)
        self.active= True
        while self.active:
            time.sleep(3)
            self.sock.send(("KEEP_ALIVE").encode())
    
    def stop_blackout(self):
        message = "STB"
        message = message.encode()
        self.sock.send(message)
        self.active = False
        
def global_start_blackout(computer_name):
    global blackout
    blackout = Blackout(computer_name) 
    blackout_thread = Thread(target=blackout.start_blackout)
    blackout_thread.daemon = True
    blackout_thread.start()


def global_start_wide_blackout():
    global blackouts
    blackouts = []
    df = pd.read_csv("users.csv")
    for com_name in df["COM_NAME"]:
        if df.loc[df["COM_NAME"] == com_name, "Status"].values[0] == "online":
            blackout = Blackout(com_name)
            blackout_thread = Thread(target=blackout.start_blackout)
            blackout_thread.daemon = True
            blackout_thread.start()
            blackouts.append(blackout)

def global_stop_wide_blackout():
    for blackout in blackouts:
        blackout.stop_blackout()

def help_request_handler():
    sock = socket.socket()
    sock.bind((get_my_active_interface_ip(), 5001))
    sock.listen(50)
    while True:
        conn, addr = sock.accept()
        request = conn.recv(1024).decode()
        print("request - ",request)
        request = request.split('!')
        com_name = request[0]
        request = request[1]
        request = request.split('?')
        print (request)
        display_name = request[1]
        request = request[0]
        print(display_name)
        if (request == "HELPME"):
            popup_window_thread = Thread(target=create_popup_window , args=(display_name,))
            popup_window_thread.start()



def create_popup_window(display_name):
    # Create the main window
    window = tk.Tk()
    window.title("Help Needed")

    # Create the message label
    message = tk.Label(window, text=f"{display_name} needs help")
    message.pack(pady=10)

    # Function to close the window
    def close_window():
        window.destroy()
        window.quit()  # Exit the main loop


    # Create the dismiss button
    dismiss_button = tk.Button(window, text="Dismiss", command=close_window)
    dismiss_button.pack()

    # Run the main loop to display the window
    window.mainloop()

def send_file_to_student(file_path, com_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostbyname(com_name), 5004))

    file_name = os.path.basename(file_path).replace('\0', '')
    file_size = os.path.getsize(file_path)

    # Send file info
    sock.sendall(file_name.encode('utf-8') + b'\0')
    sock.sendall(file_size.to_bytes(8, byteorder='big'))

    # Send file data
    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            sock.sendall(data)
            data = f.read(1024)

    print(f'File {file_name} sent successfully to {com_name}')
    sock.close()

def send_file_to_all(file_path):
    df = pd.read_csv("users.csv")
    for com_name in df["COM_NAME"]:
        if df.loc[df["COM_NAME"] == com_name, "Status"].values[0] == "online":
            send_file_to_student(file_path, com_name)


def activate_screensharing(com_name):
    screenshare = ScreenShare()
    screensharing_thread = Thread(target=screenshare.watch_screen, args=(com_name,))
    screensharing_thread.daemon = True
    screensharing_thread.start()
    

def run_GUI():
    global app
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()


def send_IAMALIVE():
    df = pd.read_csv("users.csv")
    for com_name in df["COM_NAME"]:
        iamalive_thread = Thread(target=thread_IAMALIVES, args=(com_name, 3))
        iamalive_thread.daemon = True
        iamalive_thread.start()

def thread_IAMALIVES(com_name , timeout):
    print(com_name)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(fr"{com_name}.local")
        sock.settimeout(timeout)
        sock.connect((socket.gethostbyname(com_name), 5005))
        message = "IAMADMIN"
        sock.send(message.encode())
        confirmation = sock.recv(1024).decode()
        if confirmation == "OK":
            client_handler.update_status(com_name, "online")
        print(f"Sent '{message}' to {com_name}")
    except Exception as e:
        print(f"Error sending message to {com_name}: {e}")
    finally:
        sock.close()

if (__name__ == "__main__"):
    df = pd.read_csv("users.csv")
    df['Status'] = df['Status'].replace({'online': 'offline'})
    df.to_csv("users.csv", index=False) 
    login_window = login.LoginWindow()
    sock = socket.socket()
    sock.bind((get_my_active_interface_ip(), 5003))
    sock.listen(5)
    print("Server started")
    send_IAMALIVE()
    gui_thread = Thread(target=run_GUI)
    gui_thread.daemon = True  
    gui_thread.start()
    help_thread = Thread(target=help_request_handler)
    help_thread.daemon = True
    help_thread.start()
    while True:
        conn, addr = sock.accept()
        print(f'Client connected IP: {addr}')
        client_handler = ClientHandler(conn, addr)
        handler_thread = Thread(target=client_handler.handle_client)
        handler_thread.start()
        