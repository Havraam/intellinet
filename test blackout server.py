import tkinter as tk

def disable_screen():
    pass
root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)
root.protocol("WM_DELETE_WINDOW", disable_screen)

but = tk.Button(root, text = "I have completed my tasks", command=root.destroy)
but.grid()

root.mainloop()