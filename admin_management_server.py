import socket




sock = socket.socket
sock.bind((fr"{socket.gethostname()}.local",5003))
sock.listen(50)
print ("server started")

while 'connected':
    conn,addr = sock.accept()
    print('Client connected IP:',addr)
    