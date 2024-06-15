import tkinter as tk
import socket
from tkinter import ttk
from Student import get_my_active_interface_ip
import time
from threading import Thread
from win10toast import ToastNotifier

def student_show_assignment_popup(title, description, timer_minutes):
    student_assignment_popup = tk.Tk()
    student_assignment_popup.title("New Assignment")

    # Assignment Title
    title_label = ttk.Label(student_assignment_popup, text="Assignment Title:")
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_value = ttk.Label(student_assignment_popup, text=title)
    title_value.grid(row=0, column=1, padx=5, pady=5)

    # Assignment Description
    description_label = ttk.Label(student_assignment_popup, text="Assignment Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    description_value = ttk.Label(student_assignment_popup, text=description)
    description_value.grid(row=1, column=1, padx=5, pady=5)

    if timer_minutes != 'None':
        # Assignment Timer
        timer_minutes = int(timer_minutes)
        student_assignment_popup.protocol("WM_DELETE_WINDOW", disable_close(student_assignment_popup))  # Disable close button
        timer_label = ttk.Label(student_assignment_popup, text="Assignment Timer (minutes):")
        timer_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        timer_value = ttk.Label(student_assignment_popup, text=f"{timer_minutes:02d}:00")
        timer_value.grid(row=2, column=1, padx=5, pady=5)

        # Start the timer
        countdown(timer_minutes * 60, timer_value, student_assignment_popup)
    student_assignment_popup.mainloop()

def countdown(remaining, timer_label, window):
    if remaining >= 0:
        minutes, seconds = divmod(remaining, 60)
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        timer_label.after(1000, countdown, remaining - 1, timer_label, window)
    else:
        window.destroy()# Enable close button and window manager's close protocol
        toaster = ToastNotifier()
        toaster.show_toast("Time's up!","the time for your assignment ran out" , duration=5)

def disable_close(window):
    window.attributes("-disabled", True)  # Disable the close button

# Function to receive assignment details from the client
def receive_assignment_from_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((get_my_active_interface_ip(), 5006))
    sock.listen(1)
    print("Waiting for assignment details...")
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024).decode()
        data = data.split(",")
        print(data)
        conn.close()
        # Code to receive the assignment details from the client
        title = data[0]
        description = data[2]
        timer_minutes = data[1]  # Example timer value (60 minutes)
        assignment_thread = Thread(target=student_show_assignment_popup, args=(title, description, timer_minutes))
        assignment_thread.start()





