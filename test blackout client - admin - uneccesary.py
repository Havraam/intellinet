from socket import socket

sock = socket()
sock.connect(("LAPTOP-L6IV9KLC.LOCAL",5002))
while True:
    message = input("This is where you type in your input request: ")
    message = message.encode()
    sock.send(message)

