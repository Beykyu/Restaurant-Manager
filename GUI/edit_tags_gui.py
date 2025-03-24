import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class EditTagsGUI():

    def __init__(self, root):
        self.root = root
        self.root.title("Tag Editor")
        self.tags = set(self.get_tags())  # Using a set to store tags

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
            messagebox.showinfo("Success", "Tags saved successfully!")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def update_tags_in_database(self, tags: set[str]) -> None:
        """
        Updates all the tags of menu items currently on database by removing all the tags that no longer exist in file
        Args:
            tags (set[str]): A set of tags that are to be removed from the file
        """
        pass

    def add_tag(self):
        """
        Prompt the user to enter a new tag and add it to the set.
        """
        new_tag = simpledialog.askstring("Add Tag", "Enter new tag:")
        if new_tag:
            self.tags.add(new_tag)  # Automatically handles duplicates
            self.update_listbox()

    def remove_tag(self):
        """
        Remove the selected tag from the set.
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            tag_to_remove = self.listbox.get(selected_index)
            self.tags.discard(tag_to_remove)  # Remove the tag from the set
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


if __name__ == "__main__":
    root = tk.Tk()
    gui = EditTagsGUI(root)
    root.mainloop()