import unittest
from models.amity import Amity
from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace
import os


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.office_1 = Office('PERL')
        self.office_2 = Office('OCCULUS')
        self.living_space_1 = LivingSpace('DOJO')
        self.living_space_2 = LivingSpace('NODE')
        self.staff_1 = Staff("BOB", "WACHIRA")
        self.staff_2 = Staff("BOB", "ODHIAMBO")
        self.fellow_1 = Fellow("LAWRENCE", "WACHIRA", "N")
        self.fellow_2 = Fellow("LAWRENCE", "NYAMBURA", "Y")
        self.staff_1.employee_id, self.staff_1.office_allocated = 1, "PERL"
        self.office_1.current_occupancy = 1
        self.staff_2.employee_id = 2
        self.fellow_1.employee_id = 3
        self.fellow_2.employee_id, self.fellow_2.office_allocated = 4, \
                                                                    "OCCULUS"
        self.office_2.current_occupancy = 1
        self.fellow_2.living_space_allocated = "DOJO"
        self.living_space_1.current_occupancy = 1
        Amity.rooms = [self.office_1, self.office_2, self.living_space_1,
                       self.living_space_2]
        Amity.offices = [self.office_1, self.office_2]
        Amity.living_spaces = [self.living_space_2, self.living_space_1]
        Amity.persons = [self.staff_1, self.staff_2, self.fellow_1,
                         self.fellow_2]
        Amity.staff = [self.staff_2, self.staff_1]
        Amity.fellows = [self.fellow_2, self.fellow_1]
        self.initial_room_count = len(Amity.rooms)
        self.initial_office_count = len(Amity.offices)
        self.initial_living_space_count = len(Amity.living_spaces)
        self.initial_persons_count = len(Amity.persons)
        self.initial_staff_count = len(Amity.staff)
        self.initial_fellow_count = len(Amity.fellows)
        with open('sample.txt', "w+") as people:
            sample_list = ["OLUWAFEMI SULE FELLOW Y\n",
                           "DOMINIC WALTERS STAFF\n",
                           "SIMON PATTERSON FELLOW Y\n",
                           "MARI LAWRENCE FELLOW Y\n",
                           "LEIGH RILEY STAFF\n", "TANA LOPEZ FELLOW Y\n",
                           "KELLY McGUIRE STAFF"]
            for person in sample_list:
                people.write(person)

        with open('.id.txt', "w+") as person_id:
            person_id.write("4")

    def test_create_room(self):
        self.amity.create_room('php', 'office')
        self.amity.create_room('go', 'o')
        self.amity.create_room('scala', 'l')
        self.amity.create_room('shell', 'livingspace')
        self.assertEqual(len(Amity.rooms), self.initial_room_count + 4)
        self.assertEqual(len(Amity.offices), self.initial_office_count + 2)
        self.assertEqual(len(Amity.living_spaces),
                         self.initial_living_space_count + 2)
        self.assertIn('GO', [room.name for room in Amity.offices])

    def test_add_staff(self):
        self.amity.add_staff('Lawrence', 'Otieno')
        self.amity.add_staff('Lawrence', 'Muchiri')
        self.amity.add_staff('Lawrence', 'Kilonzo')
        self.amity.add_staff('Lawrence', 'Mutiga')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.staff), self.initial_staff_count + 4)
        self.assertIn('ROBERT OPIYO has been allocated the office',
                      self.amity.add_staff('Robert', 'Opiyo'))

    def test_add_fellow(self):
        self.amity.add_fellow('Mercy', 'Wachira', 'Y')
        self.amity.add_fellow('Mercy', 'Muchiri')
        self.amity.add_fellow('Mercy', 'Nyambura', 'y')
        self.amity.add_fellow('Mercy', 'Mutiga')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.fellows), self.initial_fellow_count + 4)

    def test_load_people(self):
        message = "People added from file successfully"
        self.assertEqual(message, self.amity.load_people('sample.txt'))
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 7)
        self.assertEqual(len(Amity.fellows), self.initial_fellow_count + 4)
        self.assertEqual(len(Amity.staff), self.initial_staff_count + 3)
        self.assertEqual('Non-existent file', self.amity.load_people(
            'people.txt'))
        self.assertEqual("Invalid file", self.amity.load_people('people.mp3'))

    def test_reallocate_person(self):
        message = "Employee ID does not exist"
        self.assertEqual(self.amity.reallocate_person(100, "go"), message)
        message = "New Room has not been created"
        self.assertEqual(self.amity.reallocate_person(1, "go"), message)

    def test_print_allocations(self):
        self.assertEqual(self.amity.print_allocations(), 'Finished')
        message = 'Allocations printed and saved to file successfully'
        self.assertEqual(self.amity.print_allocations('allocated'), message)

    def test_print_unallocated(self):
        self.assertEqual(self.amity.print_unallocated(), "Finished")
        message = 'Write to file complete'
        self.assertEqual(self.amity.print_unallocated('unallocated.txt'),
                         message)
        self.staff_2.office_allocated = "OCCULUS"
        self.fellow_1.office_allocated = "OCCULUS"
        self.office_2.current_occupancy = 3
        self.assertEqual(self.amity.print_unallocated('unallocated.txt'),
                         'Did not output to file. All allocated')
        self.assertEqual(self.amity.print_unallocated(), 'All allocated')
        os.remove("unallocated.txt")

    def test_print_room(self):

        self.assertEqual(self.amity.print_room("go"), "Didn't print")
        self.assertEqual(self.amity.print_room("perl"), "Room printed "
                                                        "successfully")

    def test_save_state(self):
        pass

    def test_load_state(self):
        pass

    def tearDown(self):
        os.remove('sample.txt')
        os.remove(".id.txt")


if __name__ == '__main__':
    unittest.main()
