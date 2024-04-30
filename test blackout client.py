from socket import socket

sock = socket()
sock.connect(("10.30.57.179",5001))
while True:
    message = input("This is where you type in your input request: ")
    message = message.encode()
    sock.send(message)

