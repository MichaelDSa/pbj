#!/usr/bin/env python3
import json
import tempfile
import textwrap
from tkinter import W
from typing import Dict, OrderedDict, Tuple, Dict
import os # OS routines for NT or Posix depending on what system we're on.
import sys

# You can change bookmarks_file valuevia config.json
# you can change configuration_file value here,
# but first manually create parent dirs.
bookmarks_file = "~/.config/pbj/bookmarks.json"
configuration_file = "~/.config/pbj/config.json"
BOOKMARKS_FILE = os.path.expanduser(bookmarks_file)
CONFIG_FILE = os.path.expanduser(configuration_file)

def category_is_valid(value: str) -> bool:
    """
    Returns True if `category` meets the criteria for
    being a key of the outer dict of `Dict[str, Dict[str,
    str]]` returned by `load_bookmarks()`.

   Requirements of `category`
   - must consist of alphabetical characters only
   - may not contain dots (like those of inner-keys) 

    Args:
        category (str): 
        candidate for being a key of outer
        dict returned by `load_bookmarks() -> Dict[str, Dict[str,
        str]]`.

    Returns:
        bool: 
        True if `category` meets requirements.
    """
    conditions: Tuple[bool, ...] = (
        value,
        not value.isdecimal(), # is not a number
        value.isalpha(), # consists of alphabet characters only
        '.' not in value, # no dots in value
    )

    return False not in conditions
    
def change_default_category(bookmarks: Dict[str, Dict[str, str]], category: str = None) -> bool:
    success: bool = True
    success_msg = "default category changed to "
    fail_msg = "default category not changed."
    if category:
        if category in bookmarks:
            if set_config_value(value=category):
                print(f"{success_msg}'{get_config_value()}'")
            else:
                success = False
        else:
            print(f"Category '{category}' not found. Choices:")
            change_default_category(bookmarks)
    else:
        print("change default category...")
        category = choose_category(bookmarks)
        if category_is_valid(category) and not name_is_key(bookmarks, category):
            if set_config_value(value=category):
                print(f"{success_msg} '{get_config_value()}'")
            else:
                success = False
        else:
            print(fail_msg)
            success = False

    return success

def change_directory(bookmarks: Dict[str, Dict[str, str]], category: str, keynum: str) -> str:
    num: int = -1 if not keynum.isdecimal() else int(keynum)
    target_path: str = ""

    if category in bookmarks:
        keys: list = list(bookmarks[category])
        if 1 <= num <= len(keys):
            target_path = bookmarks[category][keys[num - 1]]
        elif keynum in bookmarks[category]:
            target_path = bookmarks[category][keynum]
        else:
            target_path = os.getcwd()
    else:
        target_path = os.getcwd()
        
    target_path = os.path.expanduser(target_path)
        
    try:
        os.chdir(target_path)
    except OSError as e:
        print(f"OSError: in `change_directory()`:")
        print(f"{type(e).__name__}")
        print(f"{e}")
    return os.getcwd()


def change_keyname_dialogue(bookmarks: Dict[str, Dict[str, str]], category: str) -> None:
    print("/////////////////////////////////////")
    print("////// CHANGE KEYNAME DIALOGUE //////")
    print("/////////////////////////////////////")

    selection: str = ""
    is_cat: bool = False
    is_key: bool = False
    category_to_change: str = ""
    key_to_change: str = ""
    
    # selection dialogue:
    while selection == "": 
        print("    change category or key names")
        print(" ? to list all categories")
        print(" ! to list all keys in current category")
        print(" . to abort")
        print("or just enter name of key/cat to change.")
        selection = input("(cat|key|?|!|.) input: ")
        if selection in bookmarks: # if selection matches a category name
            category_to_change = selection
            is_cat = True
        elif selection in bookmarks[category]: # if seleciton is a key in current category
            key_to_change = selection
            is_key = True
        elif selection not in ('?', '!', '.'): # list dialogue or abort
            selection = ""

    is_question: bool = selection == "?"
    is_bang: bool = selection == "!"
    abort: bool = selection == "."
    
    if is_question: # select category from list dialogue
        category_to_change = choose_category(bookmarks)
        is_cat = True
        if category_to_change == ".":
            abort = True

    if is_bang: # select key from list dialogue
        key_to_change = choose_key(bookmarks, category)
        is_key = True
        if key_to_change == ".":
            abort = True
        
    if abort:
        print("aborted")
        return
    
    if is_cat: # change category name dialogue:
        choice: str = ""
        while choice == "":
            choice = input(f"('.' aborts) change category '{category_to_change}' to: ")
            if category_is_valid(choice) and not name_is_key(bookmarks, choice):
                if choice not in bookmarks:
                    change_category_name(bookmarks, category_to_change, choice)
                else:
                    print(f"'{choice}' name is already taken")
                    choice = ""
            elif choice == ".":
                print(f"name change aborted")
            else:
                print(f"'{choice}' is not a valid category name.")
                print(f"{' ' * (len(choice) + 2)} no dots; letters only; must not be key.")
                choice = ""

    elif is_key: # change key name dialogue:
        choice = ""
        while choice == "":
            choice = input(f"('.' aborts) change key '{key_to_change}' in {category} to: ")
            if key_is_valid(choice):
                if choice not in bookmarks[category]:
                    change_key_name(bookmarks, category, key_to_change, choice)
                else:
                    print(f"key name '{choice}' is already taken")
                    choice = ""
            elif choice == ".":
                print(f"name change aborted")
            else:
                print(f"'{choice}' is not a valid name.")
                print(f"{' ' * len(choice) + 2} no leading/trailing dots; alphanumeric; must not be category.")
                choice = ""
    

