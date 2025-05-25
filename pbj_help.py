#!/usr/bin/env python3
import textwrap
from typing import Dict, List

from pbj import CONFIG_FILE, get_config_value, get_terminal_width

width: int = get_terminal_width()
indent1: str = f"{' ' * 7}"
indent2: str = f"{indent1 * 2}"
indent3: str = f"{indent1 * 3}"
wrapper1: textwrap = textwrap.TextWrapper(width, indent1, indent1, replace_whitespace=False)
wrapper2: textwrap = textwrap.TextWrapper(width, indent2, indent2, replace_whitespace=False)

# content arrays:
name: Dict[str, str] = {
    "NAME": "pbj - change directories using mnemonics saved in a categorized list",
}


synopsis: Dict[str, Dict[str, str]] = {
    "SYNOPSIS": {
        "pbj [-s|-c|-cd|-r|-rc|-a]": "[category|key] [key]",
        "pbj -h|--help": "[all|synopsis|description|options|files|standards |examples|tldr|help|author|license]"
    }
}

description: Dict[str, Dict[str, str]] = {
    "DESCRIPTION": {
        "Save directories to chosen mnemonics:": "pbj saves your current working directory (cwd) as a key within a category.  The key to which the cwd is saved is user-created at the moment of saving.  The key is saved to a default category previously selected by the initialize process, or by the user.  The default category is also known as the current category.  Key-directories can also be explicitly saved to non-default/non-current categories.",
        "Change directories using mnemonics:": "With pbj the user can cange directories by choosing either the 'speed-dial' or key of the numbered key-directory list associated with a category.  The category can be explicitly chosen, or else the current/default category is selected.  The user can browse num-key-dir lists of either the current/default or specified categories."
    }
}

options: Dict[str, Dict[str, str]] = {
    "OPTIONS": {
        "-s": "Safe save:  Save cwd to new user-created key in the default or specified category.  If the key already exists in the specified category, its value will not be changed.  If the specified category does not exist, it will not be created, and the key-dir will not be saved.",
        "-c": "Change or Create:  Save cwd to new user-created key in the default or specified category.  If the key already exists in the specified category it will be replaced.  If no arguments follow the -c option, the 'change key-name' dialogue is invoked. This is the dialogue in which the user can change the name of either a key or a category.",
        "-cd": "Change current/default category:  The argument that follows -cd is the category to become the new current/default. If no argument follows -cd, a dialogue is invoked, providing a numbered list of categories to choose from, which will become the new current/default category if selected.",
        "-r": "Remove key from current/default category:  If the argument that follows -r is identical to a key in the current/default category, the key-directory pair will be deleted from the ctategory.",
        "-rc": "Remove category:  If the argument that follows -rc is identical to a category in the bookmarks file, it will be removed along with it's  key-dir pairs.",
        "-a": "List all categories and their key-directory contents",
        }
}

files: Dict[str, List[str]] = {
    "FILES": [
        f"config.json: {CONFIG_FILE}",
        f"bookmarks.json: {get_config_value("bookmarks_file")}"
    ]
}

standards: Dict[str, Dict[str, str]] = {
    "STANDARDS": {
        "Category naming rules:": "Category names must use only aphabetical characters.  Neither spaces, numbers, nor symbols may be included in a category name.  Category names may not be identical to key names",
        "Key naming rules:": "Key names may consist of alphanumeric characters.  Dots (.) may be included within a key name, but may not preceed or follow the key name (no leading or trailing dots).  Key names may not consist entirely of numerical charaters, but may consist entierly of alphabet chars.  key names may not be identical to category names.",
        "directory naming rules:": "Directories must follow the file-system naming conventions of the host operating system.  Paths included in bookmarks.json must be directores, not files. Duplicate directory names within a category are deleted any time the bookmarks.json file is saved.",
    }
}

tldr: Dict[str, Dict[str, str]] = {
    "EXAMPLES (TL;DR)": {
        "Print numbered key-directory list in current/default category:": "pbj",
        "Switch to first list item directory in current/default category list:": "pbj 1",
        "Switch to directory associated with key in current/default category list:": "pbj mykey",
        "Print numbered key-directory list in specified category:": "pbj mycategory",
        "Switch to directory associated with key/number in specified category:": f"pbj mycategory mykey \n{indent2}or\n{indent1}pbj mycategory 1",
        "Safe save a directory to current/default category:": "pbj -s mynewkey",
        "save a directory to current/default category, replacing key-pair if it exists:": "pbj -c myoldkey",
        "change key/category name dialogue:": "pbj -c",
        "change current/default category dialogue:": "pbj -cd",
        "change current/default category explicitly:": "pbj -cd mycat",
        "remove key from current/default category:": "pbj -r mykey",
        "remove category and all associated key-directory pairs:": "pbj -rc mycat",
        "print all categories and keys:": "pbj -a",
    }
}

example_help_options: Dict[str, Dict[str, str]] = {
    "Help options":
        {
            "display synopsis and tldr": "pbj -h|--help",
            "display all help info:": "pbj -h|--help all",
            "display specific help section:": "pbj -h|--help [synopsis|description|options|files|standards |examples|tldr|help|author|license]",
            "print examples in conventional order": "pbj -h|--help examples",
            "print examples in reverse order (for short terminal heights)": "pbj -h|--help tldr",
        }
}

