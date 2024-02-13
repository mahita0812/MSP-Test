# login_gui.py
import tkinter as tk
from tkinter import messagebox

class LoginGUI:
    def __init__(self, parent, authenticate_callback, success_callback):
        self.parent = parent
        self.authenticate_callback = authenticate_callback
        self.success_callback = success_callback

        self.email_label = tk.Label(self.parent, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.parent)
        self.email_entry.pack(pady=5)

        self.password_label = tk.Label(self.parent, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.parent, show="*")  # Hide the password
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.parent, text="Login", command=self.authenticate)
        self.login_button.pack(pady=10)

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.authenticate_callback(email, password)
        self.success_callback()

if __name__ == "__main__":
    root = tk.Tk()
    login_gui = LoginGUI(root, lambda x, y: print("Authentication callback"), lambda: print("Success callback"))
    root.mainloop()