def choose_category(bookmarks: Dict[str, Dict[str, str]]) -> str:
    choices: list[str] = list(bookmarks)
    choice: str = ""
    chosen: bool = False
    while not chosen:
        for i, v in enumerate(choices):
            print(f"    {i + 1}) {v}")
        num: str = input("('.' aborts) choose by number: ")
        if num.isdecimal():
            num = int(num)
            if 0 < num <= len(choices):
                choice = choices[num - 1]
                chosen = True
        elif num == ".":
            choice = num
            chosen = True
    return choice

def choose_key(bookmarks: Dict[str, Dict[str, str]], category: str) -> str:
    choices: list[str] = list(bookmarks[category])
    choice: str = ""
    choice = "" 
    chosen = False
    ls_category(bookmarks, category)
    while not chosen:
        num: str = input("('.' aborts) choose by number: ")
        if num.isdecimal():
            num = int(num)
            if 0 < num <= len(choices):
                choice = choices[num - 1]
                chosen = True
        elif num == ".":
            choice = num
            chosen = True
    return choice  

def change_category_name(bookmarks: Dict[str, Dict[str, str]], category_to_change: str, new_name: str) -> None:
    value: Dict[str, str] = bookmarks[category_to_change]
    del bookmarks[category_to_change]
    bookmarks[new_name] = value
    save_to_bookmarks_file(bookmarks)

    # if changed category was default_category:
    default_category = get_config_value()
    if  category_to_change == default_category:
        set_config_value(value=new_name)

def change_key_name(bookmarks: Dict[str, Dict[str, str]], category: str, key_to_change: str, new_name: str) -> None:
    value: str = bookmarks[category][key_to_change]
    del bookmarks[category][key_to_change]
    bookmarks[category][new_name] = value
    save_to_bookmarks_file(bookmarks)

def delete_category(bookmarks: Dict[str, Dict[str, str]], category: str) -> bool:
    default_category: str = get_config_value()
    if category in bookmarks and category != default_category:
        del bookmarks[category]
        save_to_bookmarks_file(bookmarks)
        return True
    else:
        return False

def delete_key(bookmarks: Dict[str, Dict[str, str]], category: str, key: str) -> bool:
    if category in bookmarks and key in bookmarks[category]:
        del bookmarks[category][key]
        save_to_bookmarks_file(bookmarks)
        return True
    else:
        return False

def get_config_value(key: str ="default_category") -> str:
    # see list of values in `default_config` var
    # defined in init_config_file() definition.
    value = ""
    try:
        with open(CONFIG_FILE, 'r') as f:
            value = json.load(f)[key]
    except FileNotFoundError as e:
        print(f"FileNotFoundError in get_default_cat(): {e}")
        print("suggestions: create config file with `config_configs()`")
    
    return value

def get_current_category() -> str:
    default_category: str = get_config_value()
    current_category: str = os.environ.get("PBJ_CURRENT_CATEGORY")
    if not current_category:
        current_category = default_category
    return current_category

def get_terminal_width() -> int:
    width: int 
    if sys.stdout.isatty():
        width = os.get_terminal_size().columns
    else:
        swidth: str = os.environ.get("PBJ_TERM_WIDTH")
        width = 80 if not swidth.isdecimal() else int(swidth)
        if not swidth.isdecimal():
            print("Warning: sidth is not int")
    return width

