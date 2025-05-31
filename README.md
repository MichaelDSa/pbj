<div align="center">

# pbj 
![pbj sandwich](assets/img1_12.png)
##### Organized Bookmarks for your Directories
</div>

## TOC
* [What is pbj?](#what-is-pbj)
  * [Development](#development)
  * [Why the Name, 'pbj' was Chosen](#why-the-name-pbj-was-chosen)
* [Getting Started:](#getting-started)
  * [Installation:](#installation)
  * [Advanced Installation:](#advanced-installation)
* [Executing pbj:](#executing-pbj)
* [Demo:](#demo)
* [Examples / TLDR](#examples--tldr)
* [Help:](#help)
  * [Troubleshooting Installation](#troubleshooting-installation)
  * [Known Issues:](#known-issues)
* [Author:](#author)
* [License:](#license)

## What is pbj?:

* `cd` to your most common, or overly verbose directories with `pbj [your_bookmark]`
* **`pbj`** is a directory bookmarks manager created to covercome the friction of remembering and navigating to long directory names on the command line.  
* **`pbj`** will save your directories using bookmark names you can easily remember.
* **`pbj`** prints directory lists of long directory urls neatly, with ledgible text wrapping
* **`pbj`** mitigates unmanagably long lists of bookmarks with categorization options.

### Development:

* **`pbj`** works as expected on my **Ubuntu 24.04** laptop.
* There is one known issue currently being worked on.
* There are plans to make pbj functional for use with mac and win.

### Why The name, 'pbj' was Chosen
I like ***choice***, and I like *peanutbutter and jelly*. With **`pbj`**, you get to refer to your directories with whatever name you choose!
* Btw,  `pbj` is made with **Python**, **Bash**, and **JSON**. 

---

## Getting Started

### Installation:

#### 1. install Dependencies if necessary:
pbj has not yet been tested on other shells like zsh or fish.

**Dependencies:** Python 3. 
* check if Python 3 is installed (note the capital 'V'):

        $ python3 -V

* If Python3 is not installed:

        $ sudo apt install python3
#### 2. Clone pbj:
* (optional) Make a new directory for pbj:

        $ mkdir your_directory

* clone pbj repository in your directory: 
    
        $ cd your_directory
        $ git clone https://github.com/MichaelDSa/pbj.git

#### 3. Add this to ~/.bashrc:


        source ~/your_directory/pbj/pbj

###### That's all you need to do. 

---

## Advanced Installation:
The steps below might be overkill for some, but they were tested anyway.  If they look unfamiliar, just stick with the above method.

### Alternatives to step 2. `~/.local/` or `/usr/bin` installation:
These installation methods involve creating symlinks in either `~/.local` or `usr/bin`.   

After following step 1 by cloning the pbj repository in your preferred dir, Look at either **a)** or **b)** as alternatives to step 2.

### a) create symlinks in `~/.local/share/` & `~/.local/bin`

1. Link the cloned directory to `~/.local/share`:

        ln -s ~/your_directory/pbj ~/.local/share/pbj

2. link the application in the cloned directory to `~/.local/bin` via the symlink you just created:

        ln -s ~/.local/share/pbj/pbj ~/.local/bin/pbj

3. add this to `~/.bashrc`: 

       source ~/.local/share/pbj/pbj 


* in place of step 3, you can try adding this to `~/.bashrc` instead:

        source pbj

### b) create symlink in `/usr/bin`:

1. link the pbj applicaton to `/usr/bin`. you will have to enter your credentials and pres enter:

        sudo ln -s /usr/bin/pbj ~/your_directory/pbj/pbj


2. add this to `~/.bashrc`:

        source /usr/bin/pbj

* in place of step 2, you can try adding this to `~/.bashrc` instead:

        source pbj

---

## Executing `pbj`:
* once you've installed **`pbj`**, you need to initialize the config files by doing this:

        $ pbj

* Each time **`pbj`** runs, both config files go through a validation check, to maintain a consistent experience, reducing *gotchas* a user might experince after modifying config files.
* The script config file will be installed in `~/.config/pbj/config.json`
* The bookmarks config file will be installed in `~/.config/pbj/bookmarks.json`
  * `bookmarks.json` can be moved to a directory of your choice by modifing the `"bookmarks_file"` key in `config.json`
* Note: **`pbj`** must be sourced (not executed), either by adding the `source` command in the `~/.bashrc`, or on the command line with the command, `source pbj` (or `source path/to/pbj`).

---

## Demo:
<div align="center">

![](./assets/output2.gif) 

</div>

## Examples / TLDR:

 Print a list of saved directories, like this:

    $ pbj

You will then get a list like this:
        
    paths found in 'default':
        1) d.img: /home/user/Downloads/images
        2) d.sta: /home/user/Downloads/Statements
        3) mydir: /home/user/OneDrive/Desktop/Desktop/My_Saved_Directory  
        4) notes: /home/user/notes_temp
        5) pbj: /home/user/OneDrive/Desktop/Documents/all_projects/scripts/python_scripts/pbj 


<sup>-*Above is a list of directories in the* 'default category'</sup>

Choose which directory to `cd` to like this: 

        $ pbj 3


<sup>-*This will cd to* `/home/user/OneDrive/Desktop/My_Saved_Directory`. btw, u can skip the list just use this command.</sup>  

You can also `cd` to a directory like this:

        $ pbj mydir

<sup>-*same result as `pbj 3`*</sub> 

To save a directory, first `cd` to desired directory and do:  

      $ pbj -s mydir

<sup>-*In place of `mydir`, insert your own mnemonic* **`pbj`** will not overwrite when using **`-s`** option.</sup>

Get the list of bookmarks from other categories like this:

        pbj mycategory


You can view many more examples in the help manual by installing pbj, and typing:  
`pbj -h tldr`  or  
`pbj -h examples` or
`pbj -h all` or
`pbj -h synopsis` or
`pbj -h options` or
`pbj -h standards`, and you'll find more if you do:
`pbj -h help`

--- 

## Help:

**`pbj`** has a complete manual which can be executed with:

        $ pbj -h all

synopsis of **`pbj -h`**:

        pbj -h|--help [all|synopsis|description|options|files|standards|examples|tldr|help|author|license] 
### Troubleshooting Installation:
If after setting up symlinks in `~/.local/share`, `~/.local/bin` or `/usr/bin`, the application does not work, or does not change the directory in your terminal, It could be either that the `source` call is missing from `~/.bashrc`, or the pbj directory has been moved from its original location. 

navigate to your home directory:

        $ cd ~

Try "sourcing" pbj in the terminal:

        $ source pbj

or try sourcing with this command:

        $ source ~/path/to/pbj

Then try changing directories with pbj:

        $ pbj 1

If the symlinks were set up properly, you should find yourself in a different directory, so you're good to go. Now add the 'source' command that you used to your `~/.bashrc`.

**If `pbj` still does not run or change directories:**

* **Try** deleting the symlinks ending in `/pbj`, created in either `~/.local/share` and `~/.local/bin`, or `/usr/bin`. Careful not to delete the wrong entry. Remember, they should end with `/pbj`. **Next**, take note of the full path of the `/pbj` directory in which you cloned the pbj repository, then follow your choice of steps from [Slightly More Advanced Installation](#slightly-more-advanced-installation). 
* **consider** sticking with the [regular Installation steps](#installation). 

### Known issues:
Things being worked on:

1. **The 'default' category is being used as a *current category*:** For now, the 'default' category is filling in for 'current category'. The issue with using the 'default' category as the 'current' category is that it maintains the same state across all terminal sessions. This makes the experience confusing when swchitching panes in tmux or to another terminal window. Changing the current category in one session should not change the current category in another simultaneoulsy running session. This behavior makes sense for a default category, but pbj should have a 'current category' in place that will maintain its state on a per-session, rather than global basis.
## Author:
* Michael DSa
## License:
This project is licensed under The MIT License - see the [LICENSE.md](./LICENSE.md) file for details