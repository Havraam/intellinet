import socket

#student == client


#getting the admin IP address 
f = open("config.txt", "r")
admin_addr=f.read()


sock = socket.socket()
sock.connect((fr"{admin_addr}.local",5003))

com_name = socket.gethostname()
request = (fr"{com_name}!HELPME").encode()
sock.send(request)