def initialize() -> bool:
    success: bool = True
    if not init_config_file():
        success = False

    if not init_bookmarks_file():
        success = False
    
    if success and not init_default_category_resolve():
        bookmarks: Dict[str, Dict[str, str]] = load_bookmarks()
        if not change_default_category(bookmarks):
            success = False
            print("\nError in config.json:\nPlease set config.json key, \"default_category\" to an existing category from bookmarks.json")
            print("Run this dialogue again and choose a default category (recommended) or fix config.json manually.")
            bookmarks_file: str = get_config_value("bookmarks_file")
            if not bookmarks_file:
                bookmarks_file = "?"
            print(f"  bookmarks.json path: {bookmarks_file}")
            print(f"  config.json path: {CONFIG_FILE}\n")

    return success

def init_bookmarks_file() -> bool:
    success: bool = True
    
    # get path of bookmarks file from config. set config value if not set.
    bookmarks_file = get_config_value("bookmarks_file")
    if not bookmarks_file:
        set_config_value("bookmarks_file", BOOKMARKS_FILE)
        bookmarks_file = get_config_value("bookmarks_file")
        bookmarks_file = os.path.expanduser(bookmarks_file)
        
    # create initial bookmarks for new bookmarks.json:
    initial_bookmarks: Dict[str, Dict[str, str]] = {
        "default": {
            "pbj.bookmarks": f"{os.path.dirname(bookmarks_file)}",
            }
    }

    # test if parent directories of the bookmarks_file exists
    bookmarks_parent_dirs = os.path.dirname(bookmarks_file)
    if bookmarks_file != BOOKMARKS_FILE and not os.path.exists(bookmarks_parent_dirs):
        print(f"Please fix config.json in {CONFIG_FILE}.")
        print(f"the directory/directories associated with \"bookmarks_file\" \nmust be created by user, or choose a path that exists.")
        return False

    # determine option (r|w|x) for file access
    MODE_READ = 'r'
    MODE_WRITE = 'w'
    MODE_CREATE = 'x'

    option: str = None
    if not os.path.exists(bookmarks_file):
        option = MODE_CREATE
    elif os.path.getsize(bookmarks_file) <= 2:
        option = MODE_WRITE
    else:
        option = MODE_READ

    # contents of file saved here:
    file_read: Dict[str, Dict[str, str]]  = {}

    # file access read/write-to/create file:
    try:
        with open(bookmarks_file, option) as f:
            try:
                # only create parent dirs if set to default constant.
                if bookmarks_file == BOOKMARKS_FILE:
                    dirs = os.path.dirname(bookmarks_file)
                    os.makedirs(dirs, exist_ok=True)

                # write initial_bookmarks to file if not exists or has no content.
                if option in (MODE_CREATE, MODE_WRITE):
                    json.dump(initial_bookmarks, f, indent=4, sort_key=True)

                file_read = json.load(f)
            except json.JSONDecodeError as je:
                print(f"json.json.JSONDecodeError in init_bookmarks_file(): \n{je}")
    except Exception as e:
        print(f"option: {option}")
        print(f"Exception handling {bookmarks_file} ({type(e).__name__} in init_bookmarks_file() ): \n{e}")

    # check for user errors in file_read
    # user error list:
    errors_in_file_read: list[Tuple[str, str]] = []

    if not file_read:
        success = False
    else:
        for category, value in file_read.items():

            cat_conditions: list[Tuple[bool, str]] = [
                (not isinstance(category, str), "All categories must be double quoted. key-vals in config.json must be strings"),
                (not category_is_valid(category), "Category name characters may only contain alphabet chars."),
                (name_is_key(file_read, category), "Category names (outer-keys) must not be the same as key names (inner-keys)")
            ]
            for condition, message in cat_conditions:
                if condition:
                    success = False
                    errors_in_file_read += [(category, message)]

            for k, v in value.items():
                key_conditions: list[Tuple[bool, str]] = [
                    (not key_is_valid(k), "Keys may be alphanumeric; may have dots, but not leading/trailing dots."),
                    (k in file_read, "keys (inner-keys) may not have same name as a category (outer-keys)."),
                ]
                val_conditions: list[Tuple[bool, str]] = [
                    (not isinstance(v, str), "All keys and values in .json files must be double quoted unless surrounded by curly braces.")                   
                ]
                for condition, message in key_conditions: 
                    if condition:
                        success = False
                        errors_in_file_read += [(k, message)]

                for condition, message in val_conditions:
                    if condition:
                        success = False
                        errors_in_file_read += [(v, message)]

    if errors_in_file_read:
        print(f"\nErrors found in bookmarks.json file ({CONFIG_FILE}):")
        num: int = 0
        for cat, msg in errors_in_file_read:
            prefix: str = f"  {num + 1}) '{cat}: "
            width: int = get_terminal_width()
            wrapper = textwrap.TextWrapper(width, prefix, " " * len(prefix))
            print(wrapper.fill(msg))
            num += 1

    return success

