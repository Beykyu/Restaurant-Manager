# Restaurant Manager

A comprehensive restaurant management system built with Python and Tkinter, designed to handle menu management, order processing, and user administration.

## 🚧 Project Status

This project is currently in active development, with core features implemented and functioning. While the system is operational, most features are still being refined and enhanced.

## ✨ Key Features

### Currently Implemented:
- **User Authentication System**
  - Multi-level user permissions (Admin/Owner, Employee)
  - Secure password hashing using bcrypt
  - User management interface for administrators

- **Menu Management**
  - Add, edit, and view menu items
  - Dynamic tag system for food categorization
  - Price and item modification tracking
  - Custom modifications support for menu items
  - Editing Tag and modifications

- **Order Processing**
  - Real-time order creation and modification
  - Support for item customization and special requests
  - Order history tracking
  - Daily sales reporting

- **Employee Management**
  - Employee access control
  - Activity tracking by employee ID
  - Permission-based feature access

### Planned Features:
- Enhanced reporting and analytics
- Inventory management system
- Table management
- Customer loyalty program
- Receipt printing integration

## 🛠️ Technical Stack

- **Backend:** Python
- **Frontend:** Tkinter
- **Database:** MySQL
- **Authentication:** bcrypt
- **Environment Management:** python-dotenv

## 📋 Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  ```bash
  pymysql
  bcrypt
  python-dotenv
  ```

## 🚀 Getting Started

1. Clone the repository
2. Create a `.env` file with your database credentials:
   ```env
   DB_HOST=your_host
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=your_database_name
   ```
3. Create a new MySQL database:
   ```sql
   CREATE DATABASE restaurant;
   ```
4. Run the initial setup to create database tables and admin user:
   ```bash
   python admin_setup.py
   ```
5. Launch the application:
   ```bash
   python window_manager.py
   ```

## Database Setup

The `admin_setup.py` script will automatically:
- Create all required database tables
- Set up table relationships and constraints
- Create the initial admin user
- Configure basic security settings

If you encounter any errors during setup, ensure:
- MySQL server is running
- Database credentials in `.env` are correct
- The specified database exists
- The user has sufficient privileges

## 👥 Default Admin Access

- Username: Admin
- Password: password
- Permission Level: 1 (Owner/Admin)

## 🔒 Security

- Passwords are securely hashed using bcrypt
- Environment variables for sensitive data
- Permission-based access control

## 🗄️ Project Structure

```
Restaurant-Manager/
├── Classes/          # Core class definitions
├── GUI/              # GUI implementation files
├── Helpers/          # Utility and helper functions
├── MISC/             # Configuration files
├── Tests/            # Unit tests
└── window_manager.py # Application entry point
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

While this project is primarily for educational purposes, suggestions and improvements are welcome. Please open an issue to discuss potential changes.

## ⚠️ Known Issues

- Most UI elements need refinement
- Additional error handling needed in specific cases
- Performance optimization pending for large datasets

## 📮 Contact

For any queries or suggestions, please open an issue in the repository.