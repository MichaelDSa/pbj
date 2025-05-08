#!/usr/bin/env python3
from configparser import DuplicateSectionError
from curses.ascii import isalnum
import json
# import typing
from pickle import FALSE
from typing import Dict, List, Tuple, Dict
import os # OS routines for NT or Posix depending on what system we're on.
import sys # Built-in functions, types, exceptions, and other objects.
# import re # Support for regular expressions (RE).

CONFIG_FILE = "~/projects/Python/scripts/pbj/directory_bookmarks.json"

def change_directory(bookmarks: Dict[str, str]) -> None:
    return

def key_is_valid(key: str) -> bool:
    """Returns `True` if:
    - key arg does not have preceeding or trailing dot (`.`) characters
    - key arg is alphanumeric, or alphanumeric with the addition of dot (`.`) characters.

    Args:
        key (str): The key to be tested for naming adherance

    Returns:
        bool: `True` if key is valid
    """
    if key.startswith(".") or key.endswith("."):
        return False
    if not key.replace(".", "").isalnum():
        return False
    
    return True
    
def list(bookmarks: Dict[str, str]) -> Tuple[list[str], Dict[str, str]]:
    keys = []
    if bookmarks:
        keys = list(bookmarks.keys())
        for i, key in enumerate(keys):
            path = bookmarks[key]
            print(f"{i+1}) {key}: {path}")
    else:
        print("No directories found")
    # consder whether it's really
    # necessary to send a list of the
    # bookmark keys. Can't the client
    # just reproduce them from bookmarks?
    # Also, what client is going to
    # use the list() return value?
    return keys, bookmarks

def load() -> Dict[str, str]: 
    """returns a dict representing the keys and values of the CONFIG_FILE .json file

    Returns:
        Dict[str, str]: keys are the bookmarks. values are the paths
    """
    bookmarks: dict[str, str] = {}
    try:
        with open(CONFIG_FILE, "r") as f:
            bookmarks = json.load(f)
    except FileNotFoundError:
        print("FileNotFoundError")
    return bookmarks

def load_json_file(file: str) -> Dict[str, str]:
    """
    Save contents of a .json file to CONFIG_FILE if keys and values are valid.
    - keys must be alphanumeric but may contain one or more dots. Leading and trailing dots will be stripped.
    - keys that already exist in CONFIG_FILE will be ignored. The original value will not be replaced.
    - values must be paths to directories. Each path must exist.
    - values that already exist in CONFIG_FILE will be ignored. Key's values will not be updated.
    - valid json key-vals will be saved to CONFIG_FILE. 
    - invalid json key-vals will be ignored.

    Args:
        file (str): Arg must be a file representation of a .json file
    Returns:
        Dict[str,str]: Keys (bookmarks names) -> Values (Paths to directories)
    """
    file_contents: dict[str,str] = {}
    verified_file_contents: dict[str,str] = {}
    duplicate_keys_values: dict[str,str] = {}
    invalid_entries: dict[str,str] = {}

    if file.endswith(".json")
        try:
            with open(file, "r") as f:
                file_contents = json.load(f)
        except FileNotFoundError:
            print("FileNotFoundError (def load_json_file())")
            return {}
    else:
        print("file arg must end with `.json`")
        return {}

    if file_contents:
        bookmarks = load()
        for key, value in file_contents:
            # if key and val are valid:
            if key_is_valid(key) and (os.path.exists(value) and os.path.isdir(value)):
                # if k not found in bookmarks:
                if not bookmarks[key]:
                    # add key val to dict[str,str] (verified_file_contents)
                    verified_file_contents[key] = value
                else:
                    #add key val to duplicate_key_values
                    duplicate_keys_values[key] = value
            else:
                invalid_entries[key] = value
    
    # if invalid_entries is truthy, print them
    if invalid_entries:
        print("INVALID ENTRIES FOUND IN {file}:")
        for k, v in invalid_entries:
            print("{k}: {v}")
    print("")
    # if duplicate_keys_values is truthy, print them
    if duplicate_keys_values:
        print("DUPLICATE KEY VALS FOUND IN {file}:")
        for k, v in duplicate_keys_values:
            print("{k}: {v}")

    # initialize dict named `value_duplicates`
    value_duplicates: dict[str,str] = {}
    # check that values are not duplicated in file:
    remove_duplicate_values(verified_file_contents)
    # check verified_file_contents against bookmarks for value duplicates
    
    # display value_duplicates
    
    # return dict[str,str] (verified_file_contents)

    return verified_file_contents

