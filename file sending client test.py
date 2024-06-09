import socket
import os

HOST = '192.168.68.103'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

file_path = input('Enter file path: ')
file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)

# Send file info
client_socket.send(file_name.encode())
client_socket.send(file_size.to_bytes(4, byteorder='big'))



# Send file data
with open(file_path, 'rb') as f:
    data = f.read(1024)
    while data:
        client_socket.send(data)
        data = f.read(1024)

print(f'File {file_name} sent successfully')
client_socket.close()