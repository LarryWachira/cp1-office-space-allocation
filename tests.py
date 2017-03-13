import unittest
from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace
from models.amity import Amity


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        Amity.rooms = []
        Amity.living_spaces = []
        Amity.offices

    def test_create_room(self):
        self.amity.create_room('php', 'office')
        self.assertEqual(len(Amity.rooms), 1)
        self.assertEqual(len(Amity.offices), 1)
        php = Office('php', 'office')
        self.assertEqual(php.max_capacity, 6)

    def test_add_person(self):
        self.amity.add_person('Lawrence', 'Wachira', 'Fellow')
        self.assertEqual(len(Amity.persons), 1)
        self.assertEqual(len(Amity.fellows), 1)
        dojo = LivingSpace('dojo', 'living space')
        oculus = Office('Oculus', 'Office')
        self.amity.add_person('Robert', 'Opiyo', 'Fellow', 'Y')
        self.assertIn(person_obj, dojo.persons_allocated)
        self.assertIn(person_obj, oculus.persons_allocated)
        self.assertRaises(ValueError, self.amity.add_person(),
                          'Lawrence', 'Wachira', '24')

    def test_load_people(self):
        self.amity.load_people('people.txt')
        self.assertEqual(len(Amity.persons), 7)
        self.assertEqual(len(Amity.fellows), 4)
        self.assertEqual(len(Amity.staff), 3)

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
