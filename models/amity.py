from os import path, mkdir, remove
from random import choice
from time import sleep
import sqlite3

from termcolor import colored

from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace
from models.config import files_directory_path, databases_directory_path


class Amity(object):

    def __init__(self):
        self.rooms = []
        self.living_spaces = []
        self.offices = []
        self.persons = []
        self.staff = []
        self.fellows = []

    def create_room(self, name, room_type):
        if name.isalpha():
            if name.upper() in [room.name for room in self.rooms]:
                print("\n  Room {} already exists".format(name.upper()))
                return "Duplicate entry"

            elif room_type.upper() in ["OFFICE", "O"]:
                office_object = Office(name.upper())
                self.offices.append(office_object)
                self.rooms.append(office_object)
                print("\n  Office {} has been created".format(name.upper()))

            elif room_type.upper() in ["LIVINGSPACE", "L"]:
                living_space_object = LivingSpace(name.upper())
                self.living_spaces.append(living_space_object)
                self.rooms.append(living_space_object)
                print("\n  Living Space {} has been created".format(
                    name.upper())
                )

            else:
                print("\n  Invalid room type {}. Type help for usage "
                      "instructions".format(room_type))
                return "Invalid room type"

        else:
            print("\n  Invalid room name {}. Name should only consist of "
                  "alphabetical characters".format(name))
            return "Invalid room name"

    def add_staff(self, first_name, second_name):
        check_result = self.check_duplicate_name(first_name, second_name)
        if check_result in ["Duplicate entry", "Invalid"]:
            return check_result

        staff_object = Staff(first_name.upper(), second_name.upper())
        staff_object.employee_id = Amity.generate_id()
        self.staff.append(staff_object)
        self.persons.append(staff_object)

        available_offices = [room for room in self.offices if
                             room.free_spaces()]

        if available_offices:
            selected_office = choice(available_offices)
            staff_object.office_allocated = selected_office.name
            selected_office.current_occupancy += 1
            message = "Staff {} has been allocated the office {}".format(
                      staff_object, selected_office)
            print('\n  ', message)
            return message

        else:
            message = "No empty offices available. Staff {} has been " \
                      "added but has not been allocated an office".format(
                          staff_object)
            print("\n  ", message)
            return message

    def add_fellow(self, first_name, second_name, wants_accommodation='N'):
        check_result = self.check_duplicate_name(first_name, second_name)
        if check_result in ["Duplicate entry", "Invalid"]:
            return check_result

        fellow_object = Fellow(first_name.upper(), second_name.upper(),
                               wants_accommodation.upper())
        fellow_object.employee_id = Amity.generate_id()
        self.fellows.append(fellow_object)
        self.persons.append(fellow_object)

        available_offices = [room for room in self.offices if
                             room.free_spaces()]

        if available_offices:
            selected_office = choice(available_offices)
            fellow_object.office_allocated = selected_office.name
            selected_office.current_occupancy += 1
            message = "Fellow {} has been allocated the office {}".format(
                fellow_object, selected_office)
            print('\n  ', message)

        else:
            message = "No empty offices available. Fellow {} has been " \
                      "added but has not been allocated an office".format(
                          fellow_object)
            print("\n  ", message)

        if wants_accommodation.upper() == "Y":
            available_living_spaces = [room for room in self.living_spaces if
                                       room.free_spaces()]

            if available_living_spaces:
                selected_living_space = choice(available_living_spaces)
                fellow_object.living_space_allocated = \
                    selected_living_space.name
                selected_living_space.current_occupancy += 1
                message = "Fellow {} has been allocated the living space " \
                          "{}".format(fellow_object, selected_living_space)
                print('\n  ', message)
                return message

            else:
                message = "No empty living spaces available. Fellow {} has " \
                          "not been allocated a living space".format(
                              fellow_object)
                print("\n  ", message)
                return message

    def reallocate_person(self, employee_id, new_room_name):
        verify_result = Amity.verify_id_and_new_room_values(employee_id,
                                                            new_room_name)
        if verify_result in ["Invalid ID", "Invalid new room name"]:
            return verify_result

        employee_id = int(employee_id)

        if employee_id not in [person.employee_id for person in self.persons]:
            message = "Employee ID does not exist"
            print("\n  ", message)
            return message

        if new_room_name.upper() not in [room.name for room in self.rooms]:
            message = "New Room has not been created"
            print("\n  ", message)
            return message

        if employee_id in [staff.employee_id for staff in self.staff] and \
                new_room_name.upper() in [room.name for room in
                                          self.living_spaces]:
            message = "Cannot reallocate Staff to a living space"
            print("\n  ", message)
            return message

        if new_room_name.upper() in [room.name for room in self.offices]:
            for person in self.persons:
                if person.employee_id == employee_id:
                    person_to_be_reallocated = person
                    break

            for room in self.offices:
                if room.name == new_room_name.upper():
                    new_office = room
                    break

            if new_office.name == person_to_be_reallocated.office_allocated:
                print("\n  {} {} is already allocated to {}".format(
                    person_to_be_reallocated.designation,
                    person_to_be_reallocated, new_office.name))
                return "Already in office"

            if not new_office.free_spaces():
                print("\n  Cannot reallocate {}. New office {} is full "
                      "to capacity".format(person_to_be_reallocated,
                                           new_office.name))
                return "New office full"

            if not person_to_be_reallocated.office_allocated:
                new_office.current_occupancy += 1
                person_to_be_reallocated.office_allocated = new_office.name
                print("\n  Employee {} did not have an office but has now "
                      "been allocated to {}".format(
                          person_to_be_reallocated, new_office))
                return "Person allocated"

            for room in self.offices:
                if person_to_be_reallocated.office_allocated == room.name:
                    old_office = room
                    break

            old_office.current_occupancy -= 1
            new_office.current_occupancy += 1
            person_to_be_reallocated.office_allocated = new_office.name
            print("\n  Employee {} has been moved to the Office {} from {}"
                  .format(person_to_be_reallocated, new_office,
                          old_office))
            return "Person reallocated"

        if new_room_name.upper() in [room.name for room in self.living_spaces]:
            for fellow in self.fellows:
                if fellow.employee_id == employee_id:
                    fellow_to_be_reallocated = fellow
                    break

            if fellow_to_be_reallocated.wants_accommodation == "N":
                print("\n  The fellow does not want accommodation")
                return "Did not want accommodation"

            for room in self.living_spaces:
                if room.name == new_room_name.upper():
                    new_living_space = room
                    break

            if new_living_space.name == \
                    fellow_to_be_reallocated.living_space_allocated:
                print("\n  {} {} is already allocated to {}".format(
                    fellow_to_be_reallocated.designation,
                    fellow_to_be_reallocated,
                    new_living_space.name))
                return "Already in living space"

            if not new_living_space.free_spaces():
                print("\n  Cannot reallocate {}. New living space {} is "
                      "full to capacity".format(fellow_to_be_reallocated,
                                                new_living_space.name))
                return "New living space full"

            if not fellow_to_be_reallocated.living_space_allocated:
                new_living_space.current_occupancy += 1
                fellow_to_be_reallocated.living_space_allocated = \
                    new_living_space.name
                print("\n  Fellow {} did not have an living space but has now "
                      "been allocated to {}".format(
                          fellow_to_be_reallocated, new_living_space))
                return "Fellow allocated"

            for room in self.living_spaces:
                if fellow_to_be_reallocated.living_space_allocated == \
                        room.name:
                    old_living_space = room
                    break

            old_living_space.current_occupancy -= 1
            new_living_space.current_occupancy += 1
            fellow_to_be_reallocated.living_space_allocated = \
                new_living_space.name
            print("\n  Fellow {} has been moved the Living Space {} from "
                  "{}".format(fellow_to_be_reallocated, new_living_space,
                              old_living_space))
            return "Fellow reallocated"

    def load_people(self, file_name):

        if not file_name.endswith('.txt'):
            print("\n  Invalid file format. Amity accepts only text files "
                  "with the '.txt' extension")
            return "Invalid file"

        self.create_files_directory()

        try:
            with open(files_directory_path + file_name) as people:
                content = people.readlines()

                for line in content:
                    person_details = line.split()

                    if person_details[2].upper() == 'STAFF':
                        self.add_staff(person_details[0], person_details[1])
                        sleep(0.2)

                    elif person_details[2].upper() == 'FELLOW':
                        try:
                            self.add_fellow(person_details[0],
                                            person_details[1],
                                            person_details[3])
                            sleep(0.2)

                        except IndexError:
                            self.add_fellow(person_details[0],
                                            person_details[1])
                            sleep(0.2)

                message = "People loaded from file successfully"
                print('\n\n\t\t\t', message)
                return message

        except FileNotFoundError:
            print("\n  File '{}' does not exist in the files directory. Try a "
                  "different file name. Also ensure it's a text "
                  "file".format(file_name))

            return "Non-existent file"

    def print_allocations(self, file_name=None):
        if not self.persons:
            message = "No Employees have been added"
            print("\n  ", message)
            return message

        if not self.rooms:
            message = "No rooms have been created"
            print("\n  ", message)
            return message

        if not self.offices:
            print("\n  No offices have been created.")
        else:
            for office in self.offices:
                office_occupants = [person for person in self.persons if
                                    person.office_allocated == office.name]
                if office_occupants:
                    print("\n  ", office, ": [OFFICE]")
                    Amity.print_allocations_list_procedure(office_occupants)

                sleep(0.2)

        if not self.living_spaces:
            print("\n  No Living Spaces have been created.")
        else:
            for living_space in self.living_spaces:
                living_space_occupants = [fellow for fellow in self.fellows if
                                          fellow.living_space_allocated ==
                                          living_space.name]
                if living_space_occupants:
                    print("\n  ", living_space, ": [LIVING SPACE]")
                    Amity.print_allocations_list_procedure(
                        living_space_occupants)

                sleep(0.2)

        if file_name:
            if not file_name.endswith('.txt'):
                print("\n\n  Invalid file name '{}'. Amity saves only to text "
                      "files. Choose a different name that ends with the "
                      "'.txt' extension".format(file_name))
                return "Invalid filename"

            self.create_files_directory()

            with open(files_directory_path + file_name, 'w+') as file:

                if self.offices:
                    for office in self.offices:
                        occupants = [person for person in self.persons if
                                     person.office_allocated == office.name]

                        if occupants:
                            file.write(office.name + ": OFFICE\n\n")
                            for person in occupants:
                                file.write("[" + str(person.employee_id) + "] "
                                           + person.first_name + ' '
                                           + person.second_name + ' |'
                                           + person.designation + '\n')
                            file.write("\n\n")

                    file.write("\n\n")

                if self.living_spaces:
                    for living_space in self.living_spaces:
                        occupants = [fellow for fellow in self.fellows if
                                     fellow.living_space_allocated ==
                                     living_space.name]

                        if occupants:
                            file.write(living_space.name + ": LIVING "
                                                           "SPACE\n\n")
                            for fellow in occupants:
                                file.write("[" + str(fellow.employee_id) + "] "
                                           + fellow.first_name + ' '
                                           + fellow.second_name + ' |'
                                           + fellow.designation + '\n')
                            file.write("\n\n")

            print("\n\n  Allocated persons saved to '{}' "
                  "successfully. Find it in the 'files' folder".format(
                      file_name))
            return 'Allocations printed and saved to file successfully'

        else:
            return 'Finished'

    def print_unallocated(self, file_name=None):
        if not self.persons:
            print("\n  No employees have been added")
            return "No employees"

        unallocated_offices = [person for person in self.persons if
                               person.office_allocated is None]

        if unallocated_offices:
            print('\n  Persons that have not been allocated an office:')
            Amity.print_allocations_list_procedure(unallocated_offices)
        else:
            print("\n  All employees have been allocated offices")

        unallocated_living_spaces = [fellow for fellow in self.fellows if
                                     fellow.living_space_allocated is None
                                     and fellow.wants_accommodation == "Y"]

        if unallocated_living_spaces:
            print("\n  Fellows that want accommodation and have not been "
                  "allocated:")
            Amity.print_allocations_list_procedure(unallocated_living_spaces)
        elif not self.fellows:
            print("\n  No Fellows have been added")
        else:
            print("\n  All Fellows that want accommodation have been "
                  "allocated Living Spaces")

        unallocated_persons = unallocated_offices + unallocated_living_spaces

        if file_name:
            if not unallocated_persons:
                print("\n\n  Did not output to file. All employees have been "
                      "allocated rooms.")
                return "Did not output to file. All allocated"

            elif not file_name.endswith('.txt'):
                print("\n\n  Invalid file name '{}'. Amity saves only to text "
                      "files. Choose a different name that ends with the "
                      "'.txt' extension".format(file_name))
                return "Invalid filename"

            else:
                self.create_files_directory()

                with open(files_directory_path + file_name, 'w+') as file:
                    if unallocated_offices:
                        file.write("EMPLOYEES THAT HAVE NOT BEEN ALLOCATED AN "
                                   "OFFICE: \n\n")
                        for person in unallocated_offices:
                            file.write("[" + str(person.employee_id) + "]"
                                       + ' ' + person.first_name + ' '
                                       + person.second_name + ' '
                                       + person.designation + ' '
                                       + ' \n')

                        file.write("\n\n\n")

                    if unallocated_living_spaces:
                        file.write("FELLOWS THAT HAVE NOT BEEN ALLOCATED A "
                                   "LIVING SPACE: \n\n")
                        for person in unallocated_living_spaces:
                            file.write(
                                "[" + str(person.employee_id) + "]" + ' '
                                + person.first_name + ' '
                                + person.second_name + ' '
                                + person.designation + ' '
                                + person.wants_accommodation
                                + ' \n')

                print("\n\n  Unallocated persons saved to '{}' "
                      "successfully Find it the the 'files' folder".format(
                          file_name))
                return 'Write to file complete'

        elif not unallocated_persons:
            return "All allocated"

        else:
            return 'Finished'

    def print_room(self, room_name):
        for room in self.rooms:
            if room.name == room_name.upper():
                room_object = room

        if room_name.upper() not in [room.name for room in self.rooms]:
            print('\n  The room {} has not been created'.format(
                room_name.upper()))
            return "Didn't print"

        elif room_name.upper() in [office.name for office in self.offices]:
            if room_object.free_spaces() == 6:
                print("\n  No one has been allocated to {}".format(
                    room_object.name))
                return "None allocated"
            people_list = [person for person in self.persons if
                           person.office_allocated == room_name.upper()]
            print('\n\n', room_name.upper(), ': OFFICE')
            Amity.print_allocations_list_procedure(people_list)

        else:
            if room_object.free_spaces() == 4:
                print("\n  No one has been allocated to {}".format(
                    room_object.name))
                return "None allocated"
            people_list = [fellow for fellow in self.fellows if
                           fellow.living_space_allocated == room_name.upper()]
            print('\n\n  ', room_name.upper(), ': LIVING SPACE')
            Amity.print_allocations_list_procedure(people_list)

        return "Room printed successfully"

    def save_state(self, database_name=None):
        if not self.persons and not self.rooms:
            print("\n  Cannot save state. No rooms or persons have been "
                  "added.")
            return "No data"

        self.create_databases_directory()
        if not database_name:
            database_name = 'Amity.sqlite3'
        else:
            database_name += '.sqlite3'

        if not path.isfile(databases_directory_path + database_name):
            self.save_to_database_tables(database_name)

        else:
            remove(databases_directory_path + database_name)
            self.save_to_database_tables(database_name)

        print("\n  The current Amity state has been saved to '{}'".format(
            database_name))

        return "State saved to {} successfully".format(database_name)

    def load_state(self, database_name=None):

        self.create_databases_directory()
        if not database_name:
            database_name = 'Amity.sqlite3'
        else:
            database_name += '.sqlite3'

        if not path.isfile(databases_directory_path + database_name):
            print("\n  Database '{}' does not exist. Try a different "
                  "name".format(database_name))
            return "Database does not exist"

        conn = sqlite3.connect(databases_directory_path + database_name)
        cur = conn.cursor()

        cur.execute('''SELECT * FROM Amity_employees''')
        amity_employees = cur.fetchall()

        cur.execute('''SELECT * FROM Amity_rooms''')
        amity_rooms = cur.fetchall()

        conn.close()

        error = colored("\n  ERROR:", 'red')

        if amity_employees:
            for row in amity_employees:
                if row[4] == "STAFF":
                    if row[1] not in [person.employee_id for person in
                                      self.persons]:
                        staff_object = Staff(row[2], row[3])
                        staff_object.employee_id = row[1]
                        staff_object.office_allocated = row[5]
                        self.staff.append(staff_object)
                        self.persons.append(staff_object)
                        print("\n  Staff {} has been loaded "
                              "successfully".format(staff_object))
                        sleep(0.2)

                    else:
                        print("\n  {} Could not load staff {} successfully. "
                              "They already exist in the current session. "
                              "Always load state first before adding rooms "
                              "or persons".format(error, row[2] + ' '
                                                  + row[3]))

                elif row[4] == "FELLOW":
                    if row[1] not in [person.employee_id for person in
                                      self.persons]:
                        fellow_object = Fellow(row[2], row[3], row[6])
                        fellow_object.employee_id = row[1]
                        fellow_object.office_allocated = row[5]
                        fellow_object.living_space_allocated = row[7]
                        self.fellows.append(fellow_object)
                        self.persons.append(fellow_object)
                        print("\n  Fellow {} has been loaded "
                              "successfully".format(fellow_object))
                        sleep(0.2)

                    else:
                        print("\n  {} Could not load fellow {} successfully. "
                              "They already exist in the current session. "
                              "Always load state first before adding rooms "
                              "or persons".format(error, row[2] + ' '
                                                  + row[3]))

        if amity_rooms:
            for row in amity_rooms:
                if row[2] == "OFFICE":
                    if row[1] not in [room.name for room in self.rooms]:
                        office_object = Office(row[1])
                        office_object.current_occupancy = row[3]
                        self.offices.append(office_object)
                        self.rooms.append(office_object)
                        print("\n  Office {} has been loaded "
                              "successfully".format(office_object))
                        sleep(0.2)

                    else:
                        colored_message = colored(
                            " Could not load office {} successfully. It "
                            "already exists in the current session. It's "
                            "always better to load state first before adding "
                            "rooms or persons".format(row[1]), 'yellow'
                        )
                        print(error + colored_message)

                elif row[2] == "LIVING SPACE":
                    if row[1] not in [room.name for room in self.rooms]:
                        living_space_object = LivingSpace(row[1])
                        living_space_object.current_occupancy = row[3]
                        self.living_spaces.append(living_space_object)
                        self.rooms.append(living_space_object)
                        print("\n  Living Space {} has been loaded "
                              "successfully".format(living_space_object))
                        sleep(0.2)

                    else:
                        colored_message = colored(
                            " Could not load living space {} successfully. It "
                            "already exists in the current session. It's "
                            "always better to load state first before adding "
                            "rooms or persons".format(row[1]), 'yellow'
                        )
                        print(error + colored_message)

        if not amity_rooms and not amity_employees:
            print("\n  No data to load from {}".format(database_name))
            return "No data to load"

        print("\n\n  [All non-duplicate data from '{}' has been loaded "
              "successfully]".format(database_name))

        return "State loaded from {} successfully".format(database_name)

    def check_duplicate_name(self, first_name, second_name):
        if first_name.isalpha() and second_name.isalpha():
            for person in self.persons:
                if person.first_name == first_name.upper() and \
                        person.second_name == second_name.upper():
                    print("\n  The person {} {} already exists.".format(
                        first_name.upper(), second_name.upper()))
                    return "Duplicate entry"
            return

        else:
            print("\n  Invalid person name. Both the first name and second "
                  "name should consist of alphabetical characters.")
            return "Invalid"

    def save_to_database_tables(self, database_name):
        conn = sqlite3.connect(databases_directory_path + database_name)
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Amity_employees
                                (ID INTEGER PRIMARY KEY NOT NULL ,
                                Employee_ID INTEGER NOT NULL UNIQUE,
                                First_name TEXT NOT NULL,
                                Second_name TEXT NOT NULL,
                                Designation TEXT NOT NULL,
                                Office_allocated TEXT,
                                Wants_accommodation TEXT,
                                Living_space_allocated TEXT)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS Amity_rooms
                                        (Id INTEGER PRIMARY KEY,
                                        Room_name TEXT NOT NULL UNIQUE,
                                        Room_type TEXT NOT NULL,
                                        Current_occupancy INTEGER NOT NULL)''')

        if self.rooms:
            for room in self.rooms:
                cur.execute('''INSERT INTO Amity_rooms(Room_name, Room_type,
                            Current_occupancy) VALUES(?, ?, ?)''',
                            (room.name, room.room_type,
                             room.current_occupancy))

        if self.fellows:
            for fellow in self.fellows:
                cur.execute('''INSERT INTO Amity_employees(Employee_ID,
                            First_name, Second_name, Designation,
                            Office_allocated, Wants_accommodation,
                            Living_space_allocated)
                            VALUES(?, ?, ?, ?, ?, ?, ?)''',
                            (fellow.employee_id, fellow.first_name,
                             fellow.second_name, fellow.designation,
                             fellow.office_allocated,
                             fellow.wants_accommodation,
                             fellow.living_space_allocated))

        if self.staff:
            for staff in self.staff:
                cur.execute('''INSERT INTO Amity_employees(Employee_ID,
                            First_name, Second_name, Designation,
                            Office_allocated)
                            VALUES(?, ?, ?, ?, ?)''',
                            (staff.employee_id, staff.first_name,
                             staff.second_name, staff.designation,
                             staff.office_allocated))

        conn.commit()
        conn.close()

    @staticmethod
    def create_files_directory():
        if not path.exists(files_directory_path):
            mkdir(files_directory_path)

    @staticmethod
    def create_databases_directory():
        if not path.exists(databases_directory_path):
            mkdir(databases_directory_path)

    @staticmethod
    def generate_id():
        with open("./models/.id.txt", "a+") as unique_id:
            unique_id.seek(0)
            person_id = unique_id.read()

            if not person_id:
                person_id = 1
            else:
                person_id = int(person_id)
                person_id += 1

        with open("./models/.id.txt", "w+") as unique_id:
            unique_id.write(str(person_id))

            return person_id

    @staticmethod
    def print_allocations_list_procedure(people_list):
        print("  ----------------------------------------------------------\n")
        if len(people_list) > 1:
            for person in people_list[:-1]:
                print("  [", person.employee_id, "]", '|' + person.designation
                      + '|', person, end=',  ')

            print("  [", people_list[-1].employee_id, "]", '|' + people_list[
                -1].designation + '|', people_list[-1])
            print("\n")
        elif len(people_list) == 1:
            print("  [", people_list[0].employee_id, "]", '|' + people_list[
                0].designation + '|', people_list[0])
            print("\n")

    @staticmethod
    def verify_id_and_new_room_values(employee_id, new_room_name):
        try:
            int(employee_id)
        except ValueError:
            print("\n  Employee ID is not a number")
            return "Invalid ID"

        else:
            if not new_room_name.isalpha():
                print("\n  Invalid new room name. Room name should consist of "
                      "only alphabetical characters")
                return "Invalid new room name"

            else:
                return
