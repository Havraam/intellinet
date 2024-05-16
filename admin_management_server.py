import socket
import csv




sock = socket.socket
sock.bind((fr"{socket.gethostname()}.local",5003))
sock.listen(50)
print ("server started")

while 'connected':
    conn,addr = sock.accept()
    print('Client connected IP:',addr)
    request = conn.recv(1024).decode()
    if(request=="ADMIN?"):
        conn.send(("YES").encode())
        request = conn.recv(1024).decode()
        if ( request == "OK"):
            conn.send("NAME?")
            COM_NAME = conn.recv(1024).decode()
            data = [[COM_NAME,'online']]
            with open(fr"C:\Users\erele\Python projects\intellinet\users.csv", 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)






