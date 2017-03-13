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
        if room_type in ["office", "Office"]:
            office_object = Office(name)
            self.rooms.append(office_object)
            self.offices.append(office_object)
        elif room_type in ["living space", "Living space", "living Space"]:
            living_space_object = LivingSpace(name)
            self.rooms.append(living_space_object)
            self.living_spaces.append(living_space_object)

    def check_duplicate_name(self):
        pass

    def add_person(self, first_name, second_name, designation,
                   wants_accommodation='N'):
        if designation.lower() == 'staff':
            staff_object = Staff(first_name.lower(), second_name.lower())
            Amity.staff.append(staff_object)
            Amity.persons.append(staff_object)
            empty_rooms = [room for room in Amity.offices if
                           room.free_spaces > 0]
            selected_office = choice(empty_rooms)
            staff_object.office_allocated = selected_office
            selected_office.current_occupancy += 1

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


# val = Rooms('Valhalla', 'Office')
# print(val.room_type)
# print(Room.rooms)
# Amity().create_room()
# print(len(Amity.rooms))
