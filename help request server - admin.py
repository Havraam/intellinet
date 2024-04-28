import tkinter as tk
from socket import socket
from threading import * 


def create_popup_window(PCID):
    # Create the main window
    window = tk.Tk()
    window.title("Help Needed")

    # Create the message label
    message = tk.Label(window, text=f"Help is needed at computer number {PCID}")
    message.pack(pady=10)

    # Function to close the window
    def close_window():
        window.destroy()

    # Create the dismiss button
    dismiss_button = tk.Button(window, text="Dismiss", command=close_window)
    dismiss_button.pack()

    # Run the main loop to display the window
    window.mainloop()


def listen_for_requests():
    global root    
    sock = socket()
    sock.bind(("192.168.68.104", 5001)) #bind to this computers ip adress 
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            PCID_valid = False
            while(PCID_valid == False): #while loop to validate PCID number if not valid than loop stuck until PCID is valid  
                PCID = conn.recv(1024).decode()
                if (True): #insert database validity check to make sure PCID is valid
                    PCID_valid = True
                    conn.send(("OK").encode()) #once PCID is valid an "OK" is sent to the client which gives it a green light to send requests 

            while(True):
                request = conn.recv(1024).decode()
                if request == "HELPME":
                    BlacoutThread = Thread(target = create_popup_window, args= PCID)
                    BlacoutThread.start()


    finally:
        sock.close()

listen_for_requests()