def init_config_file() -> bool:
    # return value
    success: bool = True

    # early dismissal. do not allow user to create
    # directories via pbj, unless it's .config/pbj.
    config_file_dirs: str = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(config_file_dirs) or CONFIG_FILE != os.path.expanduser("~/.config/pbj/config.json"):
        print(f"All directories of '{config_file_dirs}' must exist to proceed.")
        print(f"User must create required directories. Create `{config_file_dirs}' and run pbj again.")
        return False
    
    # initial config default values:
    default_category: str = "default"
    bookmarks_file: str = BOOKMARKS_FILE
            
    # determine option (r|w|x) for file access
    MODE_READ = 'r'
    MODE_WRITE = 'w'
    MODE_CREATE = 'x'

    option: str = None
    if not os.path.exists(CONFIG_FILE):
        option = MODE_CREATE
    elif os.path.getsize(CONFIG_FILE) < 2:
        option = MODE_WRITE
    else:
        option = MODE_READ

    # we're going to access the file, but first
    # define initial default values:
    default_config: Dict[str, str] = {
        "default_category": default_category,
        "bookmarks_file": bookmarks_file
    }

    # whatever is in the file will be saved here:
    file_read: Dict[str, str] = {}

    # file access: read/write-to/create file:
    try:
        with open(CONFIG_FILE, option) as f:
            try:
                if option == MODE_CREATE or option == MODE_WRITE:
                    json.dump(default_config, f, indent=4, sort_keys=True)
                file_read = json.load(f) 
            except json.JSONDecodeError as je:
                print(f"json.json.JSONDecodeError in init_config_file(): \n{je}")
    except Exception as e:
        print(f"option: {option}")
        print(f"Exception handling {CONFIG_FILE} ({type(e).__name__}): \n{e}")

    # if json file has fewer keys than default_config,
    # save the missed key-vals to the file:
    if len(default_config) > len(file_read):
        # only add if key in default_config is missing from file_read
        file_read.update({k: v for k, v in default_config.items() if k not in file_read})
        try:
            option = MODE_WRITE
            with open(CONFIG_FILE, option) as f:
                json.dump(file_read, f, indent=4, sort_keys=True)
        except json.JSONDecodeError as je:
            print(f"json.json.JSONDecodeError in init_config_file(): \n{je}")
            print("found in inner try-except")

    # test file output captured by `file_read`:
    # user error list:
    errors_in_file_read: list[Tuple[str, str]] = []
    if not file_read:
        success = False
    else:
        for k, v in file_read.items():

            key_conditions: list[Tuple[bool, str]] = [
                (not k, "Key must be a double quoted non-empty string."),
                (not isinstance(k, str), "All keys-vals inside braces must be a double quoted string."),
                (k not in default_config, f"'{k}' does not belong in config.json")
            ]
            for condition, message in key_conditions:
                if condition:
                    success = False
                    errors_in_file_read += [(k, message)]

            value_conditions: list[Tuple[bool, str]] = [
                (not isinstance(v, str), "All key-vals inside braces must be a double quoted string."),
            ]
            for condition, message in value_conditions:
                if condition:
                    success = False
                    errors_in_file_read += [(v, message)]
    
    for k, v in default_config.items():
        if not k in file_read:
            success = False
            errors_in_file_read += [(k, f"'{k}' is missing from config.json")]
            print(f"'{k}' missing from config.json")
    
    # print errors if any:
    if errors_in_file_read:
        num: int = 0
        for kv, msg in errors_in_file_read:
            prefix: str = f"  {num + 1}) '{kv}: "
            width: int = get_terminal_width()
            wrapper = textwrap.TextWrapper(width, prefix, " " * len(prefix))
            print(wrapper.fill(msg))

    return success

