from Classes.MenuItems import MenuItems

class MenuItemOrder(MenuItems):
    def __init__(self, menu_item, quantity=1, modifications=None):
        """
        Initialize a MenuItemOrder instance.

        Args:
        menu_item(MenuItem): The base MenuItems object.
        quantity(int): The quantity of the menu item ordered.
        modifications(dictionary): A dictionary of modifications (e.g., {"extra onions": 0.50, "no prawns": 0.00}).
        """
        if not isinstance(menu_item, MenuItems):
            raise TypeError("menu_item must be an instance of MenuItems")
        super().__init__(menu_item.menuNumber, menu_item.menuName, menu_item.menuPrice, menu_item.menuTags)
        self._quantity = quantity
        self._modifications = modifications or {}  # Default to no modifications
        self._total_price = self.calculate_total()

    @property
    def modifications(self):
        """
        Return the modifications dictionary.
        """
        return self._modifications

    @property
    def quantity(self):
        """
        Return the quantity of the menu item ordered.
        """
        return self._quantity
    
    def set_quantity_to_one(self):
        """
        Sets the quantity to 1 in case of creating temp copies. 
        Consider refactoring so this isn't needed
        """
        self._quantity = 1
        self.calculate_total()

    def increment_quantity(self):
        """
        Increment the quantity of the menu item ordered by 1.
        """
        self._quantity += 1
        self._total_price = self.calculate_total()

    def decrement_quantity(self) -> bool:
        """
        Decrement the quantity of the menu item ordered by 1 if greater than 1.

        :return: True if the quantity was decremented, False if it was already 1.
        """
        if self._quantity > 1:
            self._quantity -= 1
            self._total_price = self.calculate_total()
            return True
        else:
            self._total_price = self.calculate_total()
            return False

    @property
    def total_price(self):
        """
        Calculate the total price of this menu item order, including modifications.

        :return: The total price as a float.
        """
        return self._total_price

    def calculate_total(self):
        """
        Calculate the total price of the menu item order, including modifications.

        :return: The total price as a float.
        """
        base_price = self.menuPrice  # Base price of the menu item
        mod_price = sum(self.modifications.values())  # Sum all price changes from modifications
        return round((base_price + mod_price) * self.quantity, 2)

    def add_modification(self, modification, cost, mod_type):
        """
        Add or update a modification for the menu item.

        :param modification: A string representing the modification (e.g., "Cheese").
        :param cost: The additional cost of the modification (can be 0 for no-cost changes).
        :param mod_type: The type of modification (e.g., "No", "Extra", "Swap").
        """
        new_key = f"{mod_type} {modification}"

        # Search for existing keys that reference the same "modification" but different types
        existing_key = next((key for key in self._modifications if key.endswith(modification)), None)

        # If an existing key is found, remove it
        if existing_key:
            del self._modifications[existing_key]

        # Add the new modification with the updated type and cost and updates total price
        self._modifications[new_key] = cost
        self._total_price = self.calculate_total()


    def remove_modification(self, modification):
        """
        Remove a modification from the menu item.

        :param modification: A string representing the modification to remove.
        :raises KeyError: If the modification is not found.
        """
        if modification in self._modifications:
            del self._modifications[modification]
        else:
            raise KeyError(f"Modification '{modification}' not found.")
        self._total_price = self.calculate_total()

    def __str__(self):
        """
        String representation of the MenuItemOrder.

        :return: A string with details about the menu item, modifications, and total price.
        """
        mods = ", ".join([f"{mod} (+£{cost:.2f})" for mod, cost in self.modifications.items() if cost > 0] +
                         [f"{mod} (no cost)" for mod, cost in self.modifications.items() if cost == 0]) or ""
        return f"{self.menuName} x{self.quantity} - £{self.total_price:.2f} ({mods})"
