import tkinter as tk
from socket import socket
from threading import * 

def disable_screen():
    pass

def start_blackout():
    global root
    root = tk.Tk()
    root.attributes("-fullscreen", True, "-topmost", True)
    root.protocol("WM_DELETE_WINDOW", disable_screen)

    but = tk.Button(root, text = "I have completed my tasks", command=root.destroy)
    but.grid()


    root.mainloop()

def listen_for_requests():
    global root    
    sock = socket()
    sock.bind(("10.30.56.202", 5001))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            while(True):
                request = conn.recv(1024).decode()
                if request == "BEBlackout":
                    BlacoutThread = Thread(target = start_blackout)
                    BlacoutThread.start()
                elif request == "STBlackout" :
                    root.destroy()
                    BlacoutThread.join()


    finally:
        sock.close()

listen_for_requests()