def remove_duplicate_values(reference: Dict[str,str]) -> Dict[str,str]:
    """- Modifies reference dict[str,str] so that all values are unique. This is achieved by removing elements whose values are identical to those of other keys.
    - Returns dict[str,str] of duplicate values and their associated keys found in reference.

    Args:
        reference (Dict[str,str]): The dict[str,str] reference to be cleaned of redundant values.

    Returns:
        Dict[str,str]: The dict[str,str] consisting of each key with a redundant value found in reference.
    """
    set_of_dups: set[str] = set()
    duplicates: dict[str,str] = {}

    for key, value in reference.items():
        if value in set_of_dups:
            duplicates[key] = value
        else:
            set.add(value)

    for key in duplicates:
        del reference[key]
        
    return duplicates
    
def save(key: str, path: str) -> None:
    # validate key - must be alphanumeric. can have dots.
    if not key_is_valid(key):
        print("Keys may: ")
        print("    - contain alphanumeric characters")
        print("    - make use of dots. (eg: `dir.1`, `dir.2`, `dir.1.0`)")
        print("Keys may not have leading or trailing dots.")
        return

    # verify that path exists and that it is a directory
    if path and (os.path.exists(path) and os.path.isdir(path)) and (not value_found_in_config(path)):
        # save key value to CONFIG_FILE
        bookmarks = load()
        save_to_json(bookmarks)
        print("{key} saved to {path}")
    else:
        print("Attempted to save path to key ({key}), but it is either not a directory, does not exist, or is already assigned to existing key ({path}).")

def save_to_json(bookmarks: dict[str, str]) -> None:
    
    return      
    
def value_found_in_config(value: str) -> bool:
    bookmark_values: set[str] = set(load().values())
    return value in bookmark_values

def value_found_in_dict(reference: Dict[str,str], value: str) -> bool:
    reference_set: set[str] = set(reference.values())
    return value in reference_set

def value_is_valid(value: str) -> bool:
    """Returns `True` if:
    - value arg is a path to an existing directory
    - value arg is not a duplicate of another value saved to a different key in CONFIG_FILE

    Args:
        value (str): Must be a path to an existing directory that is not the same value of a different key.

    Returns:
        bool: `True` if value is a path to a directory which is not already saved to another key.
    """
    return os.path.isdir(value) and not value_found_in_config(value)



    
    
    
    
    
    
if __name__ == "__main__":
    bookmarks = load()
    num_args = len(sys.argv)
    
    # 1 args: ex: ./pbj
    if num_args == 1:
        # function that lists saved paths from json file
        list(bookmarks)
    
    # 2 args: ex: ./pbj [key | number | file.json] 
    elif num_args == 2:
        arg1 = sys.argv[1]

        # if [number], use bookmarks[keylist[number - 1]]
        if arg1.isdecimal():

        # if [key], use bookmarks[key]
        elif not arg1.endswith(".json"): # if arg is not file, it's a key
            # change_directory(arg1)
        # if [file.json] load(file.json)
        else:
            # load_json_file(arg1)
    # arg[1] is '-s': (save path)
    
        # 3 args: ex: ./pbj -s [key]
        
        # 4 args: ex: ./pbj -s [key] [path]

        
    # arg[1] is '-r': (remove path)

        # 3 args or more:
