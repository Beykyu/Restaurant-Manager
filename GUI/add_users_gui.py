import tkinter as tk
from tkinter import messagebox
from gui_functions import add_user

# TODO Allow viewing, editing and deletion of users
class AddUserGUI:
    def __init__(self, root: tk.Tk, window_manager) -> None:
        self.root = root
        self.window_manager = window_manager
        self.root.title("Add New User")
        self.root.geometry("400x500")

        # Title
        tk.Label(self.root, text="Add A New User", font=("Arial", 16)).pack(pady=10)

        # Name
        tk.Label(self.root, text="Name").pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=5)

        # Username
        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Permission Level with Dropdown
        tk.Label(self.root, text="Permission Level").pack(pady=5)
        self.permission_levels = [1, 2, 3] #TODO Adjust permission levels for application
        self.selected_permission = tk.StringVar(self.root)
        self.selected_permission.set(self.permission_levels[0])  # Default value
        permission_dropdown = tk.OptionMenu(self.root, self.selected_permission, *self.permission_levels)
        permission_dropdown.pack(pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Back Button
        back_button = tk.Button(button_frame, text="Back", command=self.go_back, bg="gray", fg="white")
        back_button.pack(side=tk.LEFT, padx=10)

        # Add User Button
        add_user_button = tk.Button(button_frame, text="Add User", command=self.add_user, bg="green", fg="white")
        add_user_button.pack(side=tk.LEFT, padx=10)

    # Callback for the Back button
    def go_back(self) -> None:
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_manage_users()

    def add_user(self) -> None:
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        permission = self.selected_permission.get()
        # Ensure all fields are filled and then calls the function to add user to database
        try:
            if not (name and username and password and permission):
                raise Exception("All fields are required!")
            else:
                add_user(name, username, password, permission)
                messagebox.showinfo("Success", "User added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
