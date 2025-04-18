import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import json
from gui_functions import add_mod_to_database, get_mod_from_tag, remove_mod

class EditModsGUI():

    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager
        self.root.title("Modification Editor")

        # Create GUI elements
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=15)
        self.listbox.pack(pady=10)

        # Buttons
        self.add_button = tk.Button(root, text="Add modification", command=self.add_mod)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Selected Modification", command=self.remove_mod)
        self.remove_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Go back", command=self.owner_gui_return)
        self.save_button.pack(pady=5)
        
        self.update_listbox()

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

            # Validate inputs
            if not name or not tag:
                messagebox.showwarning("Warning", "Please fill in all the fields and try again.")
                return

            try:
                cost = float(cost)  # Convert cost to a float
            except ValueError:
                messagebox.showwarning("Warning", "Please make sure the cost is a valid number.")
                return

            # Add modification to the database
            if add_mod_to_database(name, cost, tag):
                messagebox.showinfo("Success", f"{name} added successfully.")
                self.update_listbox()
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Failed to add modification. Please try again.")

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

        # Handle default value for tags
        selected_tag_var = tk.StringVar(value=tags[0] if tags else "Select a Tag")

        # Combobox for tags
        combobox = ttk.Combobox(popup, textvariable=selected_tag_var, values=tags, state="readonly")  # Read-only so users can only pick options
        combobox.grid(row=2, column=1, padx=10, pady=10)
        combobox.current(0)  # Set the default selection to the first tag

        # Submit button
        tk.Button(popup, text="Submit", command=submit).grid(row=2, column=2, columnspan=2, pady=10)

        popup.mainloop()

    def remove_mod(self):
        """
        Remove the modification from the database.
        """
        selected_index = self.listbox.curselection()
        sorted_mods = sorted(self.mods) #Need to create a sorted list of mods otherwise index will be incorrect

        if selected_index:
            mod_to_remove = sorted_mods[selected_index[0]][0]
            if remove_mod(mod_to_remove):
                messagebox.showinfo("Success!", f"{mod_to_remove} successfully removed")
            else:
                messagebox.showerror("Error", "Could not remove the selected modification")
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "No mod selected!")


    def update_listbox(self):
        """
        Refresh the listbox to display the current mods.
        """
        self.mods = get_mod_from_tag("*")
        self.listbox.delete(0, tk.END)
        for mod in sorted(self.mods):  # Sorting tags for consistent display
            cleaned_mod = (mod[0].strip("{}"), *mod[1:])
            display_text = f"{cleaned_mod[0]} {mod[1]} {mod[2]}" 
            self.listbox.insert(tk.END, display_text)

    def owner_gui_return(self):
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_owner_screen()
