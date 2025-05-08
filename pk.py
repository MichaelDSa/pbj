#!/usr/bin/env python3
import json
import os
import sys
import re  # For checking invalid characters in keys

# CONFIG_FILE = "directory_bookmarks.json"

CONFIG_FILE = "~/notes_temp/python_script/directory_bookmarks.json"

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
    """Lists all saved bookmarks with numbers.
    Now returns a list of keys along with the bookmarks dictionary.
    """
    if bookmarks:
        print("Saved Directory Bookmarks:")
        keys = list(bookmarks.keys())  # Get a list of keys
        for i, key in enumerate(keys):
            path = bookmarks[key]
            print(f"  {i+1}: {key}: {path}")  # Display with number
        return keys, bookmarks  # Return keys and bookmarks
    else:
        print("No directories have been saved yet.")
        return [], {}  # Return empty list and dict

def save_directory(key, path=None):
    """Saves a directory path associated with the given key."""
    bookmarks = load_bookmarks()
    if not key.isalnum() or key.lower() == 'ls' or key.lower() == 'cd': # Restrict keys to alphanumeric
        print("Error: Invalid key. Keys must be alphanumeric and cannot be 'ls' or 'cd'.")
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

def change_directory(key_or_number, keys=None, bookmarks=None):
    """Changes the current directory to the path associated with the given key or number."""
    if keys is None or bookmarks is None:
        bookmarks = load_bookmarks()
        keys = list(bookmarks.keys())

    if isinstance(key_or_number, int):
        if 1 <= key_or_number <= len(keys):
            target_dir = bookmarks[keys[key_or_number - 1]]
        else:
            print(f"Error: Invalid bookmark number. Please enter a number between 1 and {len(keys)}.")
            return
    elif isinstance(key_or_number, str):
        if key_or_number in bookmarks:
            target_dir = bookmarks[key_or_number]
        else:
            print(f"Error: Key '{key_or_number}' not found in {CONFIG_FILE}.")
            return
    else:
        print("Error: Invalid argument. Please provide either a key or a number.")
        return

    try:
        os.chdir(target_dir)
        print(f"Changed directory to: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Error: Directory '{target_dir}' does not exist.")
        del bookmarks[key_or_number] if isinstance(key_or_number, str) else del bookmarks[keys[key_or_number - 1]]
        save_bookmarks(bookmarks)
        print(f"Removed broken bookmark for key '{key_or_number}'.")
    except NotADirectoryError:
        print(f"Error: '{target_dir}' is not a directory.")
        del bookmarks[key_or_number] if isinstance(key_or_number, str) else del bookmarks[keys[key_or_number - 1]]
        save_bookmarks(bookmarks)
        print(f"Removed invalid bookmark for key '{key_or_number}'.")

if __name__ == "__main__":
    num_args = len(sys.argv)

    if num_args == 1:
        keys, bookmarks = list_bookmarks(load_bookmarks()) # Capture the returned values.
    elif num_args == 2:
        command = sys.argv[1]
        if command == "cd":
            os.chdir(os.path.expanduser("~"))
            print(f"Changed directory to: {os.getcwd()}")
        elif command == "ls":
            keys, bookmarks = list_bookmarks(load_bookmarks()) # Capture returned values
        else:
            try:
                # Attempt to convert the argument to an integer
                number = int(command)
                keys, bookmarks = list_bookmarks(load_bookmarks())  # Load keys and bookmarks
                change_directory(number, keys, bookmarks)
            except ValueError:
                # If it's not an integer, treat it as a key
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
        print("  python directory_manager.py                 # List all saved bookmarks")
        print("  python directory_manager.py cd              # Change directory to home (~)")
        print("  python directory_manager.py ls              # List all saved bookmarks")
        print("  python directory_manager.py <key>           # Change directory to the saved path of <key>")
        print("  python directory_manager.py <number>        # Change directory to the path at <number>")
        print("  python directory_manager.py -s <key>        # Save current directory with <key>")
        print("  python directory_manager.py -s <key> <path>  # Save <path> with <key> (must be a directory)")

