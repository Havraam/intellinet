import ctypes
from ctypes import wintypes
from socket import socket
from threading import *
import tkinter as tk
import pywinauto


#setting up the blockinput variable
BlockInput = ctypes.windll.user32.BlockInput

#starting up the server
sock = socket()
sock.bind(("192.168.68.103",5001))
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
