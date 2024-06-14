import pandas as pd
import socket


df = pd.read_csv("users.csv")
for com_name in df["COM_NAME"]:
    print(com_name)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(fr"{com_name}.local")
        sock.connect((socket.gethostbyname(com_name), 5005))
        message = "IAMADMIN"
        sock.send(message.encode())
        print(f"Sent '{message}' to {com_name}")
    except Exception as e:
        print(f"Error sending message to {com_name}: {e}")
    finally:
        sock.close()