def init_default_category_resolve() -> bool:
    bookmarks: Dict[str, Dict[str, str]] = load_bookmarks()
    default_category: str = get_config_value()
    if default_category not in bookmarks:
        return False
    return True
    
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
        not key.isdecimal(),
        not key.startswith("."),
        not key.endswith("."),
        key.replace(".", "").isalnum()
    )
    
    return False not in values

def ls_all(bookmarks: Dict[str, Dict[str, str]]) -> None:
    for category in bookmarks:
        ls_category(bookmarks, category)
        print("")

def ls_category(bookmarks: Dict[str, Dict[str, str]], category: str) -> None:
    if category in bookmarks:
        keys = list(bookmarks[category])
        print(f"paths found in `{category}':")
    #     for i, key in enumerate(keys):
    #         value = bookmarks[category][key]
    #         if len(value) > 80:
    #             value = value[:30] + "..." + value[-40:]
    #         print(f"   {i+1}) {key}: {value}")
    # else:
    #     return
        for i, key in enumerate(keys):
            prefix: str = f"    {i + 1}) {key}: "
            width: int = get_terminal_width() 
            wrapper = textwrap.TextWrapper(width, prefix, " " * len(prefix))
            value: str = bookmarks[category][key]
            # if len(value) > 80:
            #     fmt: str = value
            #     value = fmt[:30] + "..." + fmt[-40:]
            print(wrapper.fill(value))

def load_bookmarks() -> Dict[str, Dict[str, str]]: 
    bookmarks_file: str = get_config_value("bookmarks_file")
    bookmarks_file = os.path.expanduser(bookmarks_file)
    bookmarks: dict[str, Dict[str, str]] = {}

    try:
        with open(bookmarks_file, 'r') as f:
            try:
                bookmarks = json.load(f)
            except json.JSONDecodeError as je:
                print(f"json.JSONDecodeError in load_bookmarks(): \n{je}")
    except FileNotFoundError:
        print("FileNotFoundError (load())")

    # sorting is redundant in case user modifies bookmarks.json manually
    bookmarks = sort_bookmarks(bookmarks) 
    return bookmarks

def name_is_key(bookmarks: Dict[str, Dict[str, str]], key: str) -> bool:
    """
    Returns`True`if`key`is found as a key in any category

    Args:
        bookmarks (Dict[str, Dict[str, str]]): _description_
        key (str): _description_

    Returns:
        bool: _description_
    """
    for category in bookmarks:
        if key in bookmarks[category]:
            return True
    return False

