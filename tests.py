import unittest
from models.amity import Amity


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

    def test_create_room(self):
        self.amity.create_room('php', 'office')
        self.amity.create_room('go', 'o')
        self.amity.create_room('scala', 'l')
        self.amity.create_room('php', 'living space')
        self.assertEqual(len(Amity.rooms), self.initial_room_count + 4)
        self.assertEqual(len(Amity.offices), self.initial_office_count + 2)
        self.assertEqual(len(Amity.living_spaces),
                         self.initial_living_space_count + 2)
        self.assertIn('go', [room.name for room in Amity.offices])

    def test_add_staff(self):
        self.amity.add_staff('Lawrence', 'Wachira')
        self.amity.add_staff('Lawrence', 'Muchiri')
        self.amity.add_staff('Lawrence', 'Nyambura')
        self.amity.add_staff('Lawrence', 'Mutiga')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.staff), self.initial_staff_count + 4)
        self.assertIn('allocated to', self.amity.add_staff('Robert', 'Opiyo'))

    def test_add_fellow(self):
        self.amity.add_fellow('Mercy', 'Wachira', 'Y')
        self.amity.add_fellow('Mercy', 'Muchiri')
        self.amity.add_fellow('Mercy', 'Nyambura', 'y')
        self.amity.add_fellow('Mercy', 'Mutiga')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.fellows), self.initial_fellow_count + 4)

    def test_load_people(self):
        self.amity.load_people('people.txt')
        self.assertEqual(len(Amity.persons), self.initial_persons_count + 7)
        self.assertEqual(len(Amity.fellows), self.initial_persons_count + 4)
        self.assertEqual(len(Amity.staff), self.initial_persons_count + 3)

    def test_reallocate_person(self):
        pass

    def test_print_allocations(self):
        # allocated_persons = [room.persons_allocated for room in Amity.rooms]
        # allocated_persons_set = set(allocated_persons)
        # persons_set = set(Amity.persons)
        # unallocated_persons = persons_set - allocated_persons_set
        pass

    def test_print_unallocated(self):
        pass

    def test_print_room(self):
        pass

    def test_save_state(self):
        pass

    def test_load_state(self):
        pass


if __name__ == '__main__':
    unittest.main()
