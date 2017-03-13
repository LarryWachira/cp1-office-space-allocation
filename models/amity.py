from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace
from random import choice


class Amity(object):
    rooms = []
    living_spaces = []
    offices = []
    persons = []
    staff = []
    fellows = []

    def create_room(self, name, room_type):
        if room_type in ["office", "o"]:
            office_object = Office(name.upper())
            self.rooms.append(office_object)
            self.offices.append(office_object)
        elif room_type in ["living space", "l"]:
            living_space_object = LivingSpace(name.upper())
            self.rooms.append(living_space_object)
            self.living_spaces.append(living_space_object)

    def check_duplicate_name(self):
        pass

    def add_staff(self, first_name, second_name):
        staff_object = Staff(first_name.upper(), second_name.upper())
        self.staff.append(staff_object)
        self.persons.append(staff_object)
        empty_offices = [room for room in self.offices if
                         room.free_spaces > 0]
        selected_office = choice(empty_offices)
        staff_object.office_allocated = selected_office
        selected_office.current_occupancy += 1
        message = "{} has been allocated to {} office".format(staff_object,
                                                              selected_office)
        print(message)
        return message

    def add_fellow(self, first_name, second_name, wants_accommodation='N'):
        fellow_object = Staff(first_name.upper(), second_name.upper())
        self.fellows.append(fellow_object)
        self.persons.append(fellow_object)
        empty_offices = [room for room in self.offices if
                         room.free_spaces > 0]
        selected_office = choice(empty_offices)
        fellow_object.office_allocated = selected_office
        selected_office.current_occupancy += 1

        if wants_accommodation in ["y", "Y"]:
            empty_living_spaces = [room for room in self.living_spaces if
                                   room.free_spaces > 0]
            selected_living_space = choice(empty_living_spaces)
            fellow_object.living_space_allocated = selected_living_space
            selected_living_space.current_occupancy += 1

    def reallocate_person(self):
        pass

    def load_people(self, file_name):
        pass

    def print_allocations(self, o='allocations.txt'):
        pass

    def print_unallocated(self):
        pass

    def print_room(self):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass

# Amity().create_room('Krypton', 'o')
# Amity().create_room('Kal-el', 'o')
# # Amity().add_staff('Lawrence', 'Wachira')
# Amity().add_staff('Lawrence', 'Wachira')
# Amity().add_staff('Lawrence', 'Muchiri')
# Amity().add_staff('Lawrence', 'Nyambura')
# Amity().add_staff('Lawrence', 'Mutiga')
# val = Rooms('Valhalla', 'Office')
# print(val.room_type)
# print(Room.rooms)
# Amity().create_room()
# print(len(Amity.rooms))
