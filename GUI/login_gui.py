from tkinter import *
from tkinter import messagebox
from gui_functions import Validate_login

class Login_Screen:
    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager
        self.root.title("Login Screen")

        # Widgets for the Login Screen
        username_label = Label(self.root, text="Username")
        username_label.grid(sticky=E, padx=10, pady=10, row=0, column=0)

        password_label = Label(self.root, text="Password")
        password_label.grid(sticky=E, padx=10, pady=10, row=1, column=0)

        self.username_ent = Entry(self.root)
        self.username_ent.grid(row=0, column=1)

        self.password_ent = Entry(self.root, show="*")
        self.password_ent.grid(row=1, column=1)

        self.login_status = Label(self.root, text="")
        self.login_status.grid(sticky="ew", padx=15, pady=15, row=3, column=0, columnspan=2)

        login_btn = Button(self.root, text="Login", command=self.login)
        login_btn.grid(row=2, column=1, sticky="ew")

    def login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        self.username_ent.delete(0, END)
        self.password_ent.delete(0, END)

        # Example validation logic
        access_level = Validate_login(username, password)
        if access_level == 1:
            self.login_status.config(text=f"Welcome, {username}!")
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.window_manager.show_owner_screen()  
        elif access_level == 0:
            messagebox.showinfo("Incorrect Login", "Incorrect Username or password")
            self.login_status.config(text="Incorrect Username or password")
        elif access_level == 2:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!") 
            self.window_manager.show_employee_screen(username) # TODO
        else:
            messagebox.showinfo("Access Denied", "You do not have the required permissions.")
