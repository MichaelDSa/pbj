#!/usr/bin/env python3
from configparser import DuplicateSectionError
# from curses.ascii import isalnum
import json
# import typing
from tkinter import W
from typing import Dict, List, OrderedDict, Tuple, Dict
import os # OS routines for NT or Posix depending on what system we're on.
import sys

from pj import CONFIG_FILE # Built-in functions, types, exceptions, and other objects.
# import re # Support for regular expressions (RE).


bookmarks_file = "~/.config/pbj/bookmarks.json"
configuration_file = "~/.config/pbj/config.json"
BOOKMARKS_FILE = os.path.expanduser(bookmarks_file)
CONFIG_FILE = os.path.expanduser(configuration_file)

def category_is_valid(value: str) -> bool:
    """
    Returns True if `category` meets the criteria for
    being a key of the outer dict of `Dict[str, Dict[str,
    str]]` returned by `load()`.

   Requirements of `category`
   - must consist of alphabetical characters only
   - may not contain dots (like those of inner-keys) 

    Args:
        category (str): 
        candidate for being a key of outer
        dict returned by `load() -> Dict[str, Dict[str,
        str]]`.

    Returns:
        bool: 
        True if `category` meets requirements.
    """
    conditions: Tuple[bool, bool, bool] = (
        not value.isdecimal(), # is not a number
        value.isalpha(), # consists of alphabet characters only
        '.' not in value, # no dots in value
    )

    return False not in conditions
    

def change_directory(bookmarks: Dict[str, str]) -> None:
    return

def configure_configs(alter: bool = False) -> None:
    # bookmarks: Dict[str, Dict[str, str]] = load()
    default_cat: str = "Default" 
    candidate: str = "exit"

    # change default category via user if requested and config file exists:
    while alter and os.path.exists(CONFIG_FILE):
        candidate = input("new default category ('exit' to abort): ")
        alter = False if candidate.lower() == "exit" or candidate in bookmarks else True
        if alter:
            print(f"{candidate} not found. Use an existing category.")

    if not candidate.lower() == "exit":
        default_cat = candidate

    # set options for reading/creating config file:
    option = 'r' if os.path.exists(CONFIG_FILE) else 'x'
    if default_cat.lower() != "default":
        option = 'w'
    
    # value for `default_category`
    config_dict: Dict[str, str] = {"default_category": default_cat}

    try:
        # directories to create:
        dirs = os.path.dirname(CONFIG_FILE)
        # create parent directories if not exists:
        os.makedirs(dirs, exist_ok=True)

        # read/write/create file to persist data
        with open(CONFIG_FILE, option) as f:
            if option == 'r':
                config_dict = json.load(f)
            elif option == 'x' or option == 'w':
                json.dump(config_dict, f, indent=4)
                config_dict = json.load(f)
    except Exception as e:
        print(f"option: {option}")
        print(f"Exception handling {CONFIG_FILE} ({type(e).__name__}): {e}")
    
    # now handle the bookmarks file in case it's empty:

    # set up a default Dict[str, Dict[str, str]] if bookmarks file is empty
    default_keyval: Dict[str, str] = {"pbj_script": os.path.dirname(os.path .abspath(sys.argv[0]))}
    first_bookmark: Dict[str, Dict[str, str]] = {default_cat: default_keyval}

    if not os.path.exists(BOOKMARKS_FILE):
        try:
            dirs = os.path.dirname(BOOKMARKS_FILE)
            os.makedirs(dirs, exist_ok=True)
            with open(BOOKMARKS_FILE, 'x') as f:
                json.dump(first_bookmark, f, indent=4)
        except FileNotFoundError as e:
            print(f"FileNotFoundError in config_configs(). ({BOOKMARKS_FILE})")

def get_config_value(key: str ="default_category") -> str:
    value = ""
    try:
        with open(CONFIG_FILE, 'r') as f:
            value = json.load(f)[key]
    except FileNotFoundError as e:
        print(f"FileNotFoundError in get_default_cat(): {e}")
        print("suggestions: create config file with `config_configs()`")
    
    return value

def key_is_valid(key: str) -> bool:
    """Returns `True` if:
    - key arg does not have preceeding or trailing dot (`.`) characters
    - key arg is alphanumeric, or alphanumeric with the addition of dot (`.`) characters.

    Args:
        key (str): The key to be tested for naming adherance

    Returns:
        bool: `True` if key is valid
    """
    # conditions:
    values: Tuple[bool, ...] = (
        key.isdecimal(),
        not key.startswith("."),
        not key.endswith("."),
        key.replace(".", "").isalnum()
    )
    
    return False not in values
    
