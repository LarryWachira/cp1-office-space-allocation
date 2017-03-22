"""
Usage:
    app.py create room <room_type> <room_name> ...
    app.py add person <first_name> <second_name> <designation> [wants_accommodation]
    app.py reallocate person <employee_id> <new_room_name>
    app.py print_allocations [-o=allocations.txt]
    app.py print_unallocated [-o=unallocated.txt]
    app.py print room <room_name>
    app.py save_state [--db=sqlite_database]
    app.py load_state <sqlite_database>
    app.py help
    app.py (-i | --interactive)
    app.py (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    type exit to close the app
"""

import cmd
import sys

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

            print('\nInvalid Command! Also, check the number of arguments '
                  'that can be passed in \'Usage:\' below.')
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
    intro = '\n\t\t\t\tWelcome to Amity!\n\t    -Type help for a list of ' \
            'instructions on how to use the app-'
    prompt = '\nAmity >> '
    amity = Amity()

    @docopt_cmd
    def do_create(self, args):
        """Usage: create room <room_type> <room_name>..."""
        room_type = args['<room_type>']
        room_list = args['<room_name>']
        print(room_type)
        for name in room_list:
            self.amity.create_room(name, room_type)

    @docopt_cmd
    def do_add(self, args):
        """Usage: add person <first_name> <second_name> <designation>
        [wants_accommodation]"""
        designation = args['<designation>']
        first_name = args['<first_name>']
        second_name = args['<second_name>']
        wants_accommodation = args['wants_accommodation']

        if designation.upper() in ["FELLOW", "F"]:
            if wants_accommodation:
                self.amity.add_fellow(first_name, second_name, "Y")
            else:
                self.amity.add_fellow(first_name, second_name)

        elif designation.upper() in ["STAFF", "S"]:
            self.amity.add_staff(first_name, second_name)

        else:
            print("\nInvalid Employee designation. Designation should be "
                  "either 'Staff' or 'Fellow'")

    @docopt_cmd
    def do_reallocate(self, args):
        """Usage: reallocate person <employee_id> <new_room_name>"""
        employee_id = args['<employee_id>']
        new_room_name = args['<new_room_name>']

        self.amity.reallocate_person(employee_id, new_room_name)

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [--filename=people]"""
        self.amity.load_people()

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [-o=allocations.txt]"""
        self.amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_allocations [-o=allocations.txt]"""
        self.amity.print_unallocated()

    @docopt_cmd
    def do_print(self, arg):
        """Usage: print room <room_name>"""
        room_name = arg['<room_name>']

        if room_name.isalpha():
            self.amity.print_room(room_name)

        else:
            print("\nInvalid room name. Room name should consist of "
                  "alphabetical characters only")

    @docopt_cmd
    def do_save(self, arg):
        """Usage: save state [--db=sqlite_database]"""
        pass

    @docopt_cmd
    def do_load(self, arg):
        """Usage: load state <sqlite_database>"""
        pass

    @docopt_cmd
    def do_help(self, arg):
        """Usage: help"""
        print('''
      \t\t\t\t   Commands:
      \t   create room <room_type> <room_name> ...
      \t   add person <first_name> <second_name> <designation> [wants_accommodation]
      \t   reallocate person <employee_id> <new_room_name>
      \t   print_allocations [-o=allocations.txt]
      \t   print_unallocated [-o=unallocated.txt]
      \t   print room <room_name>
      \t   save_state [--db=sqlite_database]
      \t   load_state <sqlite_database>
      \t   help
      \t-Words enclosed in angle brackets '< >' should guide you on the required number
      \t of arguments, except when they appear like this: '< >...' when any number
      \t of arguments is allowed.
      \t-Square brackets '[]' denote optional arguments.
      \t-Separate different arguments with a space.
                           ||Type exit to close the app||''')

    def do_exit(self, arg):
        """Usage: exit"""
        pass
        print('\n' + '*' * 50 + '\n')
        print('\tThank you for using Amity!\n')
        print('*'*50)
        f = Figlet(font='slant')
        print(f.renderText('Good Bye!'))
        exit()


opt = docopt(__doc__, sys.argv[1:])


if opt['--interactive']:
    try:
        print('\n'*3)
        f = Figlet(font='block')
        print(f.renderText('Amity'))
        print('*' * 60)
        print(__doc__)
        AmityApp().cmdloop()
    except KeyboardInterrupt:
        print("\n\tExiting App")
