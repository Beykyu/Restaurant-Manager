import Classes.MenuItems as MenuItems
import Classes.CustomerOrder as CustomerOrder
import Helpers.db_connection as db_connection
import json
from tkinter import messagebox
import bcrypt

#TODO Refactor into a class to handle all database functions in database using connection pooling
def Validate_login(username: str, password: str) -> int:
    """
    Validate user credentials and return permission level.

    Args:
        username (str): The username provided by the user
        password (str): The password provided by the user

    Returns:
        int: Permission level (0 if authentication fails)

    Raises:
        Exception: If database connection or query fails
    """
    if not username or not password:
        messagebox.showerror("Error", "Username or password cannot be empty.")
        return 0

    try:
        user = get_user(username, password)
        if user:
            return user[3]  # Permission level
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            return 0
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred during login. Please try again.")
        print(f"Error details: {e}")
        return 0

    
def add_item_to_database(menuNo: str, name: str, price: float, tags: list) -> None:
    """Add a new menu item to the database.

    Args:
        menuNo (str): Unique identifier for the menu item
        name (str): Name of the menu item
        price (float): Price of the menu item
        tags (list): List of tags associated with the menu item

    Raises:
        Exception: If menu number already exists or database operation fails
    """
    db = db_connection.create_connection()
    
    if db:
        try:
            cursor = db.cursor()
            #Check if item already exits in database
            check_query = "SELECT COUNT(*) FROM menu WHERE menuNo = %s;"
            cursor.execute(check_query, (menuNo,))
            result = cursor.fetchone()
            
            #Handles if it already exists
            if result[0] > 0:  
                raise Exception(f"Menu number {menuNo} already exists in the database.")
            tags_json = json.dumps(tags)
            
            # SQL query to insert a new item into the database
            query = """
            INSERT INTO menu (menuNo, name, price, tags)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (menuNo, name, price, tags_json))
            db.commit()
            messagebox.showinfo("Success", "Successfully added to the database")
        except Exception as e:
            messagebox.showerror("Error", f"An error adding to database: {e}")
        finally:
            db.close()
    else:
        messagebox.showerror("Error", f"Failed to connect to database: {e}")

#TODO Refactor following 2 functions
def fetch_menu_items(tag: str, type: int) -> list:
    """Fetch menu items from database based on tag and search type.

    Args:
        tag (str): Search by tag or "*" for all items
        type (int): Search type (1 to search for a specific menu item, otherwise searches by items that have a tag)

    Returns:
        list: List of MenuItems objects matching the search criteria

    Raises:
        Exception: If database connection or query execution fails
    """
    menu_items_list = []
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            
            # Get the appropriate query based on the tag
            query = create_query(tag,type)
            if tag == "*": #Retrieves all the menu items
                cursor.execute(query)
            elif type == 1: #Searchs for a specific menu item through id
                cursor.execute(query, (tag,)) #Search by tags
            else:
                cursor.execute(query, (f"%{tag}%",))  # Pass the tag as a parameter
            
            # Fetch all rows and process them
            rows = cursor.fetchall()
            for row in rows:
                menuNo, name, price, tags_json = row
                tags = json.loads(tags_json)  # Parse tags from JSON
                menu_items_list.append(MenuItems.MenuItems(menuNo, name, price, tags))
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving from the database: {e}")
        finally:
            if db:
                db.close()
    else:
        messagebox.showerror("Error", "Can't connect to database")
    return menu_items_list

def create_query(tag: str, type: int) -> str:
    """
    Create SQL query based on search parameters.
    
    Args:
        tag (str): Search tag or "*" for all items
        type (int): Search type (1 for menuNo search, other for tag search)
    
    Returns:
        str: SQL query string with proper ordering
    """
    order_by = """
        ORDER BY 
            CAST(menuNo AS UNSIGNED), 
            menuNo
    """
    
    if tag == "*": #Retrieves all menu items
        return f"SELECT * FROM menu {order_by}"
    elif type == 1: #Finds a specific menu item by id
        return "SELECT * FROM menu WHERE MenuNo = %s"
    else: #Retrieves all menu items that have the tag
        return f"SELECT * FROM menu WHERE tags LIKE %s {order_by}"


def update_item_in_database(item: MenuItems) -> None:
    """Update existing menu item in database.

    Args:
        item (MenuItems): Menu item object containing updated information

    Raises:
        Exception: If database connection or update operation fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            tags_json = json.dumps(item.menuTags)
            query = """
            UPDATE menu
            SET name = %s, price = %s, tags = %s
            WHERE menuNo = %s;
            """
            cursor.execute(query, (item.menuName, item.menuPrice, tags_json, item.menuNumber))
            db.commit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            db.close()

