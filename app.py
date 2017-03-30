"""
Usage:
    app.py create_room <room_type> <room_name> ...
    app.py add_person <designation> <first_name> <second_name> \
[-a <wants_accommodation>]
    app.py reallocate_person <employee_id> <new_room_name>
    app.py print_allocations [-o <file_name>]
    app.py print_unallocated [-o <file_name>]
    app.py print_room <room_name>
    app.py load_people <file_name>
    app.py save_state [--db <database_name>]
    app.py load_state [--db <database_name>]
    app.py help
    app.py (-i | --interactive)
    app.py (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help         Show this screen and exit.
    -v, --version      Show app version
    type exit to close the app
"""

import cmd
import sys
from time import sleep

from termcolor import cprint, colored
from colorama import init

from docopt import docopt, DocoptExit
from pyfiglet import Figlet

from models.amity import Amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.

            print('\nInvalid Command! \nCheck the command format and number '
                  'of arguments that can be passed in \'Usage:\' below\n')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityApp(cmd.Cmd):
    intro = colored('\n\t\t\t\tWelcome to Amity!\n\t    -Type help for a '
                    'list of instructions on how to use the app-', 'green')
    prompt = colored('\n\nAmity >> ', 'magenta')
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>..."""
        room_type = args['<room_type>']
        room_list = args['<room_name>']

        for name in room_list:
            self.amity.create_room(name, room_type)
            sleep(0.2)

    @docopt_cmd
    def do_add_person(self, args):
        """
        Usage: add_person <designation> <first_name> <second_name> \
[-a <wants_accommodation>]

Options:
    -a <wants_accommodation>  Whether person wants accommodation [default: N]
        """
        designation = args['<designation>']
        first_name = args['<first_name>']
        second_name = args['<second_name>']
        wants_accommodation = args['-a']

        if wants_accommodation.upper() not in ["Y", "N"]:
            print("\n<wants_accommodation> should either be 'Y' or 'N' and is "
                  "not an option for STAFF persons")

        elif designation.upper() in ["FELLOW", "F"]:
            if wants_accommodation.upper() == 'Y':
                self.amity.add_fellow(first_name, second_name, "Y")
            else:
                self.amity.add_fellow(first_name, second_name)

        elif designation.upper() in ["STAFF", "S"]:
            if wants_accommodation != 'N':
                print("\n  STAFF persons cannot be allocated living spaces")

            else:
                self.amity.add_staff(first_name, second_name)

        else:
            print("\n  Invalid Employee designation. Designation should be "
                  "either 'Staff' or 'Fellow'")

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <employee_id> <new_room_name>"""

        employee_id = args['<employee_id>']
        new_room_name = args['<new_room_name>']

        self.amity.reallocate_person(employee_id, new_room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""

        self.amity.load_people(arg["<file_name>"])

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
    Usage: print_allocations [-f <file_name>]

Options:
    -f <file_name>  Output to file
        """
        if arg['-f']:
            self.amity.print_allocations(arg['-f'])

        else:
            self.amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """
        Usage: print_unallocated [-f <file_name>]

Options:
    -f <unallocated.txt>  Output to file
        """
        if arg['-f']:
            self.amity.print_unallocated(arg['-f'])

        else:
            self.amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

        room_name = arg['<room_name>']

        if room_name.isalpha():
            self.amity.print_room(room_name)

        else:
            print("\n  Invalid room name. Room name should consist of "
                  "alphabetical characters only")

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db <database_name>]

Options:
    --db <database_name>  Save to specified database(default is set to 'Amity')
        """
        if arg['--db']:
            self.amity.save_state(arg['--db'])

        else:
            self.amity.save_state()

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [--db <sqlite_database>]

Options:
    --db <database_name>  Load from specified database(default is set to
    'Amity')
        """
        if arg['--db']:
            self.amity.load_state(arg['--db'])

        else:
            self.amity.load_state()

    @docopt_cmd
    def do_help(self, arg):
        """Usage: help"""

        print('''
\t\t\t\t   Commands:
   create room <room_type> <room_name> ...
   add person <first_name> <second_name> <designation> [wants_accommodation]
   reallocate person <employee_id> <new_room_name>
   print_allocations [-o=allocations.txt]
   print_unallocated [-o=unallocated.txt]
   print room <room_name>
   load_people <file_name>
   save_state [--db=sqlite_database]
   load_state <sqlite_database>
   help
-Words enclosed in angle brackets '< >' should guide you on the required
 number of arguments, except when they appear like this: '< >...' when any
 number of arguments is allowed.
-Square brackets '[]' denote optional arguments.
-Separate different arguments with a space.
\n\t\t\t  ||Type exit to close the app||
                   ''')

    @docopt_cmd
    def do_exit(self, arg):
        """Usage: exit"""
        print('\n\n' + '*' * 60 + '\n')
        cprint('\t\tThank you for using Amity!\n', 'green')
        print('*' * 60)
        style = Figlet(font='pebbles')
        cprint(style.renderText('Good Bye!'), 'magenta')
        exit()


opt = docopt(__doc__, sys.argv[1:] + ['-i'], version=1.0)

if opt['--interactive']:
    try:
        init()
        print('\n')
        style = Figlet(font='dotmatrix')
        cprint(style.renderText('Amity'), 'magenta')
        print('*' * 65)
        cprint(__doc__, 'yellow')
        AmityApp().cmdloop()
    except KeyboardInterrupt:
        print("\n\tExiting App")