def list(bookmarks: Dict[str, Dict[str, str]], category: str = get_config_value("default_category")) -> Dict[str,str]:
    return
    
    
def list(bookmarks: Dict[str, str]) -> Tuple[List[str], Dict[str, str]]:
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

def load() -> Dict[str, Dict[str, str]]: 
    """returns a dict representing the keys and values of the CONFIG_FILE .json file

    Returns:
        Dict[str, str]: keys are the bookmarks. values are the paths
    """
    bookmarks: dict[str, Dict[str, str]] = {}
    option = 'r' if os.path.exists(BOOKMARKS_FILE) else 'x'
    try:
        dirs = os.path.dirname(BOOKMARKS_FILE)
        os.makedirs(dirs, exist_ok=True)

        with open(BOOKMARKS_FILE, option) as f:
            if option == 'r':
                bookmarks = json.load(f)
                bookmarks = sort_bookmarks(bookmarks)
    except FileNotFoundError:
        print("FileNotFoundError (load())")
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

    if file.endswith(".json"):
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
    
def save_to_category(category: str, key: str, path: str = os.getcwd()) -> None:
    """
    Assigns a`path`value to`key`in
    specified`category`. This`Dict[str,
    Dict[str, str]]`is subsequently saved
    to`CONFIG_FILE`via`save_to_config()`.
    - `path`is the value to save
    - `key` is the key of the `path` value.
    - `category` is the key of the value made up
    of`key-path.`
    - the whole`category-key-path`structure is saved to
    a`Dict[str, Dict[str, str]]`, which is subsequently
    saved to`CONFIG_FILE`in`json`format.
    - if no value given,`path`defaults
    to`os.getcwd()`(current working directory)

    Args:
        category (str): key* of`Dict[str*, Dict[str, str]]`
        key (str): key* of `Dict[str,Dict[str*, str]]`
        path (str, optional): value* of`Dict[str, Dict[str, str*]]`Defaults to`os.getcwd().`
    """
    path = os.path.expanduser(path)
    bookmarks: Dict[str, Dict[str, str]] = load()

    if not (category_is_valid(category) or key_is_valid(key)):
        # early return
        print(f"either {category} or {key} is invalid. Try again.")
        print("Category names may:")
        print("    - only contain alphabetical characters")
        print("    - not contain numbers")
        print("    - not contain dots")
        print("    - not have identical names")
        print("Key names may: ")
        print("    - contain alphanumeric characters")
        print("    - make use of dots. (eg: `dir.1`, `dir.2`, `dir.1.0`)")
        print("    - not have leading or trailing dots.")
        print("    - not consist solely of numbers")
        return
    
    #if category in bookmarks:
        # verify that path exists, that it is a directory, and is not a value in the category:
    if value_is_valid(path) and not value_found_in_dict(bookmarks[category], path):
        # save category, key and value to bookmarks:
        bookmarks[category][key] = path
        # save key value to CONFIG_FILE
        if save_to_config(bookmarks):
            print(f"'{path}' saved to '{key}' in category: '{category}'")
        else:
            print("`save_to_config()` failed in `save_to_category()`")
    else:
        print(f"Failed. Key invalid or path already saved")
        print(f"category: {category}")
        print(f"key:      {key}")
        print(f"value:    {path}")
            
    # else: 
    #     print(f"{category} not found")

def save_to_config(bookmarks: Dict[str, Dict[str, str]]) -> bool:
    """
    Save all paths to config file. This includes all
    new key-path items. All old key-path values in all
    categories are rewritten to the config file.

    Args:
        bookmarks (dict[str, str]): 
    """
    # sort bookmarks:
    bookmarks = sort_bookmarks(bookmarks)
    option: str = 'w' if os.path.exists(BOOKMARKS_FILE) else 'x'
    try:
        # in case parent directories do not exist:
        dirs = os.path.dirname(BOOKMARKS_FILE)
        os.makedirs(dirs, exist_ok=True)

        # read/write/create file to persist data:
        with open(BOOKMARKS_FILE, option) as f:
            json.dump(bookmarks, f, indent=4)
    except Exception as e:
        # Prints error message, and {type(e)..} name/type of exception and {e} error
        print(f"Error saving to CONFIG_FILE in save_to_copy(). ({type(e).__name__}): {e}")
        return False
    return True
    
