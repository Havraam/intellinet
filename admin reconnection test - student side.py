import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((fr"{socket.gethostname()}.local", 5005))
sock.listen(5)
print('Listening for admin connection...')

while True:
    print("Waiting for admin connection...")
    conn, addr = sock.accept()
    print('connected:', addr)
    message = conn.recv(1024).decode()
    if(message == "IAMADMIN"):
        print("admin reconnected")
        #help_window.root.deiconify()  # Show the help_window again

    conn.close()
    break
