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

class ComputerIcon:
    def __init__(self, master, x, y, computer_name):
        self.master = master
        self.computer_name = computer_name
        self.frame = tk.Frame(master, width=100, height=100)
        self.frame.place(x=x, y=y)

        self.icon = tk.Label(self.frame, text=computer_name, bg="lightblue", width=12, height=6)
        self.icon.pack()

        self.icon.bind("<Button-3>", self.show_context_menu)

        self.menu = Menu(master, tearoff=0)
        self.menu.add_command(label="watch screen", command=self.activate_function_1)
        self.menu.add_command(label="disable computer", command=self.activate_function_2)
        self.menu.add_separator()
        self.menu.add_command(label="Remove", command=self.remove_icon)

    def show_context_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def activate_function_1(self):
        activate_screensharing(self.computer_name)
        print(f" screen share activated on {self.icon.cget('text')}")

    def activate_function_2(self):
        print(f" blackout started on {self.icon.cget('text')}")

    def remove_icon(self):
        self.frame.destroy()
        self.master.remove_computer(self.computer_name)

class DesktopApp:
    def __init__(self, master):
        self.master = master
        master.title("Desktop App")
        master.geometry("1000x800")  # Adjusted to fit more icons

        self.computers = []  # Start with an empty list of computers
        self.icons = []

        # Adding control buttons
        # self.add_button = tk.Button(master, text="Add Computer", command=self.add_computer)
        # self.add_button.pack()

    def load_computers(self):
        df = pd.read_csv("users.csv")
        for value in df['COM_NAME']:
            if value['Status'] == 'online':
                computer_name = value
                self.computers.append(value)
                self.create_icons()

    def add_computer(self, com_name):
        self.computers.append(com_name)
        self.create_icons()

    def remove_computer(self, computer_name):
        self.computers = [computer for computer in self.computers if computer != computer_name]
        self.create_icons()


    def create_icons(self):
        self.clear_icons()
        for i, computer in enumerate(self.computers):
            x = (i % 6) * 150 + 25  # 6 icons per row
            y = (i // 6) * 150 + 25  # New row every 6 icons
            icon = ComputerIcon(self.master, x, y, computer)
            self.icons.append(icon)

    def clear_icons(self):
        for icon in self.icons:
            icon.frame.destroy()
        self.icons = []

    def reposition_icons(self):
        for i, icon in enumerate(self.icons):
            x = (i % 6) * 150 + 25
            y = (i // 6) * 150 + 25
            icon.frame.place(x=x, y=y)




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


    def screenshare(self, host, port=5000): #insert wanted computers name 
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
        host = host+".local"
        print(host)
        sock = socket.socket()
        sock.connect((host, port))
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
                    print("request - ",request)
                    request = request.split('!')
                    com_name = request[0]
                    request = request[1]
                    
                    print(com_name)
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
                    

        
        
                
        def handle_admin_request(self):
            # Implement admin logic here (e.g., toggle modules)
            self.conn.send(("YES").encode())
            request = self.conn.recv(1024).decode()
            if request == "OK":
                self.conn.send(("NAME?").encode())
                com_name = self.conn.recv(1024).decode()
                print(com_name)
                app = app.add_computer(com_name)
                data = [com_name, 'online']
                with open(fr"users.csv", 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(data)

        def handle_user_request(self, com_name ,request):
            print(request)
            if ("online" == request):
                self.update_status(com_name, "online")
                self.send_message("Welcome back into the system")
                app.add_computer(com_name)
            if ("HELPME" == request):
                print("HELPME")
                create_popup_window(com_name)
            if ("KEEP_ALIVE" == request):
                pass

        def update_status(self, com_name, status):
            self.df.loc[self.df["COM_NAME"] == com_name, "Status"] = status
            self.df.to_csv("users.csv", index=False)

        def send_message(self, message):
            self.conn.send(message.encode())

        def send_error(self, error):
            self.send_message(f"Error: {error}")
        # Function to start the client handler thread (implementation varies based on language)
        def start(self):
            # Use threading or multiprocessing library to run in a separate thread
            thread = Thread(target=self.handle_client)
            thread.start()

class Blackout:
    def __init__(self,target) -> None:
        self.sock = socket.socket()
        self.target = target
        self.sock.connect((fr"{target}.local",5002))

    def start_blackout(self):
        while True:
            #IF specific button on gui pressed ----> send BEB
            #IF specific button on gui pressed ----> send STB
            message = input("This is where you type in your input request: ")
            message = message.encode()
            self.sock.send(message)
        
        

def create_popup_window(given_COMNAME):
    # Create the main window
    window = tk.Tk()
    window.title("Help Needed")

    # Create the message label
    message = tk.Label(window, text=f"Help is needed at {given_COMNAME}")
    message.pack(pady=10)

    # Function to close the window
    def close_window():
        window.destroy()

    # Create the dismiss button
    dismiss_button = tk.Button(window, text="Dismiss", command=close_window)
    dismiss_button.pack()

    # Run the main loop to display the window
    window.mainloop()

def activate_screensharing(com_name):
    screenshare = ScreenShare()
    ScreenShare.screenshare(screenshare, com_name)

def run_GUI():
    global app
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()

if (__name__ == "__main__"):
    df = pd.read_csv("users.csv")
    df['Status'] = df['Status'].replace({'online': 'offline'})
    df.to_csv("users.csv", index=False)  
    sock = socket.socket()
    sock.bind((fr"{socket.gethostname()}.local", 5003))
    sock.listen(5)
    print("Server started")
    gui_thread = Thread(target=run_GUI)
    gui_thread.start()
    while True:
        conn, addr = sock.accept()
        print(f'Client connected IP: {addr}')
        client_handler = ClientHandler(conn, addr)
        client_handler.start()  # Run client handler in a separate thread