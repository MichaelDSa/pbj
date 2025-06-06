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
wrapper3: textwrap = textwrap.TextWrapper(width,indent2, indent2, replace_whitespace=False, drop_whitespace=True)
# content arrays:
name: Dict[str, str] = {
    "NAME": "pbj - change directories using mnemonics saved in a categorized list",
}


synopsis: Dict[str, Dict[str, str]] = {
    "SYNOPSIS": {
        "pbj [-s|-c|-cu|-cd|-r|-rc|-a]": "[category|key] [key]",
        "pbj -h|--help": "[all|synopsis|description|options|files|standards |examples|tldr|help|author|license]"
    }
}

description: Dict[str, Dict[str, str]] = {
    "DESCRIPTION": {
        "Save directories to chosen mnemonics:": "pbj saves your current working directory (cwd) to a key within a category.  The key to which the cwd is saved is user-created at the time of saving.  The key is saved to a either the current category selected by the user, a default category identified in the configuration file, or any other existing category specified by the user.",
        "Change directories using mnemonics:": "With pbj the user can cange directories by choosing either the 'speed-dial' or key of the numbered key-directory list associated with a category.  The category can be explicitly chosen, otherwise the current category is selected.  The user can browse num-key-dir lists of either the current, specified, or all categories.",
    }
}

options: Dict[str, Dict[str, str]] = {
    "OPTIONS": {
        "-s": "Safe save:  Save cwd to new user-created key in the current or specified category.  If the key already exists in the specified category, its value will not be changed.  If the specified category does not exist, it will not be created, and the key-dir will not be saved.",
        "-c": "Change or Create:  Save cwd to new user-created key in the current or specified category.  If the key already exists in the specified category it will be replaced.  If no arguments follow the -c option, the 'change key-name' dialogue is invoked. This is the dialogue in which the user can change the name of either a key or a category.",
        "-cu": "Change current category: The argument that follows -cu is the category to become the new current category. If no argument follows -cu, a dialogue is invoked, providing a numbered list of categories, of which the user selected category will become the new current cateogry.",
        "-cd": "Change default category:  The argument that follows -cd is the category to become the new default category. If no argument follows -cd, a dialogue is invoked, providing a numbered list of categories, of whch the suser selected category will become the new default category saved to the configuration file.",
        "-r": "Remove key from current category:  If the argument that follows -r is identical to a key in the current category, the key-directory pair will be deleted from the ctategory.",
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
       "print numbered key-directory list in current category:": "pbj",
       "switch to first list item directory in current category list:": "pbj 1",
       "switch to directory associated with key in current category list:": "pbj mykey",
       "print numbered key-directory list in specified category:": "pbj mycategory",
       "switch to directory associated with key/number in specified category:": "pbj mycategory mykey\nor\npbj mycategory 1",
       "safe save a directory to current category:": "pbj -s mynewkey",
       "save a directory to current category, replacing key-pair if it exists:": "pbj -c myoldkey",
       "change key/category name dialogue:": "pbj -c",
       "change current category using an interactive dialogue:": "pbj -cu",
       "change current category explicitly:": "pbj -cu mycat",
       "change current category explicitly and change directory:": "pbj -cu mycat mykey",
       "change default category using an interactive dialogue:": "pbj -cd",
       "change default category explicitly:": "pbj -cd mycat",
       "remove key from current category:": "pbj -r mykey",
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

license_content: list[str] = [
    "The MIT License",
    "Version N/A",
    "SPDX short identifier: MIT\n",
    "",
    "Open Source Initiative Approved License",
    "Copyright 2025, Michael D'Sa\n",
    "",
    "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n",
    "",
    "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n",
    "",
    "THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n",
]

version: Dict[str, str] = {
    "VERSION": "v0.2.1"
}

license: Dict[str, list[str]] = {
    "LICENSE": license_content
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
    help_version()
    help_license()

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

def help_version() -> None:
    content: Dict[str, str] = version
    for key, item in content.items():
        print(key)
        print(wrapper1.fill(item))
    print()

def help_license() -> None:
    content: Dict[str, list[str]] = license
    for key, items in license.items():
        print(key)
        for para in items:
            print(wrapper1.fill(para))
            
    return