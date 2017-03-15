import unittest
from models.amity import Amity
import os


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.create_room('perl', 'office')
        self.amity.create_room('oculus', 'o')
        self.amity.create_room('dojo', 'l')
        self.amity.create_room('Node', 'living space')
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

    def test_create_room(self):
        self.amity.create_room('php', 'office')
        self.amity.create_room('go', 'o')
        self.amity.create_room('scala', 'l')
        self.amity.create_room('php', 'living space')
        self.assertEqual(len(Amity.rooms), self.initial_room_count + 4)
        self.assertEqual(len(Amity.offices), self.initial_office_count + 2)
        self.assertEqual(len(Amity.living_spaces),
                         self.initial_living_space_count + 2)
        self.assertIn('GO', [room.name for room in Amity.offices])

    def test_add_staff(self):
        self.amity.add_staff('Lawrence', 'Wachira')
        self.amity.add_staff('Lawrence', 'Muchiri')
        self.amity.add_staff('Lawrence', 'Nyambura')
        self.amity.add_staff('Lawrence', 'Mutiga')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.staff), self.initial_staff_count + 4)
        self.assertIn('has been allocated the office', self.amity.add_staff(
            'Robert', 'Opiyo'))

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
        self.assertRaises(FileNotFoundError, self.amity.load_people,
                          'people.txt')

    def test_reallocate_person(self):
        pass

    def test_print_allocations(self):
        message = 'Allocations printed successfully'
        self.assertEqual(self.amity.print_allocations(), message)
        message = 'Allocations printed and saved to file successfully'
        self.assertEqual(self.amity.print_allocations('test'), message)
        self.assertEqual(self.amity.print_allocations('test.txt'), message)

    def test_print_unallocated(self):
        message = 'Unallocated printed successfully'
        self.assertEqual(self.amity.print_unallocated(), message)
        message = 'Unallocated printed and saved to file successfully'
        self.assertEqual(self.amity.print_unallocated('test'), message)
        self.assertEqual(self.amity.print_unallocated('test.txt'), message)

    def test_print_room(self):
        pass

    def test_save_state(self):
        pass

    def test_load_state(self):
        pass

    def tearDown(self):
        os.remove('sample.txt')


if __name__ == '__main__':
    unittest.main()
