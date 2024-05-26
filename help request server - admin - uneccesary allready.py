import tkinter as tk
import socket
from threading import * 
import pandas as pd

def create_popup_window():
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


def handle_client(client_socket, client_address):
    while True:
        request = client_socket.recv(1024).decode()
        if request == "HELPME":
            print(f"Help request from {client_address[0]}")
            BlacoutThread = Thread(target=create_popup_window)
            BlacoutThread.start()
            

if (__name__== "__main__"):
    global root    
    sock = socket.socket()
    sock.bind((fr"{socket.gethostname()}.local", 5001)) #bind to this computers ip adress 
    try:
        sock.listen(50)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            COMNAME_valid = False
            while(COMNAME_valid == False): #while loop to validate comnames if not valid than loop stuck until comname is valid  
                given_COMNAME = conn.recv(1024).decode()
                df = pd.read_csv("users.csv") 
                for com_name in df["COM_NAME"]:
                    if(given_COMNAME == com_name):
                        COMNAME_valid = True
                        conn.send(("OK").encode()) #once PCID is valid an "OK" is sent to the client which gives it a green light to send requests 
                        break


            client_thread = Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True  # Mark as daemon to avoid blocking server shutdown
            client_thread.start()

    finally:
        sock.close()