def remove_duplicate_values(bookmarks: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    found_dups: set[str] = set()
    duplicates: Dict[str, str] = {}
    all_duplicates: Dict[str, Dict[str, str]] = {}
    for category, item in bookmarks.items():
        duplicates.clear()
        found_dups.clear()
        # catch all duplicate values
        for key, path in item.items():
            if path in found_dups:
                duplicates[key] = path
            else:
                found_dups.add(path)
        # save duplicates for reporting
        if len(duplicates) > 0:
            for k, p in duplicates.items():
                all_duplicates.setdefault(category, {})[k] = p

        # delete found duplicates from bookmarks
        for key in duplicates:
            del bookmarks[category][key]
    # return the found duplicates for reporting
    return all_duplicates
    
def save_to_category(bookmarks: Dict[str, Dict[str, str]], category: str, key: str, path: str = os.getcwd()) -> bool:
    """
    Assigns a`path`value to`key`in
    specified`category`. This`Dict[str,
    Dict[str, str]]`is subsequently saved
    to`BOOKMARKS_FILE`via`save_to_bookmarks_file()`.
    - `path`is the value to save
    - `key` is the key of the `path` value.
    - `category` is the key of the value made up
    of`key-path.`
    - the whole`category-key-path`structure is saved to
    a`Dict[str, Dict[str, str]]`, which is subsequently
    saved to`BOOKMARKS_FILE`in`json`format.
    - if no value given,`path`defaults
    to`os.getcwd()`(current working directory)

    Args:
        category (str): key* of`Dict[str*, Dict[str, str]]`
        key (str): key* of `Dict[str,Dict[str*, str]]`
        path (str, optional): value* of`Dict[str, Dict[str, str*]]`Defaults to`os.getcwd().`
    """
    path = os.path.expanduser(os.path.abspath(path))
    success = False

    if not (category_is_valid(category) and key_is_valid(key)):
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
        return success
        
    if not value_is_valid(path):
        print("invalid value")
        return success

    if category in bookmarks: 
        if value_found_in_dict(bookmarks[category], path):
            print(f"This path is already saved in {category}:")
            return success


    if name_is_key(bookmarks, category) or key in bookmarks or category == key:
        print(f"'{category}' is a key in another category.")
        print("Please choose a different category name")
        print("`pbj -a` to list all categories and bookmarks")
        return success

        
    # save key-value to category in local bookmarks dict
    bookmarks.setdefault(category, {})[key] = path
        ######################
        # this is kind of the same as:
        # if category in bookmarks:
        #     bookmarks[category][key] = path
        # else:
        #     bookmarks[category] = {key: path}
    
    # save bookmarks to file:
    if save_to_bookmarks_file(bookmarks):
        print(f"saved to '{key}' in category: '{category}':")
        print(f"'{path}'")
        success = True
    else:
        print("`save_to_bookmarks_file()` failed in `save_to_category()`")
        success = False
    
    return success

def save_to_bookmarks_file(bookmarks: Dict[str, Dict[str, str]]) -> bool:
    """
    Save all paths to BOOKMARKS_FILE. This includes all
    new key-path items. All old key-path values in all
    categories are rewritten to the file.

    Args:
        bookmarks (dict[str, str]): 
    """
    # prepare bookmarks with sorting and pruning:
    # sort bookmarks:
    bookmarks = sort_bookmarks(bookmarks)
    # prune. remove duplicate values from all categories. Save dups for reporting:
    dups: Dict[str, Dict[str, str]] = remove_duplicate_values(bookmarks)
    # print a report of which duplicates in their categories were deleted:
    if len(dups) > 0:
        print("deleted duplicate key-values:")
        for category in dups:
            print(f"{category}:")
            for key, path in dups[category].items():
                print(f"  {key}: {path}")

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
        print(f"Error saving to BOOKMARKS_FILE in save_to_bookmarks_file(). ({type(e).__name__}): {e}")
        return False
    return True
    
def set_config_value(key: str = "default_category", value: str = "default") -> bool:
    success: bool = False
    config: Dict[str, str] = {}

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError as je:
                    print(f"json.JSONDecodeError in set_config_value(): \n{je}")
        except Exception as e:
            print(f"set_config_value() Exception handling... {CONFIG_FILE} \nexception type: {type(e).__name__}: \n{e}")

    if config and key in config: # write the new key-val to file
        config[key] = value
        try: 
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4, sort_keys=True)
        except Exception as e:
            print(f"set_config_value() Exception handling... {CONFIG_FILE} \nexception type: {type(e).__name__}: \n{e}")
        success = True
    else:
        print("set_config_value(): key not found")

    return success

def set_current_category(bookmarks: Dict[str, Dict[str, str]], category: str = None, keynum: str = None)-> bool:
    success: bool = True
    old_current_category: str = get_current_category() 
    new_current_category: str = ""
    new_current_directory: str = ""
    if category == None:
        print(f"current category: {old_current_category}")
        print("change current category:")
        choice = choose_category(bookmarks)
        if choice != ".":
            new_current_category = choice
        else:
            success = False
    elif category_is_valid(category) and category in bookmarks:
        new_current_category = category
    else:
        success = False
    
    key: str = keynum
    # assign value to `new_current_directory`, but first:
    # if success, and keynum is a number, get the corresponding key
    if success and keynum:
        keys: list = list(bookmarks[new_current_category])
        num: int = -1 if not keynum.isdecimal() else int(keynum)
        if 1 <= num <= len(keys):
            key = keys[num -1]
        # if key is relevant:  
        if key in bookmarks[new_current_category]:
            new_current_directory = bookmarks[category][key]
        else:
            success = False

    # if cat and dir change successful, prepare to write
    # current category env to temp file.  The bash script
    # will set the env and change dir using the file contents
    if success:
        parent_pid: int = os.getppid()
        temp_dir: str = tempfile.gettempdir()
        temp_filename: str = os.path.join(temp_dir, f"pbj_set_current_category_{parent_pid}.tmp")

        # write to temp file:
        try:
            # bash script will source and rm temp file
            with open(temp_filename, 'w') as f:
                # bash script will export variable
                f.write(f"PBJ_CURRENT_CATEGORY=\"{new_current_category}\"\n")
                if new_current_directory:
                    # bash script will cd to new dir if var exists
                    f.write(f"PBJ_NEWDIR=\"{new_current_directory}\"\n")
        except Exception as e:
            success = False
            print(f"set_current_category() Exception handling... {temp_filename}\nexception type: {type(e).__name__}: \n{e}")

    # set env var, PBJ_CURRENT_CATEGORY in bash script
    return success

