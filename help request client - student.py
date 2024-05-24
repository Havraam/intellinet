import socket

#student == client


#getting the admin IP address 
f = open("config.txt", "r")
admin_addr=f.read()


sock = socket.socket()
sock.connect((fr"{admin_addr}.local",5001))

com_name = socket.gethostname()
com_name = com_name.encode()
sock.send(com_name)
response = sock.recv(1024).decode()
print(response)
if(response == "OK"):
    message = "HELPME"
    message = message.encode()
    sock.send(message)
    sock.close()