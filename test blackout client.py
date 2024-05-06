from socket import socket

sock = socket()
sock.connect(("192.168.68.103",5001))
while True:
    message = input("This is where you type in your input request: ")
    message = message.encode()
    sock.send(message)

