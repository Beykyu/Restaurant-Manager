import tkinter as tk
from gui_functions import fetch_menu_items, add_customer_order, get_mod_from_tag
from tkinter import messagebox
import Classes.MenuItems
import Classes.MenuItemOrder
from Classes.CustomerOrder import CustomerOrder
import json
import copy

class EmployeeGui:
    """
    A graphical user interface for employee operations in the restaurant management system.
    
    This class handles:
    - Displaying and managing customer orders
    - Menu item selection and modification
    - Order processing and checkout
    """
    
    def __init__(self, root: tk.Tk, window_manager, employeeID: str) -> None:
        """
        Initialize the employee GUI.

        Args:
            root: The main window of the application
            window_manager: The window management system
            employeeID: Unique identifier for the employee
        """
        self.root = root
        self.window_manager = window_manager

        try:
            with open('MISC/tags.json', 'r') as file:
                data = json.load(file)
            self.tags = data["tags"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tags.json: {e}")
            self.tags = []
        
        # Add customer order instance
        self.current_order = CustomerOrder(employeeID)
        
        # Frame for customer order on the left
        self.customer_order_frame = tk.Frame(root, borderwidth=1, relief="solid")
        self.customer_order_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.customer_order_label = tk.Label(self.customer_order_frame, text="Customer Order", font=("Arial", 14))
        self.customer_order_label.pack(pady=5)

        self.customer_order_listbox = tk.Listbox(self.customer_order_frame, font=("Courier", 12), height=15)
        self.customer_order_listbox.pack(expand=True, fill="both")

        # Add buttons and total price
        buttons_frame = tk.Frame(self.customer_order_frame)
        buttons_frame.pack(pady=5, fill="x")  # Ensure the frame stretches horizontally

        # Configure grid layout for buttons_frame
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

        # Add "+" button
        self.add_item_button = tk.Button(buttons_frame, text="Add +", font=("Arial", 10), height=4, bg="green", fg="white", command=self.add_item)
        self.add_item_button.grid(row=0, column=0, sticky="nsew")

        # Add "Modify item" button
        self.modify_item_button = tk.Button(buttons_frame, text="Modify item", font=("Arial", 10), height=4, bg="yellow", fg="black", command=self.modify_item)
        self.modify_item_button.grid(row=0, column=1, sticky="nsew")

        # Add "-" button
        self.remove_item_button = tk.Button(buttons_frame, text="Remove -", font=("Arial", 10), height=4, bg="red", fg="white", command=self.remove_item)
        self.remove_item_button.grid(row=0, column=2, sticky="nsew")

        # "Accept Order" button and total price label
        self.accept_order_button = tk.Button(buttons_frame, text="Accept Order", font=("Arial", 10), command= lambda: self.accept_order(employeeID), height=4, bg="blue", fg="white")
        self.accept_order_button.grid(row=1, column=0, sticky="nsew", padx=5)

        self.total_price_label = tk.Label(buttons_frame, text="Total Price: £0.00", font=("Arial", 12, "bold"), anchor="w")
        self.total_price_label.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=5)

        # Move "Log Out" button to the bottom of the frame
        self.log_out_button = tk.Button(self.customer_order_frame, text="Log Out", font=("Arial", 10), command=self.go_back)
        self.log_out_button.pack(pady=10, fill="x")

        # Frame for menu items in the middle
        self.menu_items_frame = tk.Frame(root, borderwidth=1, relief="solid")
        self.menu_items_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.menu_items_label = tk.Label(self.menu_items_frame, text="Menu Items", font=("Arial", 14))
        self.menu_items_label.pack(pady=5)

        self.menu_items_listbox = tk.Listbox(self.menu_items_frame, font=("Courier", 12))
        self.menu_items_listbox.pack(expand=True, fill="both")

        # Frame for buttons on the right
        self.buttons_frame = tk.Frame(root, borderwidth=1, relief="solid")
        self.buttons_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        self.create_buttons()

        # Configure grid weights for resizing
        root.grid_columnconfigure(0, weight=5)  
        root.grid_columnconfigure(1, weight=5)  
        root.grid_columnconfigure(2, weight=2)  
        root.grid_rowconfigure(0, weight=1)     # Allow vertical resizing
        
        for i in range(10):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Bind click event to menu_items_listbox
        self.menu_items_listbox.bind("<ButtonRelease-1>", self.add_item_from_menu)

                # Add a search box below the menu items listbox
        self.search_frame = tk.Frame(self.menu_items_frame)
        self.search_frame.pack(fill="x", pady=5)

        self.search_label = tk.Label(self.search_frame, text="Search:", font=("Arial", 10))
        self.search_label.pack(side="left", padx=5)

        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Bind the search entry to call the search function
        self.search_entry.bind("<KeyRelease>", self.search_menu_items)

        self.root.minsize(1000, 700)  # Set minimum window size

        # Add mapping dictionary
        self.listbox_to_menu_map = {}

    def create_button(self, parent, text, command=None, **kwargs) -> tk.Button:
        """Creates a standardized button with common styling."""
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 10),
            command=command,
            **kwargs
        )
        return button

    def create_buttons(self) -> None:
        """Creates a grid of menu category buttons based on available tags."""
        tag_index = 0
        for row in range(10):
            for col in range(3):
                if tag_index < len(self.tags):
                    tag = self.tags[tag_index]
                    button = self.create_button(
                        self.buttons_frame,
                        text=tag,
                        command=lambda t=tag: self.update_menu_items_listbox(t)
                    )
                    tag_index += 1
                else:
                    button = self.create_button(self.buttons_frame, text="")
                button.grid(row=row, column=col, sticky="nsew")

    def update_menu_items_listbox(self, tag: str) -> None:
        """
        Updates the menu items listbox based on selected category tag.

        Args:
            tag: The category tag to filter menu items
        """
        items = fetch_menu_items(tag,2)
        self.update_listbox(self.menu_items_listbox, items)

    def manage_order_item(self, item_action: str) -> None:
        """Manages order item actions (add/remove/modify)."""
        selected_item = self.customer_order_listbox.curselection()
        if not selected_item:
            return

        menu_index = self.listbox_to_menu_map.get(selected_item[0])
        if menu_index is not None:
            order_item = self.current_order.menu_items[menu_index]
            
            if item_action == "add":
                order_item.increment_quantity()
            elif item_action == "remove":
                if order_item.quantity > 1:
                    order_item.decrement_quantity()
                else:
                    self.current_order.delete_item(order_item)
                    
            self.current_order.update_total_items()
            self.refresh_order_display()

            # Reselect the same item if it still exists
            for listbox_idx, menu_idx in self.listbox_to_menu_map.items():
                if menu_idx == menu_index:
                    self.customer_order_listbox.select_set(listbox_idx)
                    break

    def add_item(self) -> None:
        """Increments the quantity of the selected menu item."""
        self.manage_order_item("add")

    def remove_item(self) -> None:
        """Decrements the quantity of the selected menu item or removes it."""
        self.manage_order_item("remove")

    def select_and_prepare_item_for_modification(self) -> bool:
        """
        Selects an item from the customer order listbox and prepares it for modification.
        Returns True if successful, otherwise False.
        """
        # Check if an item is selected in the customer_order_listbox
        selected_item = self.customer_order_listbox.curselection()
        if not selected_item:
            print("No item selected to modify.")
            return False

        # Store the selected item
        selected_index = selected_item[0]
        # Create a deepcopy of the selected item and set its quantity to 1
        self.selected_order_item = copy.deepcopy(self.current_order.menu_items[selected_index])
        self.selected_order_item.set_quantity_to_one() # Update the quantity of the copied item
        self.original_order_item = self.current_order.menu_items[selected_index]  # Hold current item in case it needs to be removed
        self.remove_mod_item_checker = True  # Allows the order item currently being modified to be removed only once
        return True

    def modify_item(self) -> None:
        """
        Switches the interface to Modify mode, allowing customization of selected menu items.
        This method:
        - Checks if an item is selected in the customer order listbox.
        - Prepares the selected item for modification, ensuring its quantity is set to 1.
        - Temporarily stores the original item for potential removal or update.
        - Hides the original menu items listbox and displays a new listbox with customization options.
        - Reads modification tags from a JSON file and populates the modifications listbox.
        - Updates the label and buttons on the interface to reflect the modification mode.
        
        If no item is selected or if there is an issue reading the JSON file, appropriate error handling is performed.
        """
        if not self.select_and_prepare_item_for_modification():
            return

        # Hide the original menu_items_listbox
        self.menu_items_listbox.pack_forget()

        # Create and show the new modifications_listbox
        self.modifications_listbox = tk.Listbox(self.menu_items_frame, font=("Courier", 12))
        self.modifications_listbox.pack(expand=True, fill="both")  
        self.menu_items_label.config(text="Custom item")

        try:
            with open('MISC/mod_tags.json', 'r') as file:
                data = json.load(file)
            self.mod_tags = data.get("tags", [])  # Fallback to an empty list if "tags" is missing
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tags.json: {e}")
            self.mod_tags = []
        # Populate the modifications listbox with modification options for the selected tag
        if self.mod_tags and len(self.mod_tags) > 0:    
            self.handle_column_button(self.mod_tags[0])
        else:
            print("No tags available to display modifications.")

        # Update the buttons on the right
        self.refresh_buttons_layout(self.mod_tags,
                                    ["Add", "No", "Swap", "Save", "Cancel"])


    def add_item_from_menu(self, event: tk.Event) -> None:
        """
        Adds an item to the Customer Order listbox when clicked in the Menu Items listbox.
        If the item already exists in the customer order, increments the quantity instead.
        Deselects the clicked item in the Menu Items listbox after adding.
        """
        selected_item = self.menu_items_listbox.curselection()

        if selected_item:
            # Get the selected item's details
            item_text = self.menu_items_listbox.get(selected_item)
            item_no = item_text.split(":")[0].strip()
            item = fetch_menu_items(item_no, 1)[0]  # Fetch item details
            order_item = Classes.MenuItemOrder.MenuItemOrder(item)  # Create MenuItemOrder object

            # Check if the item already exists in the current order
            for existing_item in self.current_order.menu_items:
                if existing_item.menuName == order_item.menuName and existing_item.modifications == order_item.modifications:
                    # Item already exists, increment the quantity
                    existing_item.increment_quantity()
                    self.current_order.update_total_items()
                    self.refresh_order_display()
                    self.menu_items_listbox.selection_clear(0, tk.END)
                    return

            # If item does not exist, add it to the current order and clears listbox
            self.current_order.add_item(order_item)
            self.refresh_order_display()
            self.menu_items_listbox.selection_clear(0, tk.END)

    def refresh_order_display(self) -> None:
        """
        Updates the customer order listbox with current order items and their modifications.
        Also maintains a mapping of listbox indices to menu item indices.
        """
        self.customer_order_listbox.delete(0, tk.END)
        self.listbox_to_menu_map = {}  # Maps listbox indices to menu item indices
        
        listbox_index = 0
        for menu_index, item in enumerate(self.current_order.menu_items):
            # Store mapping of listbox index to menu item index
            self.listbox_to_menu_map[listbox_index] = menu_index
            
            # Display the main item
            self.customer_order_listbox.insert(
                tk.END, f"{item.quantity} x {item.menuName} - £{item.total_price:.2f}"
            )
            listbox_index += 1
            
            # Display modifications
            if item.modifications:
                for mod in item.modifications:
                    self.customer_order_listbox.insert(tk.END, f"    - {mod}")
                    listbox_index += 1
        self.update_total_price()

    def go_back(self) -> None:
        """
        Logs the user out.
        """
        self.current_order = None
        self.root.destroy()
        self.window_manager.show_login_screen()

    def update_total_price(self) -> None:
        """
        Updates the total price display.
        """
        total_price = self.current_order.totalprice
        self.total_price_label.config(text=f"Total Price: £{total_price:.2f}")

    def accept_order(self, employee: str) -> None:
        """
        Adds the order to the database

        Args:
            employee: The employee who accepted the order
        """
        messagebox.showinfo("Order Accepted", self.current_order.display_order_as_string())
        if add_customer_order(self.current_order):
            self.current_order = CustomerOrder(employee)
            self.refresh_order_display()

    def search_menu_items(self, event: tk.Event) -> None:
        """
        Handles the search functionality.
        This function will filter menu items based on the input in the search box.

        Args:
            event: The event that triggered the search
        """
        search_text = self.search_entry.get().lower()  # Get the current text in the search box
        items = fetch_menu_items('*', 1)  # Fetch all items 
        #Creates a list of all items where their name or menuid is similar or matches the input text
        filtered_items = [
            item for item in items if search_text in item.menuName.lower() or search_text in item.menuNumber.lower()
        ]
        self.update_listbox(self.menu_items_listbox, filtered_items)

    def update_listbox(self, listbox: tk.Listbox, items: list) -> None:
        """
        Updates the given the listbox with the elements in the list provided

        Args:
            listbox: The listbox to update
            items: The items to add to the listbox
        """
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, f"{item.menuNumber}: {item.menuName}")


    def refresh_buttons_layout(self, column_buttons: list, action_buttons: list) -> None:
        """Dynamically update the buttons on the right frame."""
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Create column buttons
        for i, tag in enumerate(column_buttons):
            button = self.create_button(
                self.buttons_frame,
                text=tag,
                command=lambda t=tag: self.handle_column_button(t)
            )
            button.grid(row=i, column=0, columnspan=3, sticky="nsew")

        # Create action buttons
        base_row = len(column_buttons)
        for i, label in enumerate(action_buttons[:3]):
            button = self.create_button(
                self.buttons_frame,
                text=label,
                command=lambda l=label: self.handle_action_button(l)
            )
            button.grid(row=base_row, column=i, sticky="nsew")

        # Create bottom buttons
        for i, label in enumerate(action_buttons[3:]):
            button = self.create_button(
                self.buttons_frame,
                text=label,
                command=lambda l=label: self.handle_action_button(l)
            )
            button.grid(row=base_row + 1 + i, column=0, columnspan=3, sticky="nsew")

        # Configure grid weights
        for i in range(base_row + len(action_buttons)):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.buttons_frame.grid_columnconfigure(j, weight=1)

    def handle_column_button(self, tag: str) -> None:
        """
        Handle clicks on the column buttons (Veg, Sauces, etc.).

        Args:
            tag: The tag for the button clicked.
        """
        self.tag_info = get_mod_from_tag(tag)
        self.modifications_listbox.delete(0, tk.END)
        for tag in self.tag_info:
            self.modifications_listbox.insert(tk.END, f"{tag[0]}: {tag[1]}")


    def handle_action_button(self, label: str) -> None:
        """
        Handle clicks on the action buttons (Add, No, Swap, Cancel, Back).
        Keeps track of modifications to the selected item.

        Args:
            label: The label for the button clicked.
        """
        if label == "Save":
            self._handle_save_action()
        elif label == "Cancel":
            self._handle_cancel_action()
        elif label in ["Add", "No", "Swap"]:
            self._handle_modification_action(label)
        else:
            print(f"Unknown action: {label}")

    def _handle_save_action(self) -> None:
        """Handle the 'Save' button click."""
        self.reset_to_default_layout()
        self.selected_order_item = None
        self.remove_mod_item_checker = True

    def _handle_cancel_action(self) -> None:
        """Handle the 'Cancel' button click."""
        if self.selected_order_item:
            self.current_order.delete_item(self.selected_order_item)
        if not self.remove_mod_item_checker:
            self.current_order.add_item(self.original_order_item)
        self.original_order_item = None
        self.reset_to_default_layout()
        self.selected_order_item = None
        self.remove_mod_item_checker = True

    def _handle_modification_action(self, label: str) -> None:
        """Handle 'Add', 'No', or 'Swap' button clicks."""
        selected_item = self.modifications_listbox.curselection()
        if selected_item:
            selected_index = selected_item[0]
            if selected_index < len(self.tag_info):
                mod_item = self.tag_info[selected_index]
                self._update_modifications(label, mod_item)

    def _update_modifications(self, label: str, mod_item: tuple) -> None:
        """
        Apply modifications to the selected item.

        Args:
            label: The type of modification ('Add', 'No', 'Swap').
            mod_item: The modification details as a tuple (name, cost).
        """
        if self.remove_mod_item_checker:
            self.current_order.delete_item(self.original_order_item)
            self.remove_mod_item_checker = False
        else:
            self.current_order.delete_item(self.selected_order_item)

        # Apply the modification
        if label == "Add":
            self.selected_order_item.add_modification(mod_item[0], float(mod_item[1]), label)
        else:
            self.selected_order_item.add_modification(mod_item[0], 0.00, label)

        self.current_order.add_item(self.selected_order_item)
        self.refresh_order_display()

    def reset_to_default_layout(self) -> None:
        """
        Restore the original layout, including the menu items listbox.
        """
        # Destroy the modifications listbox
        if hasattr(self, 'modifications_listbox'):
            self.modifications_listbox.destroy()
            del self.modifications_listbox

        # Restore the menu_items_listbox
        self.menu_items_listbox.pack(expand=True, fill="both")

        # Update the label back to "Menu Items"
        self.menu_items_label.config(text="Menu Items")

        # Restore the default buttons
        self.create_buttons()

        # Clear the tracked selected order item
        self.selected_order_item = None
        self.refresh_order_display()