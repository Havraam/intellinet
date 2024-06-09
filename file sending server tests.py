# Server code
import socket
import os

HOST = '192.168.68.103'
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f'Server listening on {HOST}:{PORT}...')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Got connection from {addr}')
    
    # Receive file info
    file_name = client_socket.recv(1024).decode()
    file_size_bytes = client_socket.recv(4)
    file_size = int.from_bytes(file_size_bytes, byteorder='big')
    
    # Receive file data
    with open(file_name, 'wb') as f:
        bytes_read = 0
        while bytes_read < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
            bytes_read += len(data)
    
    print(f'File {file_name} received successfully')
    client_socket.close()


