import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from gui_functions import remove_menu_item_tags

class EditTagsGUI():

    def __init__(self, root, window_manager):
        self.root = root
        self.window_manager = window_manager
        self.root.title("Tag Editor")
        self.tags = set(self.get_tags())  # Using a set to store tags
        self.tags_to_remove = set() # Holds a set of tags to be removed from the database

        # Create GUI elements
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=15)
        self.listbox.pack(pady=10)

        # Add existing tags to the listbox
        self.update_listbox()

        # Buttons
        self.add_button = tk.Button(root, text="Add Tag", command=self.add_tag)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Selected Tag", command=self.remove_tag)
        self.remove_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Tags", command=self.save_tags)
        self.save_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Go back", command=self.owner_gui_return)
        self.save_button.pack(pady=5)

    def get_tags(self) -> set[str]:
        """
        Retrieves the currently saved tags.
        Returns:
            tags(set[str]): A set of all tags currently on file.
        """
        try:
            with open('MISC/tags.json', 'r') as file:
                data = json.load(file)
            return data.get("tags", set())  # Fallback to an empty list if "tags" is missing
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tags.json: {e}")
            return set()

    def save_tags(self) -> None:
        """
        Updates the file containing the saved tags.
        """
        try:
            with open('MISC/tags.json', 'w') as file:
                data = {"tags": list(self.tags)}  # Convert set to list for JSON serialization
                json.dump(data, file)
            self.update_tags_in_database(self.tags_to_remove)
            #messagebox.showinfo("Success", "Tags saved successfully!")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def update_tags_in_database(self, tags: set[str]) -> None:
        """
        Updates all the tags of menu items currently on database by removing all the tags that no longer exist in file
        Args:
            tags (set[str]): A set of tags that are to be removed from the file
        """
        if remove_menu_item_tags(tags):
            messagebox.showinfo("Success", "Tags successfully changed")
        else:
            messagebox.showerror("Error", "Tags could not be updated")
        

    def add_tag(self):
        """
        Prompt the user to enter a new tag and add it to the set.
        """
        new_tag = simpledialog.askstring("Add Tag", "Enter new tag:")
        if new_tag:
            self.tags.add(new_tag)
            self.tags_to_remove.discard(new_tag) # Stops newly added tag from being accidently deleted from database
            self.update_listbox()

    def remove_tag(self):
        """
        Remove the selected tag from the set.
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            tag_to_remove = self.listbox.get(selected_index)
            self.tags_to_remove.add(tag_to_remove) # Adds tag to set that stores tags that need to be removed from database
            self.tags.discard(tag_to_remove)  # Remove the tag current tags list
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "No tag selected!")

    def update_listbox(self):
        """
        Refresh the listbox to display the current tags.
        """
        self.listbox.delete(0, tk.END)
        for tag in sorted(self.tags):  # Sorting tags for consistent display
            self.listbox.insert(tk.END, tag)

    def owner_gui_return(self):
        """Return to the owner GUI screen."""
        self.root.destroy()
        self.window_manager.show_owner_screen()

if __name__ == "__main__":
    root = tk.Tk()
    gui = EditTagsGUI(root)
    root.mainloop()