from socket import socket

sock = socket()
sock.connect(("192.168.68.104",5001))
while True:
    PCID = "1"
    PCID = PCID.encode()
    sock.send(PCID)
    response = sock.recv(1024).decode()
    print(response)
    if(response == "OK"):
        message = input("This is where you type in your input request: ")
        message = message.encode()
        sock.send(message)