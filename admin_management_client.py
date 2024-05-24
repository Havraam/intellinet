import socket
from tkinter import Tk, Label, Entry, Button


def get_computer_name():
    computer_name = entry.get()
    # Process the computer name here (e.g., store it)
    print(f"Admin computer name: {computer_name}")
    f = open("config.txt", "w")    
    sock = socket.socket()
    sock.connect((fr"{computer_name}.local",5003))
    message = ("ADMIN?").encode()
    sock.send(message)
    response = sock.recv(1024).decode() 
    if (response == "YES"):
        f.write(computer_name)
        message = ("OK").encode()
        sock.send(message)
        response = sock.recv(1024).decode()
        if(response == "NAME?"):
            message = (socket.gethostname()).encode()
    
    setup_window.destroy()  # Close the setup_window after processing

def admin_setup():
    global setup_window
    global entry
    setup_window = Tk()
    setup_window.title("Admin Setup")

    welcome_message = Label(setup_window, text="Greetings friend !")
    welcome_message.pack()

    instruction_message = Label(setup_window, text="Please insert admin computer name:")
    instruction_message.pack()

    entry = Entry(setup_window)
    entry.pack()

    submit_button = Button(setup_window, text="Submit", command=get_computer_name)
    submit_button.pack()

    setup_window.mainloop()



f = open("config.txt", "r")
admin_addr=f.read()
if (admin_addr==""):
    admin_setup()
else:
    sock = socket()
    sock.connect((fr"{admin_addr}.local",5003))


    


