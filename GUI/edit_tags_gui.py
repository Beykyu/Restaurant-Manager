import tkinter as tk
import json

class EditTagsGUI():

    def __init__(self, root, windows):
        pass

    def get_tags(self) -> list[str]:
        """
        Retrieves the currently saved tags 
        Returns:
            tags(list[str]): A list of all tags currently on file
        """
        try:
            with open('MISC/tags.json', 'r') as file:
                data = json.load(file)
            self.old_tags = data.get("tags", [])  # Fallback to an empty list if "tags" is missing
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading tags.json: {e}")
            self.tags = []
        return self.old_tags

    def save_tags(self, tags: list[str]) -> None:
        """
        Updates the file containing the saved tags 
        Args:
            tags (list[str]): A list of tags to replace current tags on file
        """
        try: 
            with open('MISC/tags.json', 'w') as file:
                data = {"tags" : tags }
                json.dump(data, file)
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    def update_tags_in_database(self, tags: list[str]) -> None:
        """
        Updates all the tags of menu items currently on database by removing all the tags that no longer exist in file
        Args:
            tags (list[str]): A list of tags that are to be removed from the file
        """
        pass