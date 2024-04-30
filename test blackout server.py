import tkinter as tk
from socket import socket
from threading import * 
import ctypes
from ctypes import wintypes


def disable_screen():
    pass

def start_blackout(BlockInput):
    global root
    root = tk.Tk()
    root.attributes("-fullscreen", True, "-topmost", True)
    root.protocol("WM_DELETE_WINDOW", disable_screen)
    root.mainloop()
    blocked = BlockInput(True)
    if blocked:
        pass
    else:
        raise RuntimeError('input is already blocked by another thread')

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
                    BlockInput = ctypes.windll.user32.BlockInput
                    BlackoutThread = Thread(target = start_blackout, args= BlockInput)
                    BlackoutThread.start()
                elif request == "STBlackout" :
                    root.destroy()
                    unblocked = BlockInput(False)
                    BlackoutThread.join()


    finally:
        sock.close()

listen_for_requests()



print("hello")