def sort_bookmarks(bookmarks: Dict[str, Dict[str, str]]) -> OrderedDict[str, OrderedDict[str, str]]:
    sorted_dict: OrderedDict[str, Dict[str, str]] = OrderedDict()
    for ordered_key in sorted(bookmarks.keys()):
        ordered_inner_dict = OrderedDict(sorted(bookmarks[ordered_key].items()))
        sorted_dict[ordered_key] = ordered_inner_dict
    return sorted_dict
        
    
def value_found_in_bookmarks(bookmarks: Dict[str, Dict[str, str]], value: str) -> bool:
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
    # verify config.json & bookmarks.json. Validate all
    # .json data. Create starter files if they dont exist.
    # verify that default_category matches a category in 
    # bookmarks.json. Bash script (pbj-liason) depends on success.
    if not initialize():
        sys.exit(1)
    bookmarks: Dict[str, Dict[str, str]] = load_bookmarks()
    num_args: int = len(sys.argv)
    default_category: str = get_config_value()
    current_category: str = get_current_category()

    # booleans indicating presence/absence of short and long options:
    no_dash: bool = True
    opt_h: bool = False
    opt_a: bool = False
    opt_s: bool = False
    opt_c: bool = False
    opt_cd: bool = False
    opt_cu: bool = False
    opt_r: bool = False
    opt_rc: bool = False
    is_test: bool = False
    long_opt_set_term_width: bool = False
    if len(sys.argv) >= 2:
        arg: str = sys.argv[1]
        no_dash = not arg.startswith('-')
        opt_h = arg == "-h" or arg == "--help"
        opt_a = arg == "-a"   # list all categories and keys
        opt_s = arg == "-s"   # save [category and] key
        opt_c = arg == "-c"   # create/change [category] [key]
        opt_cd = arg == "-cd" # change default category
        opt_cu = arg == "-cu" # change current category
        opt_r = arg == "-r"   # remove key
        opt_rc = arg == "-rc" # remove category
        is_test = arg == "-test"  # tests for noob devs
        
    # help options
    if num_args > 1 and opt_h:
        import pbj_help

        if num_args == 2:
            pbj_help.help_name()
            pbj_help.help_synopsis()
        elif num_args > 2:
            help_option: str = sys.argv[2].lower()
            if help_option == "all":
                pbj_help.help()
            elif help_option == "synopsis":
                pbj_help.help_synopsis()
            elif help_option == "description":
                pbj_help.help_description()
            elif help_option == "options":
                pbj_help.help_options()
            elif help_option == "files":
                pbj_help.help_files()
            elif help_option == "standards":
                pbj_help.help_standards()
            elif help_option == "examples":
                pbj_help.help_examples()
            elif help_option == "tldr":
                pbj_help.help_examples(True)
            elif help_option == "help":
                pbj_help.help_example_help_options()
            elif help_option == "author":
                pbj_help.help_authors()
            elif help_option == "version":
                pbj_help.help_version()
            elif help_option == "license":
                pbj_help.help_license()
    # list all bookmarks:
    elif num_args > 1 and opt_a:
        ls_all(bookmarks)
    # if 2 args and arg[1] is -c. ex: `./pbj -c`
    elif num_args == 2 and opt_c: 
        change_keyname_dialogue(bookmarks, current_category)
    # if arg[1] is -s|-c: (save bookmark | change value or create category)
    elif num_args > 2 and opt_s or opt_c: 
        # if 3 args: ex: ./pbj -s [alphanum (key)] (save to default)
        if num_args == 3: 
            key: str = sys.argv[2]
            if key in bookmarks[current_category]:
                if opt_s:
                    print(f"key ({key}) already assigned to '{bookmarks[current_category][key]}'.")
                    print("use '-c' option to change key's value")
                elif opt_c:
                    old_value: str = bookmarks[current_category][key]
                    if save_to_category(bookmarks, current_category, key):
                        new_value: str = bookmarks[current_category][key]
                        print(f"Old {key} value: {old_value}")
                        print(f"New {key} value: {new_value}")
            else:
                save_to_category(bookmarks, current_category, key)
        # elif 4 args: ex: ./pbj -s|-c [category] [key] (save to specified cat. or newly created cat)
        elif num_args == 4: 
            category: str = sys.argv[2]
            key: str = sys.argv[3]
            if category in bookmarks:
                if key in bookmarks[category]:
                    if opt_s:
                        print(f"key ({key}) already assigned to '{bookmarks[category][key]}'")
                        print("use '-c' option to change key's value")
                    elif opt_c:
                        old_value: str = bookmarks[category][key]
                        if save_to_category(bookmarks, category, key):
                            new_value: str = bookmarks[category][key]
                            print(f"Old {key} value: {old_value}")
                            print(f"New {key} value: {new_value}")                       
                else:
                    save_to_category(bookmarks, category, key)
            elif opt_c:
                    if save_to_category(bookmarks, category, key):
                        print(f"'{category}' category created. `pbj {category}` to list bookmarks.")
            else:
                print("Use `-c` option to create new categories")

    #####TEST BRANCH#####
    elif num_args > 1 and is_test:
        set_current_category(bookmarks, "default", "pbj")

    # change default category
    elif num_args > 1 and opt_cd:
        if num_args == 2:
            change_default_category(bookmarks)
        elif num_args == 3:
            category: str = sys.argv[2]
            change_default_category(bookmarks, category)
    # if arg[1] is -r: (remove path) WORKING...
    elif num_args > 2 and opt_r:
        # if 3 args: ex ./pbj -r [alphanum key]
        if num_args == 3: # remove keypair from current_category
            key: str = sys.argv[2]
            path: str = ""
            if key in bookmarks[current_category]:
                path = bookmarks[current_category][key]
            if delete_key(bookmarks, current_category, key):
                print(f"keypair deleted from '{current_category}':")
                print(f"{key}: {path}")
            else:
                print("key does not exist.")
        
        # elif 4 args: ex ./pbj -r [category-key] [nested-key]:
        elif num_args == 4: # remove keypair from specified category
            category: str = sys.argv[2]
            key: str = sys.argv[3]
            path: str = ""
            if category in bookmarks and key in bookmarks[category]:
                path = bookmarks[category][key]
            if delete_key(bookmarks, category, key):
                print(f"keypair deleted from '{category}':")
                print(f"{key}: {path}")
            else:
                print("key or category does not exist")
    # ./pbj -rc [category]
    elif num_args > 2 and opt_rc:
        category: str = sys.argv[2]
        accept: bool = False
        found: bool = False
        # confirm with user if category exists
        if category in bookmarks:
            found = True
            print(f"Deleting category ({category})...")
            answer: str = input(f"Are you sure? [y/N]: ")
            accept = True if answer.lower() == "y" else False
        else:
            print("category not found")
        # remove category from bookmarks:
        if accept and delete_category(bookmarks, category):
            print(f"'{category}' category was deleted.")
        elif found:
            print("deletion aborted/unsuccessful")
            print("note: current category cannot be deleted.")

