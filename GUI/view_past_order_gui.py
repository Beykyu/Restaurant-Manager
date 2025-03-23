import sys
import os
from datetime import date
import json
from typing import List, Optional, Tuple

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from gui_functions import get_past_order, get_past_order_items
from Classes.CustomerOrder import CustomerOrder
import Classes.MenuItems
import Classes.MenuItemOrder
import tkinter as tk

#TODO Clean up UI, consider adding more ways of viewing different stats 
class PastOrdersGUI:
    """
    A GUI application for viewing and managing past orders.

    This class provides a graphical interface for viewing historical order data,
    including order details, items, and daily earnings.

    Attributes:
        root (tk.Tk): The main window of the application.
        window_manager: The manager handling window transitions.
        past_orders (List[CustomerOrder]): List of retrieved past orders.
        current_selected_order (Optional[CustomerOrder]): Currently selected order.
    """

    def __init__(self, root: tk.Tk, windows_manager =None) -> None:
        """
        Initialize the PastOrdersGUI.

        Args:
            root (tk.Tk): The main window of the application.
            windows_manager: The manager handling window transitions.
        """
        self.root = root
        self.window_manager = windows_manager
        self.past_orders: List[CustomerOrder] = []
        self.current_selected_order: Optional[CustomerOrder] = None
        
        self._setup_main_window()
        self._setup_ui_components()
        self._load_current_date_orders()

    def _setup_main_window(self) -> None:
        """Configure the main window properties."""
        self.root.title("View Past orders")
        self.root.geometry("1000x700")

    def _setup_ui_components(self) -> None:
        """Set up all UI components of the application."""
        self._setup_orders_section()
        self._setup_search_section()
        self._setup_items_section()
        self._setup_details_section()
        self._setup_navigation()

    def _setup_orders_section(self) -> None:
        """Set up the orders list section."""
        self.orders_listbox = tk.Listbox(self.root, width=30, height=15)
        self.orders_listbox.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        self.orders_listbox.bind('<<ListboxSelect>>', self.on_order_select)

        self.total_price_label = tk.Label(
            self.root, 
            text="Total Earnings: £0.00", 
            font=("Arial", 12), 
            anchor="w"
        )
        self.total_price_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    def _setup_search_section(self) -> None:
        """Set up the date search section."""
        self.search_label = tk.Label(self.root, text="Enter date (YYYY-MM-DD):")
        self.search_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.search_entry = tk.Entry(self.root, width=20)
        self.search_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.search_button = tk.Button(
            self.root, 
            text="Search", 
            command=self.search_past_orders_box
        )
        self.search_button.grid(row=3, column=0, sticky="e", padx=10, pady=5)

    def _setup_items_section(self) -> None:
        """Set up the order items display section."""
        self.items_listbox_label = tk.Label(self.root, text="Order Items")
        self.items_listbox_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.items_listbox = tk.Listbox(self.root, width=40, height=20)
        self.items_listbox.grid(row=1, column=1, padx=10, pady=5)

    def _setup_details_section(self) -> None:
        """Set up the order details display section."""
        self.order_details_label = tk.Label(self.root, text="Order Details")
        self.order_details_label.grid(row=0, column=2, padx=10, pady=5)
        
        self.order_details_text = tk.Text(
            self.root, 
            width=30, 
            height=15, 
            wrap="word", 
            state="disabled"
        )
        self.order_details_text.grid(row=1, column=2, padx=10, pady=5)

    def _setup_navigation(self) -> None:
        """Set up navigation buttons."""
        self.back_button = tk.Button(
            self.root, 
            text="Back", 
            command=self.go_back, 
            bg="gray", 
            fg="white"
        )
        self.back_button.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    def _load_current_date_orders(self) -> None:
        """Load orders for the current date."""
        current_date = date.today()
        self.retrieve_past_orders(current_date)

    def retrieve_past_orders(self, date_str: str) -> None:
        """
        Retrieve past orders from the database for a specific date.

        Args:
            date_str: The date to retrieve past orders from (YYYY-MM-DD format).
        """
        order_list: List[Tuple] = get_past_order(date_str)
        self.past_orders.clear()
        
        for order in order_list:
            employee_id, order_id, time_of_order, item_count = order
            menu_item_list = self._get_order_items(order_id)
            self.past_orders.append(
                CustomerOrder(
                    employee_id, 
                    order_id, 
                    menu_items=menu_item_list,
                    date_time=time_of_order, 
                    total_items=item_count
                )
            )
        
        total = self.get_day_total()
        self.total_price_label.config(text=f"Total Earnings: £{total:.2f}")
        self.update_past_orders_listbox()

    def _get_order_items(self, order_id: int) -> List[Classes.MenuItemOrder.MenuItemOrder]:
        """
        Retrieve and parse items for a specific order.

        Args:
            order_id: The ID of the order to retrieve items for.

        Returns:
            List of MenuItemOrder objects.
        """
        items = get_past_order_items(order_id)
        menu_item_list = []
        
        for item in items:
            menu_no, product_name, quantity, price, modifications = item
            modifications = json.loads(modifications) if isinstance(modifications, str) else {}
            
            menu_item = Classes.MenuItems.MenuItems(menu_no, product_name, price, [])
            order_item = Classes.MenuItemOrder.MenuItemOrder(
                menu_item, 
                quantity, 
                modifications
            )
            menu_item_list.append(order_item)
            
        return menu_item_list

    def search_past_orders_box(self) -> None:
        """
        Retrieves date input from the search box and then retrieves past orders from that date.
        """
        date_str = self.search_entry.get().strip()
        if not date_str:
            return
        self.retrieve_past_orders(date_str)

    def update_past_orders_listbox(self) -> None:
        """Update the orders listbox with past orders."""
        self.orders_listbox.delete(0, tk.END)
        self.order_data = {}  # Store order data for quick access
        for order in self.past_orders:
            display_text = f"ID: {order.order_id}, Time: {order.get_time()}, Total: £{order.totalprice:.2f}"
            self.orders_listbox.insert(tk.END, display_text)

    def update_order_details_listbox(self) -> None:
        """Display the details of the selected order."""
        order = self.current_selected_order
        if not order:
            return

        self.order_details_text.config(state="normal")  # Enable editing temporarily
        self.order_details_text.delete("1.0", tk.END)  

        self.order_details_text.insert(tk.END, f"Order ID: {order.order_id}\n")
        self.order_details_text.insert(tk.END, f"Date: {order.get_date()}\n")
        self.order_details_text.insert(tk.END, f"Time: {order.get_time()}\n")
        self.order_details_text.insert(tk.END, f"Employee ID: {order.employeeID}\n")
        self.order_details_text.insert(tk.END, f"Total Items: {order.total_items}\n")
        self.order_details_text.insert(tk.END, f"Total Price: £{order.totalprice:.2f}\n")

        self.order_details_text.config(state="disabled")  # Disable editing again

    def update_order_items_listbox(self) -> None:
        """Display the items of the selected order."""
        order = self.current_selected_order
        if not order:
            return

        self.items_listbox.delete(0, tk.END)    
        for item in order.menu_items:
            self.items_listbox.insert(
                tk.END, f"{item.quantity} x {item.menuName} - £{item.total_price:.2f}"
            )
            if item.modifications:
                for mod in item.modifications:
                    self.items_listbox.insert(tk.END, f"    - {mod}")

    def on_order_select(self, event) -> None:
        """Display the details and items of the selected order."""
        selected_idx = self.orders_listbox.curselection()
        if not selected_idx:
            return

        selected_order_text = self.orders_listbox.get(selected_idx[0])
        order_id = int(selected_order_text.split("ID:")[1].split(",")[0].strip())
        self.current_selected_order = next(
            (order for order in self.past_orders if order.order_id == order_id), 
            None
        )
        self.update_order_items_listbox()
        self.update_order_details_listbox()

    def get_day_total(self) -> float:
        """Calculate the total earnings for the day."""
        total: float = 0.00
        for order in self.past_orders:
            total += order.totalprice   
        return total
    
    def go_back(self) -> None:
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_owner_screen()