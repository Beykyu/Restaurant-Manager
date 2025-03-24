from tkinter import Tk, Toplevel
from GUI.login_gui import Login_Screen
from GUI.owner_gui import Owner_Gui
from GUI.new_item_gui import New_Item
from GUI.add_users_gui import AddUserGUI
from GUI.manage_users_gui import ManageUsersGUI
from GUI.employee_gui import EmployeeGui
from GUI.view_past_order_gui import PastOrdersGUI
from GUI.edit_tags_gui import EditTagsGUI

class WindowManager:
    def __init__(self):
        self.root = Tk()  # The single Tk() instance
        self.root.withdraw()  # Start with the root window hidden

    def show_login_screen(self):
        # Create the login screen within the single root instance
        self.root.deiconify()  # Show the root window
        Login_Screen(self.root, self)

    def show_owner_screen(self):
        # Hide the root window and create a new Toplevel for the owner screen
        self.root.withdraw()
        new_window = Toplevel(self.root)  # Use Toplevel for additional windows
        Owner_Gui(new_window, self)

    def show_add_item_screen(self):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        New_Item(new_window,self)

    def run(self):
        self.show_login_screen()
        self.root.mainloop()

    def show_add_users(self):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        AddUserGUI(new_window,self)

    def show_manage_users(self):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        ManageUsersGUI(new_window,self)

    def show_employee_screen(self,id):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        EmployeeGui(new_window, self, employeeID=id)

    def show_past_orders_screen(self):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        PastOrdersGUI(new_window, self)

    def show_edit_tags_screen(self):
        self.root.withdraw()
        new_window = Toplevel(self.root)
        EditTagsGUI(new_window, self)
        
if __name__ == "__main__":
    app = WindowManager()
    app.run()
