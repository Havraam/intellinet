import tkinter as tk
from tkinter import ttk
import socket
import pandas as pd


def disable_timer_entry(timer_entry):
    timer_entry.config(state="disabled")

def enable_timer_entry(timer_entry):
    timer_entry.config(state="normal")
    timer_entry.focus_set()

def show_assignment_popup(root):
    assignment_popup = tk.Toplevel(root)
    assignment_popup.title("Create Assignment")

    # Assignment Title
    title_label = ttk.Label(assignment_popup, text="Assignment Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry = ttk.Entry(assignment_popup)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    # Assignment Description
    description_label = ttk.Label(assignment_popup, text="Assignment Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    description_entry = tk.Text(assignment_popup, height=5, width=30)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

    # Assignment Timer
    timer_label = ttk.Label(assignment_popup, text="Assignment Timer:")
    timer_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    timer_var = tk.IntVar()
    no_timer_radio = ttk.Radiobutton(assignment_popup, text="No Time Limit", variable=timer_var, value=0, command=lambda: disable_timer_entry(timer_entry))
    no_timer_radio.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    timer_frame = ttk.Frame(assignment_popup)
    timer_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    timer_entry = ttk.Entry(timer_frame, width=5)
    timer_entry.pack(side="left")
    timer_entry.insert(0, "120")  # Default value of 120 minutes
    timer_entry.config(state="disabled")

    timer_label = ttk.Label(timer_frame, text="minutes (up to 120)")
    timer_label.pack(side="left", padx=5)

    timer_radio = ttk.Radiobutton(assignment_popup, text="Time Limit", variable=timer_var, value=1, command=lambda: enable_timer_entry(timer_entry))
    timer_radio.grid(row=2, column=1, padx=5, pady=20, sticky="e")

    # Submit Button
    submit_button = ttk.Button(assignment_popup, text="Submit")
    submit_button.grid(row=4, column=1, padx=5, pady=5)

    # Function to handle submission
    def submit_assignment():
        title = title_entry.get()
        description = description_entry.get("1.0", "end-1c")  # Get text from Text widget
        if ( title != "" ) and ( description != "" ):
            if timer_var.get() == 0:
                timer = None
            else:
                timer = timer_entry.get()
            # Send the assignment details to the server
            send_assignment_to_students(title, description, timer)
            assignment_popup.destroy()  # Close the assignment popup window
        else:
            status_label.config(text="please fill all fields", foreground="red")

    submit_button.config(command=submit_assignment)

    status_label = ttk.Label(assignment_popup, text="")
    status_label.grid(row=5, column=1, padx=5, pady=5)


# Function to send assignment details to the server
def send_assignment_to_students(title, description, timer):
    df = pd.read_csv("users.csv")
    data = fr"{title},{timer},{description}"
    for com_name in df["COM_NAME"]:
        if df.loc[df["COM_NAME"] == com_name, "Status"].values[0] == "online":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((socket.gethostbyname(com_name), 5006))
            client_socket.send(data.encode())
            client_socket.close()
    # Code to send the assignment details to the server
    print(title , timer , description)
    pass

