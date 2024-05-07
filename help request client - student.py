from socket import socket

#student == client


#getting the admin IP address 
f = open("config.txt", "r")
admin_addr=f.read()


sock = socket()
sock.connect((fr"{admin_addr}.local",5001))
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