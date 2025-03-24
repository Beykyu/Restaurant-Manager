import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from gui_functions import add_mod_to_database

class EditModsGUI():

    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager
        self.root.title("Modification Editor")

        # Create GUI elements
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=15)
        self.listbox.pack(pady=10)

        # Add existing tags to the listbox
        self.update_listbox()

        # Buttons
        self.add_button = tk.Button(root, text="Add modification", command=self.add_mod)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Selected Modification", command=self.remove_mod)
        self.remove_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Go back", command=self.owner_gui_return)
        self.save_button.pack(pady=5)

    def get_tags(self) -> set[tuple]:
        """
        Retrieves the currently saved tags.
        Returns:
            tags(set[str]): A set of all tags currently on file.
        """
        pass


    def get_modifications(self) -> list[tuple]:
        """
        Retrieves all the modifications from the database
        Returns:
             list[tuple]: A list of tuples that contains the name, cost and tag of each modification in the database
        """
        pass

    #TODO Fix bug where dropdown not displaying menu correctly
    def add_mod(self) -> None:
        """
        Prompt the user to enter a new menu modification and add it to the database.
        """
        def submit():
            # Retrieve user inputs
            name = name_entry.get()
            cost = number_entry.get()
            tag = selected_tag_var.get()
            if name and cost and tag:
                if add_mod_to_database(name, cost, tag) :
                    messagebox.showinfo("Success", "Modification added successfully")
                    popup.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill in all the fields.")

        # Create the popup window
        popup = tk.Tk()
        popup.title("Enter Modification name and Cost")

        # Create labels and input fields
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(popup, text="Cost:").grid(row=1, column=0, padx=10, pady=10)
        number_entry = tk.Entry(popup)
        number_entry.grid(row=1, column=1, padx=10, pady=10)

        # Dropdown for tags
        tk.Label(popup, text="Tag:").grid(row=2, column=0, padx=10, pady=10)
        try:
            with open('MISC/mod_tags.json', 'r') as file:
                data = json.load(file)
            tags = data.get("tags", [""])  # Fallback to an empty list if "tags" is missing
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tags.json: {e}")
        selected_tag_var = tk.StringVar(value=tags[0])
        dropdown = tk.OptionMenu(popup, selected_tag_var, *tags)
        dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Add a submit button
        tk.Button(popup, text="Submit", command=submit).grid(row=2, column=2, columnspan=2, pady=10)

        # Run the popup window
        popup.mainloop()

    def remove_mod(self):
        """
        Remove the modification from the database.
        """
        pass

    def update_listbox(self):
        """
        Refresh the listbox to display the current mods.
        """
        pass

    def owner_gui_return(self):
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_owner_screen()