def add_user(name: str, username: str, password: str, permission_level: int) -> None:
    """Add new user to the database.

    Args:
        name (str): Full name of the user
        username (str): Unique username
        password (str): User's password (will be hashed)
        permission_level (int): User's permission level

    Raises:
        Exception: If database operation fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            salt = bcrypt.gensalt()
            password = password.encode('utf-8')  # Convert to bytes
            password = bcrypt.hashpw(password, salt)
            cursor = db.cursor()

            query = """
            INSERT INTO users(name, username, password, permission_level)
            VALUES (%s, %s, %s, %s);
            """

            cursor.execute(query,(name, username, password, permission_level))

            db.commit()
            print("Works")
        except Exception as e:
            raise Exception(e)
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def update_User(name: str, username: str, password: str, permission_level: int) -> None:
    """Update existing user's details in database.

    Args:
        name (str): Updated full name
        username (str): Username to identify user
        password (str): New password (optional, will be hashed if provided)
        permission_level (int): Updated permission level

    Raises:
        Exception: If database operation fails
    """
    db = db_connection.create_connection()
    
    if not db:
        messagebox.showerror("Error", "Database connection failed!")
        return

    try:
        cursor = db.cursor()
        if password:
            # Hash the password if it's provided
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            query = """
                UPDATE users
                SET name = %s, username = %s, password = %s, permission_level = %s
                WHERE username = %s;
            """
            cursor.execute(query, (name, username, hashed_password, permission_level, username))
        else:
            # Update without changing the password
            query = """
                UPDATE users
                SET name = %s, username = %s, permission_level = %s
                WHERE username = %s;
            """
            cursor.execute(query, (name, username, permission_level, username))

        db.commit()
        messagebox.showinfo("Success", "User updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if db:
            db.close()
    
def get_user(username: str, password: str = False) -> tuple:
    """Retrieve user information from database.

    Args:
        username (str): Username to look up
        password (str, optional): Password to verify. Defaults to False.

    Returns:
        tuple: User information if found, False if authentication fails

    Raises:
        Exception: If database query fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()

            query = """
            SELECT * 
            FROM users
            WHERE username = %s;
            """

            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row and password:
                # Verify the password
                stored_password = row[2]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return row
                return False
            else:
                return row
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")

def get_all_user() -> list:
    """Retrieve all users from database.

    Returns:
        list: List of tuples containing user information

    Raises:
        Exception: If database query fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()

            query = """
            SELECT * 
            FROM users;
            """

            cursor.execute(query)
            row = cursor.fetchall()           
            if row:
                return row
        except Exception as e:
            raise Exception
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def add_customer_order(order: CustomerOrder) -> bool:
    """Add new customer order to database.

    Args:
        order (CustomerOrder): Order object containing order details

    Returns:
        bool: True if order was successfully added

    Raises:
        Exception: If database operation fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """
                    INSERT INTO customer_orders(employee_username, time_of_order, total_price, total_no_of_items)
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(query,(order.employeeID, order.datetime, order.totalprice, order.total_items))
            last_inserted_id = cursor.lastrowid
            for menuItem in order.menu_items:
                query = """
                    INSERT INTO menu_item_order(order_id, menuNo, quantity, total_price, modifications)
                    VALUES (%s, %s, %s, %s, %s)"""
                modifications_json = json.dumps(menuItem.modifications)
                cursor.execute(query,(last_inserted_id, menuItem.menuNumber, menuItem.quantity, menuItem.total_price,modifications_json ))
            db.commit()
            return True
        except Exception as e:
            raise Exception
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def get_mod_from_tag(tag: str) -> list:
    """Get modifications info associated with a specific tag/grouping.

    Args:
        tag (str): Group that the modification belongs to

    Returns:
        list: List of tuples containing modification details

    Raises:
        Exception: If database query fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """
                    SELECT modification_name, additional_cost
                    FROM modifications
                    WHERE tag_name = %s
                    """
            cursor.execute(query, tag)
            row = cursor.fetchall()
            return row 
        except Exception as e:
            raise Exception
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def get_past_order(date: str) -> list:
    """Get past orders from the database.

    Args:
        date (str): Date to search for past orders generally in YYYY-MM-DD format

    Returns:
        list: List of tuples containing order details

    Raises:
        Exception: If database query fails
        ConnectionError: If database connection fails
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """SELECT employee_username, order_id, time_of_order, total_no_of_items
                    FROM customer_orders
                    WHERE DATE(time_of_order) = %s
                    ORDER BY time_of_order ASC;
                    """
            cursor.execute(query, date)
            row = cursor.fetchall()
            return row
        except Exception as e:
            raise Exception
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def get_past_order_items(order_id: int) -> list:
    """Get items associated with a past order.

    Args:
        order_id (int): Order ID to look up items for

    Returns:
        list: List of tuples containing item details"
        """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """SELECT mio.menuNo, m.name ,mio.quantity, m.price, mio.modifications
                    FROM menu_item_order AS mio
                    JOIN menu AS m
                    ON mio.menuNo = m.menuNo
                    WHERE order_id = %s;
                    """
            cursor.execute(query, order_id)
            row = cursor.fetchall()
            return row
        except Exception as e:
            raise Exception
        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
    
def remove_menu_item_tags(tags_to_remove: set[str]) -> bool:
    """
    Removes a set of tags from all menu items in the database.

    Args:
        tags_to_remove (set[str]): A set of tags to be removed from menu items.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    db = db_connection.create_connection()
    if db:
        try:
            cursor = db.cursor()

            # Retrieve all menu items with their tags
            query = "SELECT menuNo, tags FROM menu"
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                entry_id = row[0]
                tags = json.loads(row[1])  # Parse JSON tags into a Python list

                # Remove the specified tags
                updated_tags = [tag for tag in tags if tag not in tags_to_remove]

                # Handle empty tags by adding "None"
                if not updated_tags:
                    updated_tags = ["None"]

                # Update the database with the modified tags
                update_query = "UPDATE menu SET tags = %s WHERE menuNo = %s"
                cursor.execute(update_query, (json.dumps(updated_tags), entry_id))

            db.commit()
            return True

        except Exception as e:
            db.rollback()  # Undo changes in case of an error
            print(f"Error: {e}")
            return False

        finally:
            db.close()
    else:
        raise ConnectionError("Failed to establish database connection.")
        