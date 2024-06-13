import pandas as pd
import socket


df = pd.read_csv("users.csv")
for com_name in df["COM_NAME"]:
    print(com_name)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect(("192.168.68.103", 4956))
        print(fr"{com_name}.local")
        sock.connect((fr"{com_name}.local", 4956))
        message = "IAMADMIN"
        sock.send(message.encode())
        print(f"Sent '{message}' to {com_name}")
    except Exception as e:
        print(f"Error sending message to {com_name}: {e}")
    finally:
        sock.close()