[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fb2cfdf3e2f44a9d9f3cd33f6a9f3118)](https://www.codacy.com/app/LarryWachira/cp1-office-space-allocation?utm_source=github.com&utm_medium=referral&utm_content=LarryWachira/cp1-office-space-allocation&utm_campaign=badger)
[![Build Status](https://travis-ci.org/LarryWachira/cp1-office-space-allocation.svg?branch=master)](https://travis-ci.org/LarryWachira/cp1-office-space-allocation)
[![Coverage Status](https://coveralls.io/repos/github/LarryWachira/cp1-office-space-allocation/badge.svg?branch=master)](https://coveralls.io/github/LarryWachira/cp1-office-space-allocation?branch=master)
# Amity:
## A room allocation system for one of Andela’s facilities

Amity is a room allocation command line application with key essential features written in Python.
You can add people, add rooms, print allocations and unallocated data and also reallocate employees. What's more, Amity also allows you to backup to a specified text file or sqlite database of your choosing.

Here's a commands list highlighting all of its current features:

## Usage:
1.  create_room <room_type> <room_name> ...
2.  add_person <designation> <first_name> <second_name> [-a <wants_accommodation>]
3.  reallocate_person <employee_id> <new_room_name>
4.  print_allocations [-o <file_name>]
5.  print_unallocated [-o <file_name>]
6.  print_room <room_name>
7.  load_people <file_name>
8.  save_state [--db <database_name>]
9.  load_state [--db <database_name>]
10.  help

Features that require arguments of one type or another are indicated in angle brackets while optional arguments
are enclosed in square brackets.

--------------------------------------------------------

## Setting up Amity
The app has a number of dependencies as detailed in the `requirements.txt`. To run it, you'll need to install [Python 3.6](http://python.org) from Python's website and setup a virtual environment as illustrated [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Dependencies that are built into Python have not been included.



### Installing

Clone the repository from GitHub:

`git clone https://github.com/LarryWachira/cp1-office-space-allocation.git`

Change Directory into the project folder

`cd cp1-office-space-allocation`

Install the dependencies from requirements.txt

`pip install -r requirements.txt`

The last and final is simply to run `python app.py` on your command line to fire up the app.

--------------------------------------------------------


To run tests, just run the following command on the terminal:

`nosetests --with-coverage -v --cover-package=models
`