def sort_bookmarks(bookmarks: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    sorted_dict: OrderedDict[str, Dict[str, str]] = OrderedDict()
    for ordered_key in sorted(bookmarks.keys()):
        ordered_inner_dict = OrderedDict(sorted(bookmarks[ordered_key].items()))
        sorted_dict[ordered_key] = ordered_inner_dict
    return sorted_dict
        
    
def value_found_in_bookmarks(value: str) -> bool:
    bookmarks: dict[str, Dict[str, str]] = load()
    return any(value in inner_dict.values() for inner_dict in bookmarks.values())

def value_found_in_dict(reference: Dict[str,str], value: str) -> bool:
    reference_set: set[str] = set(reference.values())
    return value in reference_set

def value_is_valid(value: str) -> bool:
    """Returns `True` if value arg is a path to an existing directory

    * Useage:
    >- client uses function to check if value is path to existing directory.
    >- client must separately perform check to see if value is assigned to another key in the same category.

    Args:
        value (str): > Must be a path to an existing directory that is not the same value of a different key.

    Returns:
        bool: > `True` if value is a path to a directory which is not already saved to another key.
    """
    # conditions tuple:
    conditions: Tuple[bool,...] = (
        os.path.isdir(value),
        os.path.exists(value),
    )
    return False not in conditions



    
    
    
    
    
    
if __name__ == "__main__":
    configure_configs() # this initializes a starting point for all config file json data. 
    bookmarks: Dict[str, Dict[str, str]] = load()
    num_args: int = len(sys.argv)
    default_category: str = get_config_value()

    # booleans indicating presence of short options:
    is_dash_s: bool = False
    is_dash_c: bool = False
    is_dash_r: bool = False
    is_test: bool = False
    if len(sys.argv) >= 2:
        arg: str = sys.argv[1]
        is_dash_s = arg == "-s"
        is_dash_c = arg == "-c"
        is_dash_r = arg == "-r"
        is_test = arg == "-test"
        
    
    # if arg[1] is -s|c: (save path)
    if num_args > 1 and is_dash_s or is_dash_c: ##### WORKING...
        # if 3 args: ex: ./pbj -s [alphanum (key)]
        if num_args == 3 and is_dash_s: #### WORKING...done
            key = sys.argv[2]
            save_to_category(default_category, key)
            #print(f"cmd: './pbj {sys.argv[1]} {sys.argv[2]}'") # save to default cat
        # elif 4 args: ex: ./pbj -s [category] [key]
        elif num_args == 4:
            # if sys.argv[1] == "-c"...
                # if not create_new_category(sys.argv[1]) #returns bool
                    # print statemnt
                    # exit
            print(f"cmd: './pbj -s {sys.argv[2]} {sys.argv[3]}'")
    elif num_args > 1 and is_test:
        value: str = "/home/michael/projects/Python/scripts/pbj"
        istrue = value_found_in_bookmarks(value);
        print(istrue)

    # if arg[1] is -r: (remove path)
    elif num_args > 1 and sys.argv[1] == "-r":
        # if 3 args: ex ./pbj -r [alphanum key | value]
        if num_args == 3:
            # if key: remove key-val from current category
            if bookmarks[default_category][sys.argv[2]]:
                print("cmd: './pbj -r {sys.argv[2]}'")
            # elif check if value exists; remove value
            else: # should be elif (new function:) value_found_in_all([value])
                print("cmd: './pbj -r {sysargv[2]}'")
        # elif 4 args: ex ./pbj -r [category-key] [nested-key]:
        elif num_args == 4:
            # if bookmarks[category], remove [category-key] [nested-key]
            if bookmarks[default_category][sys.argv[3]]:
                print("cmd: './pbj -r {sys.argv[2]} {sys.argv[3]}'")
                print("removing bookmarks[current_category]{sys.argv[3]]}")

    # if no args:
    elif num_args == 1:
        print("cmd: no args.")# new function: `ls_current_category(bookmarks[current_category])`
    # elif 1 args: ex: ./pbj
    elif num_args == 2: 
        arg1 = sys.argv[1]
        # change directory to the key of arg[1]
        print(f"cmd: './pbj {arg1}'") #change_directory(bookmarks[DEFAULT_CATEGORY], arg1)
    # elif 3 args: ex ./pbj [category] [alphanum | number]
    elif num_args == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        # if arg1 is a category:
        if arg1 in bookmarks:
            if arg2 in bookmarks[arg1]:
                #change_directory(bookmarks[arg1], arg2)
                print("cmd: './pbj {arg1} {arg2}")
            else:
                print(f"{arg2} not found in {arg1}")
        else:
            print(f"{arg1} not found")
                
                
