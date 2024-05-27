import tkinter as tk

def minimize_window():
    root.iconify()

def call_help():
    # Code to call for help can be added here
    print("Help is on the way!")

root = tk.Tk()
root.title("Need help?")
root.geometry("200x100")

label = tk.Label(root, text="Need help?")
label.pack(pady=10)

call_help_button = tk.Button(root, text="Call Help", command=call_help)
call_help_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", minimize_window)

root.mainloop()