authors: Dict[str, List[str]] = {
    "AUTHORS": [
        "Michael D'Sa",
    ]
}

def help() -> None:
    help_name()
    help_synopsis()
    help_description()
    help_options()
    help_files()
    help_standards()
    help_examples()
    help_authors()

def help_name() -> None:
    content: Dict[str, str] = name
    for title, desc in content.items():
        print(title)
        print(wrapper1.fill(desc) + "\n")
    return

def help_synopsis() -> None:
    content: Dict[str, Dict[str, str]] = synopsis
    for k, items in content.items():
        print(k)
        for k, v in items.items():
            wrapper: textwrap = textwrap.TextWrapper(width, indent1, " " * (len(indent1) + len(k) + 1), replace_whitespace=False)
            item: str = k + " " + v
            print(wrapper.fill(item))
    print()
    return

def help_description() -> None:
    content: Dict[str, Dict[str, str]] = description
    for key, items in content.items():
        print(key)
        for k, v in items.items():
            print(wrapper1.fill(k))
            print(wrapper1.fill(v) + "\n")
    return

def help_options() -> None:
    content: Dict[str, Dict[str, str]] = options
    wrapper: textwrap = textwrap.TextWrapper(width, indent1, indent2, replace_whitespace=False)  
    for key, items in content.items():
        print(key)
        for k, v in items.items():
            entry: str = k + f"{' ' * (len(indent1) - len(k))}" + v
            print(wrapper.fill(entry) + "\n")

def help_standards() -> None:
    content: Dict[str, Dict[str, str]] = standards
    for key, items in content.items():
        print(key)
        for k, v in items.items():
            print(wrapper1.fill(k))
            print(wrapper2.fill(v) + "\n")
    return

def help_files() -> None:
    content: Dict[str, List[str]] = files
    for key, items in content.items():
        print(key)
        for s in items:
            print(wrapper1.fill(s))
    print()
    return

def help_examples(reverse: bool = False) -> None:
    # the examples can be printed in reverse order by reversing the tldr dict
    # reason: the list of examples is long. short terminals will benefit by 
    # having the simplest examples in view.
    reverse_note: str = "-- Scroll up 4 reverse print"

    # inner keys (description of examples) start with a dash in this tldr document
    # reminder: wrapper1 & wrapper2 are globals
    dash_indent1: str = "     - "
    dash_indent2: str = f"{indent1 + dash_indent1}"
    wrapperk1 = textwrap.TextWrapper(width, dash_indent1, indent1, replace_whitespace=False)
    wrapperk2 = textwrap.TextWrapper(width, dash_indent2, indent2, replace_whitespace=False)

    content: Dict[str, Dict[str, str]] = tldr 
    content.update(example_help_options)

    if reverse:
        content = dict(reversed(content.items()))


    # print content in either forward/reverse (ascending/descending) order
    for key, items in content.items():
        # print the key first if not reverse
        if not reverse:
            if key.lower() == "help options":
                print(wrapper1.fill(key))
            else:
                print(key + "\n")
        # reverse inner dict if necessary
        else: 
            items = dict(reversed(items.items()))
        # print the inner dict keys & vals:
        for k, v in items.items():
            # inner keys (descriptions of examples) start with a dash in this tldr document
            wrapperk: textwrap.TextWrapper = wrapperk2 if key.lower() == "help options" else wrapperk1
            wrapperv: textwrap.TextWrapper = wrapper1 if key.lower() != "help options" else wrapper2
            # the example with heading, "display specific help section", needs special wrapping
            if k.lower() == "display specific help section:":
                wrapperv = textwrap.TextWrapper(width, indent2, " " * (len(indent1) * 4), replace_whitespace=False)
            print(wrapperk.fill(k))
            print(wrapperv.fill(v) + "\n")
        # print the key and reverse_note if in reverse order:
        if reverse:
            indent = indent1 if key.lower() == "help options" else ""
            revkey: str = key + f"{' ' * (width - len(reverse_note + indent + key))}{reverse_note}\n"
            wrapper: textwrap.TextWrapper = wrapper1 
            if key.lower() == "help options":
                print(wrapper.fill(revkey) + "\n")
            else:
                print(revkey)
    
def help_example_help_options() -> None:
    content: Dict[str, Dict[str, str]] = example_help_options
    for key, items in content.items():
        print(wrapper1.fill(key))
        for k, v in items.items():
            wrapper: textwrap = wrapper2
            if k.lower() == "display specific help section:":
                wrapper = textwrap.TextWrapper(width, indent2, " " * (len(indent2) + 14), replace_whitespace=False)
            print(wrapper.fill(k))
            print(wrapper.fill(v) + "\n")
    return

def help_authors() -> None:
    content: Dict[str, List[str]] = authors
    for key, items in content.items():
        print(key)
        for s in items:
            print(wrapper1.fill(s))
    print()
    return

def help_license() -> None:
    return