######-cu#########################################
    elif num_args > 1 and opt_cu:
        if num_args == 2:
            # change_current_category_dialogue()
            set_current_category(bookmarks)
            
        if num_args == 3:
            # specify new current category
            new_category: str = sys.argv[2]
            set_current_category(bookmarks, new_category)

        if num_args == 4:
            # speciry new current category and key to cd to.
            new_category: str = sys.argv[2]
            keynum: str = sys.argv[3]
            set_current_category(bookmarks, new_category, keynum)

########-cu#######################################

    elif no_dash:
        # if no args:
        if num_args == 1:
            ls_category(bookmarks, current_category)
        # elif 1 args: ex: ./pbj
        elif num_args == 2: #change directory current_category: ./pbj [key | num]
            arg1: str = sys.argv[1]
            # check if arg1 is category:
            if arg1 in bookmarks:
                ls_category(bookmarks, arg1)
            # change directory to the key of arg[1]
            else: 
                dir: str = change_directory(bookmarks, current_category, arg1)
                print(os.path.abspath(dir))
            # print(os.getcwd())
        # elif 3 args: ex ./pbj [category] [alphanum | number]
        elif num_args == 3:
            category = sys.argv[1]
            keynum = sys.argv[2]
            # if category does not exist, current working directory returned.
            dir: str = change_directory(bookmarks, category, keynum)
            print(os.path.abspath(dir))
    else:
        import pbj_help
        pbj_help.help_synopsis()
    # os.system("/bin/bash") 
    # this will create a new subshell in the client terminal
    # for example, to exit the terminal you'll have to ctr-d 
    # multiple times. Instead, use bash wrapper.
                
