import re
    
class MenuItems():
    """
    A class to represent a menu item in a restaurant.

    Attributes:
        menuNumber (str): The menu item number (digits + optional single letter).
        menuName (str): The name of the menu item.
        menuPrice (float): The price of the menu item.
        menuTags (list): Tags describing the menu item (e.g., "Chicken", "Beef").
    Raises:
        ValueError : If the given menuNumber is not in the correct format of any number of digits followed by 1 or 0 letters
    """
    def __init__(self,menuNo,name,price,tags = None):
        newMenuNo = str(menuNo).strip().replace(" ", "")
        
        # Regex validation for digits of any length followed by 0 or 1 letter(s)
        if not re.fullmatch(r"^\d+[a-zA-Z]?$", newMenuNo):
            raise ValueError("menuNumber must start with numbers and may have 0 or 1 letters at the end. All whitespace is ignored.")
        self.__menuNumber = newMenuNo
        self.menuName = name
        self.menuPrice = price
        self.menuTags = tags

    @property 
    def menuNumber(self):
        return self.__menuNumber
    
    @property
    def menuName(self):
        return self._menuName
    
    @menuName.setter
    def menuName(self,name : str) -> None:
        """
        Sets the menu item name.

        Args:
            name (str): The name of the menu item to be set. Must non-empty string with no whitespace in front or back.

        Raises:
            ValueError: If name is an empty string.

        All front and back white space of string is removed and is validated to ensure it's not empty
        """
        newName = str(name.strip())
        if newName == "":
            raise ValueError("Please make sure you've entered a name")
        self._menuName = newName
    
    @property
    def menuPrice(self):
        return self._menuPrice
    
    #TODO check if additional checks are required
    @menuPrice.setter
    def menuPrice(self,newVal : float) -> None:
        """
        Sets the menu item price.

        Args:
            newVal (float): The new price to set. Must be a non-negative number, formatted to 2 decimal places.

        Raises:
            ValueError: If newVal is None, negative, or not a valid numeric value.

        The value is validated, rounded to two decimal places, and stored as a float.
        """
        try:
            if newVal is None:
                raise ValueError("Error: Price cannot be None.")
            price = round(float(newVal), 2) 
            if price < 0:
                raise ValueError("Please enter a valid price")
            #Rounds the number to 2 decimal places and then ensures it's always in .xx format
            self._menuPrice = float("{:.2f}".format(price))
        except (ValueError, TypeError):
            raise ValueError("Please enter a number")

    @property
    def menuTags(self):
        return self._menuTags
    
    #Come back to do checks later, May allow for iterables instead of only lists 
    @menuTags.setter
    def menuTags(self, tags : list) -> None:
        """
        Sets all the tags that a menu item can be described with.

        Args:
            tags (list or None): A list of strings. If an empty list or None is passed, it will default to ["None"].

        Raises:
            TypeError: If the input is not a list or None, or if the list contains non-string elements.

        Ensures the tags are correctly formatted and safely assigned.
        """
        if tags is None or (isinstance(tags, list) and len(tags) == 0):
            # Set to ["None"] if tags is None or an empty list
            self._menuTags = ["None"]
        elif not isinstance(tags, list):
            raise TypeError("Error: Expected a list for tags, but got a different type.")
        elif not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Error: All elements in the tags list must be strings.")
        else:
            # Remove "None" if other tags are present
            tags = [tag for tag in tags if tag != "None"]  # Filter out "None"
            if not tags:  # If the resulting list is empty, default to ["None"]
                self._menuTags = ["None"]
            else:
                self._menuTags = tags[:]  # Use a copy of the list to avoid external modification

    def __str__(self):
        tags = ", ".join(self.menuTags) if self.menuTags else "No Tags"
        return f"Menu item {self.menuNumber} : {self.menuName} - Price : £{self.menuPrice:.2f}  ({', '.join(self.menuTags)})"