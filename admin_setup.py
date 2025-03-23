from Helpers.db_connection import create_connection
from gui_functions import add_user
import os

# Initial admin setup constants
NAME = "Owner"
USERNAME = "Admin" 
PASSWORD = "password"
PERMISSION_LEVEL = 1

# SQL Queries for table creation
SQL_QUERIES = [
    """CREATE TABLE menu(  
        menuNo VARCHAR(10) NOT NULL PRIMARY KEY COMMENT 'Primary Key',
        name VARCHAR(255) NOT NULL,
        price DECIMAL(4,2) NOT NULL CHECK (price >= 0),
        tags JSON CHECK (JSON_VALID(tags))
    ) COMMENT 'Table for storing menu items';""",
    
    """CREATE TABLE users(
        name VARCHAR(255),
        username VARCHAR(255) NOT NULL PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        permission_level INT NOT NULL
    );""",
    
    """CREATE table Customer_Orders(
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        employee_username VARCHAR(255),
        time_of_order DATETIME,
        total_price DECIMAL(10,2) CHECK (total_price >= 0),
        total_no_of_items INT,
        FOREIGN KEY (employee_username) REFERENCES users(username)
    );""",
    
    """Create table Menu_Item_order(
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        menuNo VARCHAR(10) NOT NULL,
        quantity INT CHECK (quantity > 0),
        total_price DECIMAL(10,2) CHECK (total_price >= 0),
        modifications JSON CHECK (JSON_VALID(modifications)),
        FOREIGN KEY (order_id) REFERENCES Customer_Orders(order_id),
        FOREIGN KEY (menuNo) REFERENCES menu(menuNo)
    );""",
    
    """CREATE TABLE modifications (
        modification_id INT PRIMARY KEY AUTO_INCREMENT,
        modification_name VARCHAR(255) NOT NULL,
        additional_cost DECIMAL(10, 2) DEFAULT 0.00,
        tag_name VARCHAR(255) NOT NULL
    );"""
]

def setup_database():
    """
    Creates all required database tables.
    Should only be run during initial setup.
    """
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            for query in SQL_QUERIES:
                cursor.execute(query)
        connection.commit()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
    finally:
        connection.close()

def setup_initial_admin():
    """
    Creates the initial admin user in the database.
    This should only be run once during initial setup.
    """
    try:
        add_user(NAME, USERNAME, PASSWORD, PERMISSION_LEVEL)
        print("Admin user created successfully")
    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    setup_database()
    setup_initial_admin()
