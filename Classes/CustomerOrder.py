from datetime import datetime
from typing import List, Optional
from Classes.MenuItemOrder import MenuItemOrder

class CustomerOrder:
    """
    Represents a customer's order with multiple menu items.
    
    Attributes:
        employeeID (str): ID of employee handling order
        order_id (str): Unique order identifier
        menu_items (List[MenuItemOrder]): List of ordered items
        datetime (datetime): Order timestamp
        totalprice (float): Total price of the order
        total_items (int): Total quantity of items in order
    """
    
    def __init__(self, 
                 employeeID: str, 
                 order_id: Optional[int] = None, 
                 menu_items: Optional[List[MenuItemOrder]] = None, 
                 date_time: Optional[datetime] = None,
                 total_items: int = 0):
        """
        Initialize the CustomerOrder object.

        Args:
            employeeID (str): The ID of the employee handling the order, typically the username.
            order_id (int, optional): The unique identifier for the order.
            menu_items (list[MenuItemOrder], optional): List of MenuItemOrder objects.
            date_time (datetime, optional): Order datetime, defaults to current time.
            totalprice (float, optional): Initial total price, recalculated if items exist.

        Raises:
            TypeError: If employeeID is not an str or menu_items is not a list.
            ValueError: If employeeID is negative.
        """
        if not isinstance(employeeID, str):
            raise TypeError("employeeID must be a string")
        if employeeID == '':
            raise ValueError("employeeID cannot be empty")
        if menu_items is not None and not isinstance(menu_items, list):
            raise TypeError("menu_items must be a list or None")
            
        self.__employeeID = employeeID
        self.__order_id = order_id
        self._menu_items = menu_items or []
        self.__datetime = date_time or datetime.now() #Ensure datetime is set to current time if not provided
        self._totalprice = self.calculate_total()  # Always calculate from items
        self._total_items = total_items

        # Additional validation
        if order_id is not None and not isinstance(order_id, int):
            raise TypeError("order_id must be a int or None")
        if date_time is not isinstance(date_time, datetime):
            raise TypeError("date_time must be a datetime object")
        if menu_items:
            if not all(isinstance(item, MenuItemOrder) for item in menu_items):
                raise TypeError("All items in menu_items must be MenuItemOrder instances")

    @property
    def employeeID(self):
        return self.__employeeID

    @property
    def order_id(self):
        return self.__order_id

    @property
    def menu_items(self):
        return self._menu_items

    @menu_items.setter
    def menu_items(self, items):
        """
        Replaces all menu items with different ones and recalculate the total price.

        :param items: A list of MenuItemOrder objects.
        """
        self._menu_items = items
        self._totalprice = self.calculate_total()

    @property
    def datetime(self):
        return self.__datetime
    
    def get_date(self):
        """
        Gets the date portion of the datetime object
        """
        return self.__datetime.date()
    
    def get_time(self):
        """
        Gets the time portion of the datetime object
        """
        return self.__datetime.time()

    @property
    def totalprice(self) -> str:
        """
        Calculate the total price of the order.

        :return: The total price as a float.
        """
        return self.calculate_total()

    @totalprice.setter
    def totalprice(self, value):
        """
        Prevent direct setting of total price; force recalculation instead.
        """
        raise AttributeError("Total price cannot be set directly. Use calculate_total() method instead.")

    def calculate_total(self):
        """
        Calculate the total price of the order. Sums all the prices of all the items in the order

        :return: The total price as a float.
        """
        total = 0.00
        for item in self._menu_items:
            total += item.total_price
        return round(total,2)
    
    @property
    def total_items(self):
        return self._total_items
    
    @total_items.setter
    def total_items(self, value):
        """
        Prevent direct setting of total number of items; force recalculation instead.
        """
        raise AttributeError("Total items cannot be set directly. Use update_total_items() method instead.")
    
    def update_total_items(self) -> None:
        """
        Updates the number of total items that are in the order
        """
        self._total_items = sum(item.quantity for item in self.menu_items)

    def add_item(self, menu_item_order: MenuItemOrder) -> None:
        """
        Add a MenuItemOrder to the order or increment quantity if exists.

        Args:
            menu_item_order (MenuItemOrder): The item to add

        Raises:
            TypeError: If menu_item_order is not a MenuItemOrder instance
            
        Note:
            If an item with the same menu number and modifications exists,
            its quantity will be incremented instead of adding a new item.
        """
        if not isinstance(menu_item_order, MenuItemOrder):
            raise TypeError("menu_item_order must be an instance of MenuItemOrder")

        # Look for matching item by menu number and modifications
        for existing_item in self._menu_items:
            if (existing_item.menuNumber == menu_item_order.menuNumber and
                    existing_item.modifications == menu_item_order.modifications):
                existing_item.increment_quantity()
                self._update_order_totals()
                return

        self._menu_items.append(menu_item_order)
        self._update_order_totals()

    def _update_order_totals(self) -> None:
        """Update both total price and total items count."""
        self._totalprice = self.calculate_total()
        self._total_items = self.update_total_items()

    def delete_item(self, item):
        """
        Remove or decrement a menu item from the order.
        
        This method will:
        1. Remove the item completely if its quantity is 1
        2. Decrement the quantity if greater than 1
        3. Remove the item if decrementing would result in 0 quantity
        
        Args:
            item: MenuItems object representing the item to remove/decrement
            
        Raises:
            ValueError: If the item is not found in the order
            TypeError: If item doesn't have required attributes
        """
        if not hasattr(item, 'menuNumber'):
            raise TypeError("Invalid menu item object")
            
        for menu_item_order in self._menu_items:
            if menu_item_order.menuNumber == item.menuNumber and menu_item_order.modifications == item.modifications:
                # If quantity is 1 or decrementing fails, remove the item
                if menu_item_order.quantity == 1 or not menu_item_order.decrement_quantity():
                    self._menu_items.remove(menu_item_order)
                self._update_order_totals()
                return
                
        raise ValueError(f"Item '{item.menuName}' not found in the order.")

    def get_items_by_tag(self, tag: str) -> List[MenuItemOrder]:
        """
        Get all items in the order with a specific tag.

        Args:
            tag (str): The tag to search for

        Returns:
            List[MenuItemOrder]: List of matching items
        """
        return [item for item in self._menu_items if tag in item.menuTags]

    def clear_order(self) -> None:
        """Clear all items from the order."""
        self._menu_items.clear()
        self._totalprice = 0.0
        self.update_total_items()

    def get_order_summary(self) -> dict:
        """
        Get a summary of the order details.

        Returns:
            dict: Order summary including total items, price, and timestamp
        """
        return {
            'order_id': self.__order_id,
            'datetime': self.__datetime,
            'employee_id': self.__employeeID,
            'total_items': sum(item.quantity for item in self._menu_items),
            'total_price': self.totalprice,
            'items': [{'name': item.menuName, 
                      'quantity': item.quantity, 
                      'price': item.total_price} 
                     for item in self._menu_items]
        }

    def display_order_as_string(self):
        """
        Generate and return the order details as a string.

        :return: A string representation of the order.
        """
        # Start constructing the order string
        order_details = []
        order_details.append(f"Order ID: {self.__order_id or 'Not assigned yet'}")
        order_details.append(f"Date/Time: {self.__datetime}")
        order_details.append(f"Employee ID: {self.__employeeID}")
        order_details.append("Items Ordered:")
        
        # Loop through each menu item
        for item in self._menu_items:
            order_details.append(f" - {item.menuName}: {item.quantity} @ £{item.total_price:.2f} each")
        
        # Add total price and total items
        order_details.append(f"Total Price: £{self._totalprice:.2f}")
        order_details.append(f"Total Items: {self.total_items}")

        # Join the list into a single string with line breaks
        return "\n".join(order_details)