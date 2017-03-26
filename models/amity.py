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

    def create_room(self, name, room_type):
        if name.isalpha():
            if name.upper() in [room.name for room in self.rooms]:
                print("\nRoom {} already exists".format(name.upper()))
                return "Duplicate entry"

            elif room_type.upper() in ["OFFICE", "O"]:
                office_object = Office(name.upper())
                self.rooms.append(office_object)
                self.offices.append(office_object)
                print("\nOffice {} has been created".format(name.upper()))

            elif room_type.upper() in ["LIVINGSPACE", "L"]:
                living_space_object = LivingSpace(name.upper())
                self.rooms.append(living_space_object)
                self.living_spaces.append(living_space_object)
                print("\nLiving Space {} has been created".format(name.upper())
                      )

            else:
                print("\nInvalid room type {}. Type help for usage "
                      "instructions".format(room_type))

        else:
            print("\nInvalid room name {}. Name should only consist of "
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
            print('\t\n', message)
            return message

        else:
            message = "No empty offices available. Staff {} has not been " \
                      "allocated".format(staff_object)
            print("\t\n", message)

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
            print('\t\n', message)

        else:
            message = "No empty offices available. Fellow {} has not been " \
                      "allocated".format(fellow_object)
            print("\t\n", message)

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
                print('\t\n', message)
                return message

            else:
                message = "No empty living spaces available. Fellow {} has " \
                          "not been allocated".format(fellow_object)
                print("\t\n", message)
                return message

    def reallocate_person(self, employee_id, new_room_name):
        verify_result = Amity.verify_id_and_new_room_values(employee_id,
                                                            new_room_name)
        if verify_result in ["Invalid ID", "Invalid new room name"]:
            return verify_result

        if employee_id not in [person.employee_id for person in self.persons]:
            message = "Employee ID does not exist"
            print("\n", message)
            return message

        if new_room_name.upper() not in [room.name for room in self.rooms]:
            message = "New Room has not been created"
            print("\n", message)
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

            for room in self.offices:
                if person_to_be_reallocated.office_allocated == room.name:
                    old_office = room
                    break

            old_office.current_occupancy -= 1
            new_office.current_occupancy += 1
            person_to_be_reallocated.office_allocated = new_office.name
            print("\nEmployee {} has been moved to the Office {} from {}"
                  .format(person_to_be_reallocated, new_office,
                          old_office))
            return "Employee reallocated"

        if new_room_name.upper() in [room.name for room in self.living_spaces]:
            for fellow in self.fellows:
                if fellow.employee_id == employee_id:
                    fellow_to_be_reallocated = fellow
                    break

            for room in self.living_spaces:
                if room.name == new_room_name.upper():
                    new_living_space = room
                    break

            for room in self.living_spaces:
                if fellow_to_be_reallocated.living_space_allocated == \
                        room.name:
                    old_living_space = room
                    break

            old_living_space.current_occupancy -= 1
            new_living_space.current_occupancy += 1
            fellow_to_be_reallocated.living_space_allocated = \
                new_living_space.name
            print("\nFellow {} has been moved the Living Space {} from "
                  "{}".format(fellow_to_be_reallocated, new_living_space,
                              old_living_space))
            return "Fellow reallocated"

    def load_people(self, file_name):
        if not file_name.endswith('.txt'):
            print("Invalid file format. Amity accepts only text files with "
                  "the '.txt' extension")
            return "Invalid file"

        try:
            with open(file_name) as people:
                content = people.readlines()

                for line in content:
                    person_details = line.split()

                    if person_details[2].upper() == 'STAFF':
                        self.add_staff(person_details[0], person_details[1])
                        sleep(0.5)

                    elif person_details[2].upper() == 'FELLOW':
                        try:
                            self.add_fellow(person_details[0],
                                            person_details[1],
                                            person_details[3])
                            sleep(0.5)

                        except IndexError:
                            self.add_fellow(person_details[0],
                                            person_details[1])
                            sleep(0.5)

                message = "People added from file successfully"
                print('\n\n\t\t', message, "\n")
                return message

        except FileNotFoundError:
            print("\n  File '{}' does not exist. Try a different file "
                  "name. Also ensure it's a text file".format(file_name))

            return "Non-existent file"

    def print_allocations(self, file_name=None):
        if len(self.persons) == 0:
            message = "No Employees have been added"
            print("\n", message)
            return message

        if len(self.offices) == 0:
            print("\nNo offices have been created.")
        else:
            for office in self.offices:
                occupants = [person for person in self.persons if
                             person.office_allocated == office.name]
                if len(occupants) > 0:
                    print("\n", office, ": [OFFICE]")
                    Amity.print_allocations_list_procedure(occupants)

                sleep(0.5)
                # if to_file:
                #     Amity.write_to_file()

        if len(self.living_spaces) == 0:
            print("\nNo Living Spaces have been created.")
        else:
            for living_space in self.living_spaces:
                occupants = [fellow for fellow in self.fellows if
                             fellow.living_space_allocated ==
                             living_space.name]
                if len(occupants) > 0:
                    print("\n", living_space, ": [LIVING SPACE]")
                    Amity.print_allocations_list_procedure(occupants)

                sleep(0.5)
                # if to_file:
                #     Amity.write_to_file()

        if file_name:
            return 'Allocations printed and saved to file successfully'
        else:
            return 'Finished'

    def print_unallocated(self, file_name=None):
        unallocated_offices = [person for person in self.persons if
                               person.office_allocated is None]

        if len(unallocated_offices) > 0:
            print('\nPersons that have not been allocated an office:')
            Amity.print_allocations_list_procedure(unallocated_offices)
        elif len(self.persons) == 0:
            print("\nNo employees have been added")
            return "No employees"
        else:
            print("\nAll employees have been allocated offices")

        unallocated_living_spaces = [fellow for fellow in self.fellows if
                                     fellow.living_space_allocated is None
                                     and fellow.wants_accommodation == "Y"]

        if len(unallocated_living_spaces) > 0:
            print("\nFellows that want accommodation and have not been "
                  "allocated:")
            Amity.print_allocations_list_procedure(unallocated_living_spaces)
        elif len(self.fellows) == 0:
            print("\nNo Fellows have been added")
        else:
            print("\nAll Fellows that want accommodation have been allocated "
                  "Living Spaces")

        unallocated_persons = unallocated_offices + unallocated_living_spaces

        if file_name:
            if not file_name.endswith('.txt'):
                print("Invalid file name. Amity write only to text files. "
                      "Choose a different name that ends with the '.txt' "
                      "extension")
                return "Invalid filename"

            elif len(unallocated_persons) == 0:
                print("\nDid not output to file. All employees have been "
                      "allocated rooms.")
                return "Did not output to file. All allocated"

            else:
                with open(file_name, 'w+') as file:
                    for person in unallocated_persons:
                        if person.designation == "FELLOW":
                            file.write("[" + str(person.employee_id) + "]"
                                       + ' ' + person.first_name + ' '
                                       + person.second_name + ' '
                                       + person.designation + ' '
                                       + person.wants_accommodation + ' \n')

                        if person.designation == "STAFF":
                            file.write("[" + str(person.employee_id) + "]"
                                       + ' ' + person.first_name + ' '
                                       + person.second_name + '  '
                                       + person.designation + ' \n')

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
            print('\nThe room {} has not been created'.format(
                room_name.upper()))
            return "Didn't print"

        elif room_name.upper() in [office.name for office in self.offices]:
            if room_object.free_spaces() == 6:
                print("\nNo one has been allocated {}".format(
                    room_object.name))
                return "None allocated"
            people_list = [person for person in self.persons if
                           person.office_allocated == room_name.upper()]
            print('\n\n', room_name.upper(), ': OFFICE')
            Amity.print_allocations_list_procedure(people_list)

        else:
            if room_object.free_spaces() == 4:
                print("\nNo one has been allocated {}".format(
                    room_object.name))
                return "None allocated"
            people_list = [fellow for fellow in self.fellows if
                           fellow.living_space_allocated == room_name.upper()]
            print('\n\n', room_name.upper(), ': LIVING SPACE')
            Amity.print_allocations_list_procedure(people_list)

        return "Room printed successfully"

    def save_state(self):
        pass

    def load_state(self):
        pass

    @staticmethod
    def generate_id():
        with open(".id.txt", "a+") as unique_id:
            unique_id.seek(0)
            person_id = unique_id.read()

            if not person_id:
                person_id = 1
            else:
                person_id = int(person_id)
                person_id += 1

        with open(".id.txt", "w+") as unique_id:
            unique_id.write(str(person_id))

            return person_id

    @staticmethod
    def print_allocations_list_procedure(people_list):
        print("----------------------------------------------------------\n")
        if len(people_list) > 1:
            for person in people_list[:-1]:
                print("[", person.employee_id, "]", person, end=',  ')

            print("[", people_list[-1].employee_id, "]", people_list[-1])
            print("\n")
        elif len(people_list) == 1:
            print("[", people_list[0].employee_id, "]", people_list[0])
            print("\n")

    @staticmethod
    def verify_id_and_new_room_values(employee_id, new_room_name):
        if type(employee_id) != int:
            print("\nEmployee ID is not a number")
            return "Invalid ID"

        elif not new_room_name.isalpha():
            print("\nInvalid new room name. Room name should consist of only "
                  "alphabetical characters")
            return "Invalid new room name"

        else:
            return

    @staticmethod
    def check_duplicate_name(first_name, second_name):
        if first_name.isalpha() and second_name.isalpha():
            for person in Amity.persons:
                if person.first_name == first_name.upper() and \
                                person.second_name == second_name.upper():
                    print("\nThe person {} {} already exists.".format(
                        first_name, second_name))
                    return "Duplicate entry"
            return

        else:
            print("\nInvalid person name. Both the first name and second name "
                  "should consist of alphabetical characters.")
            return "Invalid"
