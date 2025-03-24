from tkinter import *
import json
from tkinter import messagebox
from gui_functions import add_item_to_database

class New_Item:
    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager

        with open('MISC/tags.json','r') as file:
            data = json.load(file)

        self.available_tags = data["tags"]
        self.selected_tags = []

        # Initialize the main window
        self._setup_main_window()

    def _setup_main_window(self):
        """Set up the main window and its components."""
        self.root.title("New Item")
        self.root.geometry("500x400")

        # Input fields
        self._create_input_fields()

        # Tag management
        self._create_tag_management()

        # Action buttons
        self._create_action_buttons()

    def _create_input_fields(self):
        """Create and place input fields for menu item details."""
        Label(self.root, text="Menu Item Number").grid(sticky=E, padx=10, pady=10, row=0, column=0)
        Label(self.root, text="Menu Item Name").grid(sticky=E, padx=10, pady=10, row=1, column=0)
        Label(self.root, text="Price (£)").grid(sticky=E, padx=10, pady=10, row=2, column=0)

        self.menu_no_entry = Entry(self.root)
        self.menu_no_entry.grid(row=0, column=1)

        self.menu_name_entry = Entry(self.root)
        self.menu_name_entry.grid(row=1, column=1)

        self.price_entry = Entry(self.root)
        self.price_entry.grid(row=2, column=1)

    def _create_tag_management(self):
        """Create and place widgets for managing tags side by side."""
        tag_management_frame = Frame(self.root)  
        tag_management_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Selected Tags (Left)
        Label(tag_management_frame, text="Selected Tags:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.selected_tags_listbox = Listbox(tag_management_frame, height=10, width=25)  
        self.selected_tags_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Buttons for Adding and Removing Tags (Center)
        button_frame = Frame(tag_management_frame)
        button_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        Button(button_frame, text="Add Tag →", command=self.add_tags).pack(pady=5)
        Button(button_frame, text="← Remove Tag", command=self.remove_tags).pack(pady=5)

        # Available Tags (Right)
        Label(tag_management_frame, text="Available Tags:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.available_tags_listbox = Listbox(tag_management_frame, height=10, width=25) 
        self.available_tags_listbox.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        # Populate Available Tags Listbox
        for tag in self.available_tags:
            self.available_tags_listbox.insert(END, tag)

    def _create_action_buttons(self):
        """Create and place action buttons for the window."""
        Button(self.root, text="Add Menu Item", command=self.add_item).grid(row=7, column=0, padx=10, pady=10)
        Button(self.root, text="Back", command=self.owner_gui_return).grid(row=7, column=1, padx=10, pady=10)

    def add_tags(self):
        """Add selected tags from the available listbox to the selected tags listbox."""
        selected_indices = self.available_tags_listbox.curselection()
        selected_tags = [self.available_tags[index] for index in selected_indices]

        for tag in selected_tags:
            if tag not in self.selected_tags:  # Avoid duplicates
                self.selected_tags.append(tag)
                self.selected_tags_listbox.insert(END, tag)
                self.available_tags.remove(tag)
        self._refresh_available_tags_listbox()

    def remove_tags(self):
        """Remove selected tags from the selected tags listbox."""
        selected_indices = list(self.selected_tags_listbox.curselection())
        selected_tags = [self.selected_tags_listbox.get(index) for index in selected_indices]

        for tag in selected_tags:
            self.selected_tags.remove(tag)
            self.available_tags.append(tag)

        self._refresh_selected_tags_listbox()
        self._refresh_available_tags_listbox()

    def _refresh_available_tags_listbox(self):
        """Refresh the available tags listbox."""
        self.available_tags_listbox.delete(0, END)
        for tag in self.available_tags:
            self.available_tags_listbox.insert(END, tag)

    def _refresh_selected_tags_listbox(self):
        """Refresh the selected tags listbox."""
        self.selected_tags_listbox.delete(0, END)
        for tag in self.selected_tags:
            self.selected_tags_listbox.insert(END, tag)

    def owner_gui_return(self):
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_owner_screen()

    def add_item(self):
        """Display confirmation dialog and add the new menu item to the database."""
        popup = Toplevel(self.root)
        popup.title("Confirmation")
        popup.geometry("400x250")
        
        message = Label(
            popup, text=f"""Are you sure you want to add this item?\n
                            Menu Number: {self.menu_no_entry.get()} \n
                            Name: {self.menu_name_entry.get()}\n
                            Price: £{self.price_entry.get()}\n
                            Tags: {", ".join(self.selected_tags)}"""
        )
        message.pack(pady=10)

        # Functions to handle the confirmation button actions
        def confirm_add():
            """Adds the menu item details to the menu database"""
            try:
                if not self.selected_tags:
                    self.selected_tags = ["None"]
                add_item_to_database(
                    self.menu_no_entry.get(),
                    self.menu_name_entry.get(),
                    self.price_entry.get(),
                    self.selected_tags
                )
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                popup.destroy()

        def cancel_add():
            popup.destroy()

        Button(popup, text="Yes", command=confirm_add).pack(side=LEFT, padx=20, pady=20)
        Button(popup, text="No", command=cancel_add).pack(side=RIGHT, padx=20, pady=20)