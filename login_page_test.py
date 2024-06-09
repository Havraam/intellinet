import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter as tk
import hashlib
from tkinter import simpledialog, messagebox
import time 
# Initialize the Firebase app
cred = credentials.Certificate(fr"C:\Users\erele\Desktop\intelinet-61b65-firebase-adminsdk-k8fbq-a7876eedb9.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://intelinet-61b65-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to the database
ref = db.reference('users')

class LoginWindow:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("300x200")  # Adjust window size as needed
        self.login_window.protocol("WM_DELETE_WINDOW", self.minimize_window)


        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        self.login_status_label = tk.Label(self.login_window, text="")
        self.login_status_label.pack()

        self.login_button = tk.Button(self.login_window, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(self.login_window, text="Sign Up", command=self.show_signup)
        self.signup_button.pack()
        self.display_name = ""
        self.login_window.mainloop()

    def get_display_name(self):
        return self.display_name

    def minimize_window(self):
        self.login_window.iconify()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the user exists in the database
        if (username == "") or (password == ""):
            self.login_status_label.config(text="Please fill in all fields", fg="red")
            return
        user_data = ref.child(username).get()
        print(password)
        if user_data is not None and user_data.get('password') == self.convert_to_md5(password):
            self.login_status_label.config(text="Login Successful", fg="green")
            self.login_window.destroy()
            self.display_name = username
        else:
            self.login_status_label.config(text="Incorrect username or password", fg="red")

    def show_signup(self):
        signup_window = tk.Toplevel(self.login_window)
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")  # Adjust window size as needed

        signup_status_label = tk.Label(signup_window, text="")
        signup_status_label.pack()

        username_label = tk.Label(signup_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(signup_window)
        username_entry.pack()

        password_label = tk.Label(signup_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack()

        password_req_label = tk.Label(signup_window, text="Password requirements:\n -8 characters\n -1 uppercase\n - 1 lowercase\n - 1 number\n - 1 special character")
        password_req_label.pack()
        def signup():
            username = username_entry.get()
            password = password_entry.get()
            if(username == "") or (password == ""):
                signup_status_label.config(text="Please fill in all fields", fg="red")
                return
            # Check if the user already exists
            user_data = ref.child(username).get()

            if user_data is None:
                if(self.password_requirements(password)):
                    ref.child(username).set({'password': self.convert_to_md5(password)})
                    messagebox.showinfo("Sign Up Successful", "Your account has been created.", parent=self.login_window)
                    signup_window.destroy()
                else:
                    signup_status_label.config(text="Password does not meet requirements", fg="red")
            else:
                signup_status_label.config(text="Username already exists", fg="red")

        signup_button = tk.Button(signup_window, text="Sign Up", command=signup)
        signup_button.pack()


    def password_requirements(self,password):
        if len(password) < 8:
            return False
        elif not any(char.isupper() for char in password):
            return False
        elif not any(char.islower() for char in password):
            return False
        elif not any(char.isdigit() for char in password):
            return False
        elif not any(char in "!@#$%^&*()_+?" for char in password):
            return False
        else:
            return True
        
    def convert_to_md5(self, password):
        return hashlib.md5(password.encode()).hexdigest()


