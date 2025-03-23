import tkinter as tk
from tkinter import ttk, messagebox
from gui_functions import get_all_user, get_user, update_User

class ManageUsersGUI:
    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager
        self.root.title("Manage Users")
        self.root.geometry("800x400")

        # Variables
        self.username_var = tk.StringVar()  # Holds username dynamically
        self.permission_levels = [1, 2, 3]  #TODO Placeholder permission levels

        self._setup_gui()
        self.fetch_and_display_users()

    def _setup_gui(self):
        """Sets up the entire GUI layout."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

        # Adjust Left Frame: Reduce extra spacing on the right
        left_frame = tk.Frame(self.root, padx=1, pady=10)
        left_frame.grid(row=0, column=0, sticky="ns")

        tk.Label(left_frame, text="Users", font=("Arial", 12), anchor="w").pack(fill=tk.X, pady=5)
        self.user_listbox = tk.Listbox(left_frame, height=20, width=30)
        self.user_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)

        # Right Frame: User Details
        right_frame = tk.Frame(self.root, padx=1, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Center the details section and move it left
        details_frame = tk.Frame(right_frame)
        details_frame.place(relx=0.45, rely=0.5, anchor="center")

        # Adjusting label and entry alignment
        tk.Label(details_frame, text="Name", anchor="w", width=15).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = tk.Entry(details_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=5, padx=5)

        tk.Label(details_frame, text="Username", anchor="w", width=15).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.username_entry = tk.Entry(details_frame, textvariable=self.username_var, width=30, state="readonly")
        self.username_entry.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        tk.Label(details_frame, text="New Password", anchor="w", width=15).grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.password_entry = tk.Entry(details_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        tk.Label(details_frame, text="Permission Level", anchor="w", width=15).grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.permission_level = ttk.Combobox(details_frame, values=self.permission_levels, state="readonly", width=28)
        self.permission_level.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        self.permission_level.set(self.permission_levels[0])  # Default value

        # Buttons
        button_frame = tk.Frame(details_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_button = tk.Button(button_frame, text="Save Changes", command=self.save_changes, bg="green", fg="white")
        save_button.pack(side=tk.LEFT, padx=10)

        add_user_button = tk.Button(button_frame, text="Add User", command=self.go_to_add_user, bg="blue", fg="white")
        add_user_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(button_frame, text="Back", command=self.go_back, bg="gray", fg="white")
        back_button.pack(side=tk.RIGHT, padx=10)

    def fetch_and_display_users(self) -> None:
        """Fetch users from the database and display them in the listbox."""
        users = get_all_user()
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, user[1])

    def on_user_select(self, event):
        """
        Handle user selection from the listbox.
        Populates the selected user details.
        """
        selected_index = self.user_listbox.curselection()
        if selected_index:
            selected_user = self.user_listbox.get(selected_index[0])
            self.username_var.set(selected_user)  # Dynamically update username
            user_info = get_user(selected_user)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, user_info[0]) 
            self.password_entry.delete(0, tk.END)  
            self.permission_level.set(user_info[3]) 

    def save_changes(self):
        """Save changes made to user details to the database"""
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        permission = self.permission_level.get()

        try:
            if not (name and username and permission):
                raise Exception("All fields are required!")
            update_User(name, username, password, permission)
            messagebox.showinfo("Success", "User successfully updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_to_add_user(self):
        """Navigate to the Add User screen."""
        self.root.withdraw()  
        self.window_manager.show_add_users()  

    def go_back(self):
        """Navigate back to the previous screen."""
        self.root.destroy() 
        self.window_manager.show_owner_screen()  
