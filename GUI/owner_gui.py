from tkinter import *
from tkinter import messagebox
from gui_functions import fetch_menu_items, update_item_in_database
from Classes.MenuItems import MenuItems
import json

class Owner_Gui:
    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager

        # Initialize GUI
        self._setup_main_window()
        self._setup_menu_list_and_details()
        self._setup_tags_frame()
        self._setup_available_tags_frame()

        # Load tags and menu items
        with open('MISC/tags.json','r') as file:
            data = json.load(file)
        self.available_tags = data["tags"]
        
        self.menu_items = fetch_menu_items("*",0)
        self.populate_menu_listbox()

    def _setup_main_window(self):
        """Set up the main window."""
        self.root.title("Menu Management")
        self.root.geometry("1200x600")  # Adjusted for better spacing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        Label(self.root, text="Welcome to the Owner GUI!").grid(row=0, column=0, columnspan=4, pady=10)

    def _setup_menu_list_and_details(self):
        """Create the menu items and details frames."""
        # Menu List Frame
        menu_list_frame = Frame(self.root)
        menu_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        Label(menu_list_frame, text="Menu Items:").grid(row=0, column=0, padx=5, pady=5)
        self.listbox = Listbox(menu_list_frame, height=20, width=40)
        self.listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)

        # Details Frame
        details_frame = Frame(self.root)
        details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        Label(details_frame, text="Menu Number:").grid(row=0, column=0, padx=5, pady=5)
        self.menu_number_label = Label(details_frame, text="")
        self.menu_number_label.grid(row=0, column=1, padx=5, pady=5)

        Label(details_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.menu_name_entry = Entry(details_frame, width=30)
        self.menu_name_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(details_frame, text="Price (£):").grid(row=2, column=0, padx=5, pady=5)
        self.menu_price_entry = Entry(details_frame, width=30)
        self.menu_price_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons below Details Frame
        buttons_frame = Frame(details_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(buttons_frame, text="Save Changes", command=self.save_changes).pack(side=LEFT, padx=5) 
        Button(buttons_frame, text="Add Item", command=self.add_new_item).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Add User", command=self.add_new_user).pack(side=LEFT, padx=5) 
        Button(buttons_frame, text="Logout", command=self.logout).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="View Past Orders", command=self.view_past_orders).pack(side=LEFT, padx=5)

    def _setup_tags_frame(self):
        """Create the tags listbox and its controls."""
        tags_frame = Frame(self.root)
        tags_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        Label(tags_frame, text="Tags:").grid(row=0, column=0, padx=5, pady=5)
        self.tags_listbox = Listbox(tags_frame, height=20, width=30, selectmode=MULTIPLE)  # Consistent width
        self.tags_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        Button(tags_frame, text="Remove Tags", command=self.remove_tags).grid(row=2, column=0, pady=10)

    def _setup_available_tags_frame(self):
        """Create the available tags listbox and its controls."""
        available_tags_frame = Frame(self.root)
        available_tags_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        Label(available_tags_frame, text="Available Tags:").grid(row=0, column=0, padx=5, pady=5)
        self.available_tags_listbox = Listbox(available_tags_frame, height=20, width=30, selectmode=MULTIPLE)  # Consistent width
        self.available_tags_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        Button(available_tags_frame, text="Add Tags", command=self.add_tags).grid(row=2, column=0, pady=10)

    def populate_menu_listbox(self):
        """Populate the menu items listbox."""
        self.listbox.delete(0, END)
        for item in self.menu_items:
            self.listbox.insert(END, f"{item.menuNumber}: {item.menuName}")

    def on_item_select(self, event):
        """Handle selection of a menu item."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.menu_items[selected_index[0]]
            self._update_details(selected_item)
            self.refresh_tag_listboxes(selected_item)

    def add_tags(self):
        """Add selected tags to the current selected menu item."""
        item = self._get_selected_menu_item()
        if not item:
            return
        
        #Gets all the currently selected tags to be added to the current menu item
        selected_tags = [self.available_tags_listbox.get(i) for i in self.available_tags_listbox.curselection()]
        if not selected_tags:
            messagebox.showerror("Error", "No available tags are selected!")
            return

        item.menuTags.extend(selected_tags) #combines the 2 lists
        item.menuTags = list(set(item.menuTags))  # Remove duplicates by changing to set and then back to list
        update_item_in_database(item)

        self.refresh_tag_listboxes(item)
        messagebox.showinfo("Success", "Tags added successfully!")

    def remove_tags(self):
        """Remove selected tags from the current menu item."""
        item = self._get_selected_menu_item()
        if not item:
            return

        #Creates a list of tags to remove
        selected_tags = [self.tags_listbox.get(i) for i in self.tags_listbox.curselection()]
        if not selected_tags:
            messagebox.showerror("Error", "No tags are selected to remove!")
            return

        #Removes tags that were selected and updates the menu item in database
        item.menuTags = [tag for tag in item.menuTags if tag not in selected_tags]
        update_item_in_database(item)

        self.refresh_tag_listboxes(item)
        messagebox.showinfo("Success", "Tags removed successfully!")

    def save_changes(self):
        """Updates any changes to the menu item's name and price."""
        item = self._get_selected_menu_item()
        if not item:
            return

        try:
            item.menuName = self.menu_name_entry.get().strip()
            item.menuPrice = float(self.menu_price_entry.get().strip())
            update_item_in_database(item)
            self.populate_menu_listbox()
            messagebox.showinfo("Success", "Changes successfully saved!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for price!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_tag_listboxes(self, item : MenuItems):
        """Refresh both the tags and available tags listboxes of the given menu item that is selected
            Args:
                item (MenuItems) : The menu item which has been selected
        """
        self.tags_listbox.delete(0, END)
        self.available_tags_listbox.delete(0, END)

        for tag in item.menuTags:
            self.tags_listbox.insert(END, tag)

        used_tags = set(item.menuTags)
        for tag in self.available_tags:
            if tag not in used_tags:
                self.available_tags_listbox.insert(END, tag)

    def _update_details(self, item : MenuItems) -> None:
        """Update the details frame fields with the selected menu item's details."""
        self.menu_number_label.config(text=item.menuNumber)
        self.menu_name_entry.delete(0, END)
        self.menu_name_entry.insert(0, item.menuName)
        self.menu_price_entry.delete(0, END)
        self.menu_price_entry.insert(0, f"{item.menuPrice:.2f}")

    def _get_selected_menu_item(self):
        """Retrieve the currently selected menu item."""
        menu_number = self.menu_number_label.cget("text")
        if not menu_number:
            messagebox.showerror("Error", "No menu item is selected!")
            return None
        return next((item for item in self.menu_items if item.menuNumber == menu_number), None)

    def add_new_item(self):
        """Navigate to the Add Item screen."""
        self.root.withdraw()
        self.window_manager.show_add_item_screen()

    def add_new_user(self):
        """Navigate to the Add User screen."""
        self.root.withdraw()
        self.window_manager.show_manage_users() 

    def logout(self):
        """Log out of the application."""
        self.root.destroy()
        self.window_manager.show_login_screen()

    def view_past_orders(self):
        """Navigate to the Past Orders screen."""
        self.root.withdraw()
        self.window_manager.show_past_orders_screen()