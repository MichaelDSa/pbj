#!/usr/bin/env python3
import json
import os
import sys
import re  # For checking invalid characters in keys

CONFIG_FILE = "directory_bookmarks.json"

def load_bookmarks():
    """Loads bookmarks from the config file. Returns an empty dict if the file doesn't exist."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_bookmarks(bookmarks):
    """Saves the bookmarks to the config file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=4)

def list_bookmarks(bookmarks):
    """Lists all saved bookmarks (keys and their values)."""
    if bookmarks:
        print("Saved Directory Bookmarks:")
        for key, path in bookmarks.items():
            print(f"  {key}: {path}")
    else:
        print("No directories have been saved yet.")

def save_directory(key, path=None):
    """Saves a directory path associated with the given key."""
    bookmarks = load_bookmarks()
    if re.search(r'[-_!@#$%^&*(),.+=]', key) or key == 'ls':
        print("Error: Invalid key. Keys cannot contain special characters like '-_!@#$%^&*(),.+=', or be 'ls'.")
        return

    if path:
        if os.path.isdir(path):
            bookmarks[key] = path
            save_bookmarks(bookmarks)
            print(f"Saved directory '{path}' as key '{key}' in {CONFIG_FILE}")
        else:
            print(f"Error: Path '{path}' is not a valid directory.")
    else:
        current_dir = os.getcwd()
        bookmarks[key] = current_dir
        save_bookmarks(bookmarks)
        print(f"Saved current directory '{current_dir}' as key '{key}' in {CONFIG_FILE}")

def change_directory(key):
    """Changes the current directory to the path associated with the given key."""
    bookmarks = load_bookmarks()
    if key in bookmarks:
        target_dir = bookmarks[key]
        try:
            os.chdir(target_dir)
            print(f"Changed directory to: {os.getcwd()}")
        except FileNotFoundError:
            print(f"Error: Directory '{target_dir}' associated with key '{key}' does not exist.")
            del bookmarks[key]
            save_bookmarks(bookmarks)
            print(f"Removed broken bookmark for key '{key}'.")
        except NotADirectoryError:
            print(f"Error: '{target_dir}' associated with key '{key}' is not a directory.")
            del bookmarks[key]
            save_bookmarks(bookmarks)
            print(f"Removed invalid bookmark for key '{key}'.")
    else:
        print(f"Error: Key '{key}' not found in {CONFIG_FILE}.")

if __name__ == "__main__":
    num_args = len(sys.argv)

    if num_args == 1:
        bookmarks = load_bookmarks()
        list_bookmarks(bookmarks)
    elif num_args == 2:
        command = sys.argv[1]
        if command == "cd":
            os.chdir(os.path.expanduser("~"))
            print(f"Changed directory to: {os.getcwd()}")
        elif command == "ls":
            bookmarks = load_bookmarks()
            list_bookmarks(bookmarks)
        else:
            change_directory(command)
    elif num_args == 3 and sys.argv[1] == "-s":
        key_to_save = sys.argv[2]
        save_directory(key_to_save)
    elif num_args == 4 and sys.argv[1] == "-s":
        key_to_save = sys.argv[2]
        path_to_save = sys.argv[3]
        save_directory(key_to_save, path_to_save)
    else:
        print("Usage:")
        print("  python directory_manager.py                     # List all saved bookmarks")
        print("  python directory_manager.py cd                  # Change directory to home (~)")
        print("  python directory_manager.py ls                  # List all saved bookmarks")
        print("  python directory_manager.py <key>               # Change directory to the saved path of <key>")
        print("  python directory_manager.py -s <key>            # Save current directory with <key>")
        print("  python directory_manager.py -s <key> <path>     # Save <path> with <key> (must be a directory)")
