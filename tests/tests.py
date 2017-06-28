from os import remove, rename
from pathlib import Path
import unittest
import sqlite3

from models.amity import Amity
from models.persons import Staff, Fellow
from models.rooms import Office, LivingSpace
from models.config import files_directory_path, databases_directory_path


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
        self.fellow_3 = Fellow("MARTIN", "MUNGAI", "Y")

        self.staff_1.employee_id, self.staff_1.office_allocated = 1, "PERL"
        self.staff_2.employee_id = 2
        self.fellow_1.employee_id = 3
        self.fellow_2.employee_id, self.fellow_2.office_allocated = 4, \
            "OCCULUS"
        self.fellow_2.living_space_allocated = "DOJO"
        self.fellow_3.employee_id = 5

        self.office_1.current_occupancy = 1
        self.office_2.current_occupancy = 1
        self.living_space_1.current_occupancy = 1

        self.amity.rooms = [self.office_1, self.office_2, self.living_space_1,
                            self.living_space_2]
        self.amity.offices = [self.office_1, self.office_2]
        self.amity.living_spaces = [self.living_space_2, self.living_space_1]
        self.amity.persons = [self.staff_1, self.staff_2, self.fellow_1,
                              self.fellow_2, self.fellow_3]
        self.amity.staff = [self.staff_2, self.staff_1]
        self.amity.fellows = [self.fellow_2, self.fellow_1, self.fellow_3]

        self.initial_room_count = len(self.amity.rooms)
        self.initial_office_count = len(self.amity.offices)
        self.initial_living_space_count = len(self.amity.living_spaces)
        self.initial_persons_count = len(self.amity.persons)
        self.initial_staff_count = len(self.amity.staff)
        self.initial_fellow_count = len(self.amity.fellows)

        self.amity.create_files_directory()
        self.amity.create_databases_directory()

        self.saved_id = None
        if Path('./models/.id.txt').is_file():
            with open('./models/.id.txt', "r") as current_id:
                self.saved_id = current_id.read()
        else:
            with open('./models/.id.txt', "w+") as person_id:
                person_id.write("5")

    def test_create_room(self):
        self.amity.create_room('php', 'office')
        self.amity.create_room('go', 'o')
        self.amity.create_room('scala', 'l')
        self.amity.create_room('shell', 'livingspace')
        self.assertEqual(len(self.amity.rooms), self.initial_room_count + 4)
        self.assertEqual(len(self.amity.offices),
                         self.initial_office_count + 2)
        self.assertEqual(len(self.amity.living_spaces),
                         self.initial_living_space_count + 2)
        self.assertEqual(self.amity.create_room('shell', 'livingspace'),
                         "Duplicate entry")
        self.assertEqual(self.amity.create_room('hello', 'livispace'),
                         "Invalid room type")
        self.assertEqual(self.amity.create_room('ag@in', 'livingspace'),
                         "Invalid room name")
        self.assertIn('GO', [room.name for room in self.amity.offices])

    def test_add_staff(self):
        self.amity.add_staff('Lawrence', 'Otieno')
        self.amity.add_staff('Lawrence', 'Muchiri')
        self.amity.add_staff('Lawrence', 'Kilonzo')
        self.amity.add_staff('Lawrence', 'Mutiga')
        self.assertEqual(len(self.amity.persons),
                         self.initial_persons_count + 4)
        self.assertEqual(len(self.amity.staff), self.initial_staff_count + 4)
        self.assertEqual(self.amity.add_staff('Lawrence', 'Muchiri'),
                         "Duplicate entry")
        self.assertIn('ROBERT OPIYO has been allocated the office',
                      self.amity.add_staff('Robert', 'Opiyo'))
        self.amity.offices = []
        self.assertEqual(self.amity.add_staff('Lawrence', 'Ndegwa'),
                         "No empty offices available. Staff LAWRENCE NDEGWA "
                         "has been added but has not been allocated an office")

    def test_add_fellow(self):
        self.amity.add_fellow('Mercy', 'Wachira', 'Y')
        self.amity.add_fellow('Mercy', 'Muchiri')
        self.amity.add_fellow('Mercy', 'Nyambura', 'y')
        self.amity.add_fellow('Mercy', 'Mutiga')
        self.assertEqual(self.amity.add_fellow('Mercy', 'Muchiri'),
                         "Duplicate entry")
        self.assertEqual(self.amity.add_fellow('M0rcy', 'Muchiri'),
                         "Invalid")
        self.assertEqual(len(self.amity.persons),
                         self.initial_persons_count + 4)
        self.assertEqual(len(self.amity.fellows),
                         self.initial_fellow_count + 4)
        self.assertIn("Fellow MERCY KIBOI has been allocated the living "
                      "space", self.amity.add_fellow('Mercy', 'Kiboi', 'y'))
        self.amity.living_spaces = []
        self.assertEqual(self.amity.add_fellow('Lawrence', 'Ndegwa', 'y'),
                         "No empty living spaces available. Fellow LAWRENCE "
                         "NDEGWA has not been allocated a living space")

    def test_load_people(self):
        with open('./files/test_sample.txt', "w+") as people:
            sample_list = ["OLUWAFEMI SULE FELLOW Y\n",
                           "DOMINIC WALTERS STAFF\n",
                           "SIMON PATTERSON FELLOW Y\n",
                           "MARI LAWRENCE FELLOW Y\n",
                           "LEIGH RILEY STAFF\n", "TANA LOPEZ FELLOW Y\n",
                           "KELLY McGUIRE STAFF"]
            for person in sample_list:
                people.write(person)

        message = "People loaded from file successfully"
        self.assertEqual(message, self.amity.load_people('test_sample.txt'))

        self.assertEqual(len(self.amity.persons),
                         self.initial_persons_count + 7)
        self.assertEqual(len(self.amity.fellows),
                         self.initial_fellow_count + 4)
        self.assertEqual(len(self.amity.staff), self.initial_staff_count + 3)

        self.assertEqual('Non-existent file', self.amity.load_people(
            'test_load_people.txt'))
        self.assertEqual("Invalid file", self.amity.load_people('people.mp3'))

        remove(files_directory_path + 'test_sample.txt')

    def test_reallocate_person(self):
        message = "Employee ID does not exist"
        self.assertEqual(self.amity.reallocate_person('100', "go"), message)

        message = "New Room has not been created"
        self.assertEqual(self.amity.reallocate_person('1', "go"), message)
        self.assertEqual(self.amity.reallocate_person('5a', "go"), 'Invalid '
                                                                   'ID')

        self.staff_1.office_allocated = None
        self.assertEqual(self.amity.reallocate_person('1', "occulus"),
                         "Person allocated")
        self.assertEqual(self.amity.reallocate_person('1', "Perl"),
                         "Person reallocated")
        self.assertEqual(self.amity.reallocate_person('1', "Perl"),
                         "Already in office")

        self.assertEqual(self.amity.reallocate_person('3', "occulus"),
                         "Person allocated")
        self.assertEqual(self.amity.reallocate_person('3', "dojo"),
                         "Did not want accommodation")
        self.assertEqual(self.amity.reallocate_person('4', "node"),
                         "Fellow reallocated")
        self.assertEqual(self.amity.reallocate_person('5', "node"),
                         "Fellow allocated")
        self.assertEqual(self.amity.reallocate_person('5', "node"),
                         "Already in living space")

        self.living_space_1.current_occupancy = 4
        self.assertEqual(self.amity.reallocate_person('4', "dojo"),
                         "New living space full")

        self.office_2.current_occupancy = 6
        self.assertEqual(self.amity.reallocate_person('1', "occulus"),
                         "New office full")

        message = 'Cannot reallocate Staff to a living space'
        self.assertEqual(self.amity.reallocate_person('1', "dojo"), message)

    def test_print_allocations(self):
        self.assertEqual(self.amity.print_allocations(), 'Finished')

        message = 'Allocations printed and saved to file successfully'
        self.assertEqual(self.amity.print_allocations('test_allocated.txt'),
                         message)
        remove(files_directory_path + "test_allocated.txt")

        self.assertEqual(self.amity.print_allocations('test_allocated.mp3'),
                         "Invalid filename")

        self.amity.rooms = []
        self.assertEqual(self.amity.print_allocations(), "No rooms have been "
                                                         "created")

        self.amity.persons = []
        self.assertEqual(self.amity.print_allocations(), "No Employees have "
                                                         "been added")

    def test_print_unallocated(self):
        self.assertEqual(self.amity.print_unallocated(), "Finished")

        message = 'Write to file complete'
        self.assertEqual(self.amity.print_unallocated('test_unallocated.txt'),
                         message)
        remove(files_directory_path + "test_unallocated.txt")

        self.assertEqual(self.amity.print_unallocated('test_unallocated.mp3'),
                         "Invalid filename")

        self.staff_2.office_allocated = "OCCULUS"
        self.fellow_1.office_allocated = "OCCULUS"
        self.fellow_3.office_allocated = "PERL"
        self.fellow_3.living_space_allocated = "NODE"
        self.assertEqual(self.amity.print_unallocated('unallocated.txt'),
                         'Did not output to file. All allocated')
        self.assertEqual(self.amity.print_unallocated(), 'All allocated')

        self.amity.persons = []
        self.assertEqual(self.amity.print_unallocated(), 'No employees')

    def test_print_room(self):

        self.assertEqual(self.amity.print_room("go"), "Didn't print")
        self.assertEqual(self.amity.print_room("perl"), "Room printed "
                                                        "successfully")

        self.office_1.current_occupancy = 0
        self.living_space_1.current_occupancy = 0
        self.assertEqual(self.amity.print_room("perl"), "None allocated")
        self.assertEqual(self.amity.print_room("dojo"), "None allocated")

    def test_save_state(self):
        if Path(databases_directory_path + 'Amity.sqlite3').is_file():
            rename(databases_directory_path + 'Amity.sqlite3',
                   databases_directory_path + 'Amity_backup.sqlite3')

        self.assertEqual(self.amity.save_state(), "State saved to "
                                                  "Amity.sqlite3 "
                                                  "successfully")

        remove(databases_directory_path + 'Amity.sqlite3')

        if Path(databases_directory_path + 'Amity_backup.sqlite3').is_file():
            rename(databases_directory_path + 'Amity_backup.sqlite3',
                   databases_directory_path + 'Amity.sqlite3')

        self.assertEqual(self.amity.save_state("February"), "State saved to "
                                                            "February.sqlite3 "
                                                            "successfully")
        remove("./databases/February.sqlite3")

        self.amity.rooms = []
        self.amity.persons = []
        self.assertEqual(self.amity.save_state(), "No data")

    def test_load_state(self):
        if not Path(databases_directory_path + 'Amity.sqlite3').is_file():
            self.assertEqual(self.amity.load_state(), "Database does not "
                                                      "exist")
        else:
            self.assertIn(self.amity.load_state(), ["State loaded "
                                                    "from Amity.sqlite3 "
                                                    "successfully",
                                                    "No data to load"])

        self.assertEqual(self.amity.load_state("March"), "Database does not "
                                                         "exist")

        conn = sqlite3.connect(databases_directory_path +
                               'test_load_state_db.sqlite3')
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

        conn.commit()
        conn.close()

        self.assertEqual(self.amity.load_state("test_load_state_db"),
                         "No data to load")
        remove(databases_directory_path + 'test_load_state_db.sqlite3')

    def test_generate_id(self):
        self.assertIsInstance(Amity.generate_id(), int)

    def test_verify_id_and_new_room_values(self):
        self.assertEqual(Amity.verify_id_and_new_room_values('a', 'python'),
                         "Invalid ID")
        self.assertEqual(Amity.verify_id_and_new_room_values('1', 'pyth0n'),
                         "Invalid new room name")

    def tearDown(self):
        if self.saved_id:
            with open('./models/.id.txt', "w+") as restore_id:
                restore_id.write(self.saved_id)

        else:
            remove('./models/.id.txt')


if __name__ == '__main__':
    unittest.main()
