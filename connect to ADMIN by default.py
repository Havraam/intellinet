from socket import socket

f = open("config.txt", "r")
admin_addr=f.read()

sock = socket()
sock.connect((fr"{admin_addr}.local",5001))
print("connected")
