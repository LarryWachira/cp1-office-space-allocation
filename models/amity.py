from os import path, mkdir
from random import choice
from time import sleep

from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace


class Amity(object):
    rooms = []
    living_spaces = []
    offices = []
    persons = []
    staff = []
    fellows = []
    files_directory_path = './files/'

    def create_room(self, name, room_type):
        if name.isalpha():
            if name.upper() in [room.name for room in self.rooms]:
                print("\n  Room {} already exists".format(name.upper()))
                return "Duplicate entry"

            elif room_type.upper() in ["OFFICE", "O"]:
                office_object = Office(name.upper())
                self.rooms.append(office_object)
                self.offices.append(office_object)
                print("\n  Office {} has been created".format(name.upper()))

            elif room_type.upper() in ["LIVINGSPACE", "L"]:
                living_space_object = LivingSpace(name.upper())
                self.rooms.append(living_space_object)
                self.living_spaces.append(living_space_object)
                print("\n  Living Space {} has been created".format(
                    name.upper())
                      )

            else:
                print("\n  Invalid room type {}. Type help for usage "
                      "instructions".format(room_type))

        else:
            print("\n  Invalid room name {}. Name should only consist of "
                  "alphabetical characters".format(name))

    def add_staff(self, first_name, second_name):
        check_result = Amity.check_duplicate_name(first_name, second_name)
        if check_result in ["Duplicate entry", "Invalid"]:
            return check_result

        staff_object = Staff(first_name.upper(), second_name.upper())
        staff_object.employee_id = Amity.generate_id()
        self.staff.append(staff_object)
        self.persons.append(staff_object)

        empty_offices = [room for room in self.offices if
                         room.free_spaces() > 0]

        if len(empty_offices) > 0:
            selected_office = choice(empty_offices)
            staff_object.office_allocated = selected_office.name
            selected_office.current_occupancy += 1
            message = "Staff {} has been allocated the office {}".format(
                      staff_object, selected_office)
            print('\n  ', message)
            return message

        else:
            message = "No empty offices available. Staff {} has not been " \
                      "allocated".format(staff_object)
            print("\n  ", message)

    def add_fellow(self, first_name, second_name, wants_accommodation='N'):
        check_result = Amity.check_duplicate_name(first_name, second_name)
        if check_result in ["Duplicate entry", "Invalid"]:
            return check_result

        fellow_object = Fellow(first_name.upper(), second_name.upper(),
                               wants_accommodation.upper())
        fellow_object.employee_id = Amity.generate_id()
        self.fellows.append(fellow_object)
        self.persons.append(fellow_object)

        empty_offices = [room for room in self.offices if
                         room.free_spaces() > 0]

        if len(empty_offices) > 0:
            selected_office = choice(empty_offices)
            fellow_object.office_allocated = selected_office.name
            selected_office.current_occupancy += 1
            message = "Fellow {} has been allocated the office {}".format(
                fellow_object, selected_office)
            print('\n  ', message)

        else:
            message = "No empty offices available. Fellow {} has not been " \
                      "allocated".format(fellow_object)
            print("\n  ", message)

        if wants_accommodation.upper() == "Y":
            empty_living_spaces = [room for room in self.living_spaces if
                                   room.free_spaces() > 0]

            if len(empty_living_spaces) > 0:
                selected_living_space = choice(empty_living_spaces)
                fellow_object.living_space_allocated = \
                    selected_living_space.name
                selected_living_space.current_occupancy += 1
                message = "Fellow {} has been allocated the living space " \
                          "{}".format(fellow_object, selected_living_space)
                print('\n  ', message)
                return message

            else:
                message = "No empty living spaces available. Fellow {} has " \
                          "not been allocated".format(fellow_object)
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

            if new_office.free_spaces() == 0:
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

            if new_office.name == old_office.name:
                print("\n  {} {} is already allocated to {}".format(
                    person_to_be_reallocated.designation,
                    person_to_be_reallocated, new_office.name))
                return "Already in office"

            old_office.current_occupancy -= 1
            new_office.current_occupancy += 1
            person_to_be_reallocated.office_allocated = new_office.name
            print("\n  Employee {} has been moved to the Office {} from {}"
                  .format(person_to_be_reallocated, new_office,
                          old_office))
            return "Employee reallocated"

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

            if new_living_space.free_spaces() == 0:
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

            if new_living_space.name == old_living_space.name:
                print("\n  {} {} is already allocated to {}".format(
                    fellow_to_be_reallocated.designation,
                    fellow_to_be_reallocated,
                    new_living_space.name))
                return "Already in living space"

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
            with open(self.files_directory_path + file_name) as people:
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

                message = "People added from file successfully"
                print('\n\n\t\t', message, "\n")
                return message

        except FileNotFoundError:
            print("\n  File '{}' does not exist in the files directory. Try a "
                  "different file name. Also ensure it's a text "
                  "file".format(file_name))

            return "Non-existent file"

    def print_allocations(self, file_name=None):
        if len(self.persons) == 0:
            message = "No Employees have been added"
            print("\n  ", message)
            return message

        if len(self.rooms) == 0:
            message = "No rooms have been created"
            print("\n  ", message)
            return message

        if len(self.offices) == 0:
            print("\n  No offices have been created.")
        else:
            for office in self.offices:
                office_occupants = [person for person in self.persons if
                                    person.office_allocated == office.name]
                if len(office_occupants) > 0:
                    print("\n  ", office, ": [OFFICE]")
                    Amity.print_allocations_list_procedure(office_occupants)

                sleep(0.2)

        if len(self.living_spaces) == 0:
            print("\n  No Living Spaces have been created.")
        else:
            for living_space in self.living_spaces:
                living_space_occupants = [fellow for fellow in self.fellows if
                                          fellow.living_space_allocated ==
                                          living_space.name]
                if len(living_space_occupants) > 0:
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

            with open(self.files_directory_path + file_name, 'w+') as file:

                if len(self.offices) > 0:
                    for office in self.offices:
                        occupants = [person for person in self.persons if
                                     person.office_allocated == office.name]

                        if len(occupants) > 0:
                            file.write(office.name + ": OFFICE\n\n")
                            for person in occupants:
                                file.write("[" + str(person.employee_id) + "] "
                                           + person.first_name + ' '
                                           + person.second_name + ' |'
                                           + person.designation + '\n')
                            file.write("\n\n")

                    file.write("\n\n")

                if len(self.living_spaces) > 0:
                    for living_space in self.living_spaces:
                        occupants = [fellow for fellow in self.fellows if
                                     fellow.living_space_allocated ==
                                     living_space.name]

                        if len(occupants) > 0:
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
        unallocated_offices = [person for person in self.persons if
                               person.office_allocated is None]

        if len(unallocated_offices) > 0:
            print('\n  Persons that have not been allocated an office:')
            Amity.print_allocations_list_procedure(unallocated_offices)
        elif len(self.persons) == 0:
            print("\n  No employees have been added")
            return "No employees"
        else:
            print("\n  All employees have been allocated offices")

        unallocated_living_spaces = [fellow for fellow in self.fellows if
                                     fellow.living_space_allocated is None
                                     and fellow.wants_accommodation == "Y"]

        if len(unallocated_living_spaces) > 0:
            print("\n  Fellows that want accommodation and have not been "
                  "allocated:")
            Amity.print_allocations_list_procedure(unallocated_living_spaces)
        elif len(self.fellows) == 0:
            print("\n  No Fellows have been added")
        else:
            print("\n  All Fellows that want accommodation have been "
                  "allocated Living Spaces")

        unallocated_persons = unallocated_offices + unallocated_living_spaces

        if file_name:
            if len(unallocated_persons) == 0:
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

                with open(self.files_directory_path + file_name, 'w+') as file:
                    if len(unallocated_offices) > 0:
                        file.write("EMPLOYEES THAT HAVE NOT BEEN ALLOCATED AN "
                                   "OFFICE: \n\n")
                        for person in unallocated_offices:
                            file.write("[" + str(person.employee_id) + "]"
                                       + ' ' + person.first_name + ' '
                                       + person.second_name + ' '
                                       + person.designation + ' '
                                       + ' \n')

                        file.write("\n\n\n")

                    if len(unallocated_living_spaces) > 0:
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

        elif len(unallocated_persons) == 0:
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
        pass

    def load_state(self, database_name=None):
        pass

    def create_files_directory(self):
        if not path.exists(self.files_directory_path):
            mkdir(self.files_directory_path)

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
        if type(int(employee_id)) != int:
            print("\n  Employee ID is not a number")
            return "Invalid ID"

        elif not new_room_name.isalpha():
            print("\n  Invalid new room name. Room name should consist of "
                  "only alphabetical characters")
            return "Invalid new room name"

        else:
            return

    @staticmethod
    def check_duplicate_name(first_name, second_name):
        if first_name.isalpha() and second_name.isalpha():
            for person in Amity.persons:
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

