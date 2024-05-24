import socket
import csv
import pandas as pd
import subprocess


def update_status(df, com_name, status):
    df_name = df[df["COM_NAME"] == com_name]
    df_name["Status"] = status
    df.update(df_name)
    df.to_csv("users.csv" , index=False)

def togglee_all_modules():
    hrlp_request_server = subprocess.Popen(["python","help request server - admin.py"])
    print("hello")
    

if (__name__ == "__main__"):
    togglee_all_modules()
    sock = socket.socket()
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
                conn.send(("NAME?").encode())
                COM_NAME = conn.recv(1024).decode()
                print(COM_NAME)
                data = [COM_NAME,'online']
                print(data)
                with open(fr"users.csv", 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(data)
        

        else:
            df = pd.read_csv("users.csv") 
            for com_name in df["COM_NAME"]:
                if(request == com_name):
                    update_status(df , com_name , "online")
                    print("welcome back into the system")


