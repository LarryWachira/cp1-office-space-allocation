
# Amity:
## A room allocation system for one of Andela’s facilities

Amity is a room allocation command line application with key essential features written in Python.
You can add people, add rooms, print allocations and unallocated data and also reallocate employees. What's more, Amity also allows you to backup to a specified text file or sqlite database of your choosing.

Here's a commands list highlighting all of its current features:

## Usage:
1.  create room <room_type> <room_name> ...
2.  add person <designation> <first_name> <second_name> [-a <wants_accommodation>]
3.  reallocate person <employee_id> <new_room_name>
4.  print_allocations [-o <file_name>]
5.  print_unallocated [-o <file_name>]
6.  print room <room_name>
7.  save_state [--db <database_name>]
8.  load_state [--db <database_name>]
9.  help

Features that require arguments of one type or another are indicated in angle brackets while optional arguments
are enclosed in square brackets.

--------------------------------------------------------

## Setting up Amity
The app has a number of dependencies as detailed in the `requirements.txt`. To run it, you'll need to install [Python 3.6](http://python.org) from Python's website and setup a virtual environment as illustrated [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Dependencies that are built into Python have not been included.


### Prerequisites

The code is written in Python 3.

### Installing

Clone the repository from GitHub:

`git clone https://github.com/LarryWachira/cp1-office-space-allocation.git`

Change Directory into the project folder

`cd cp1-office-space-allocation`

Install the dependencies from requirements.txt

`pip install -r requirements.txt`

The last and final is simply to run `python app.py` on your command line to fire up the app.

--------------------------------------------------------


