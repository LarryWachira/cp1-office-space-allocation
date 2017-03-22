

class Person(object):

    def __init__(self, first_name, second_name):
        self.first_name = first_name
        self.second_name = second_name

    def __str__(self):
        return self.first_name + " " + self.second_name

    def __repr__(self):
        return self.first_name + " " + self.second_name


class Staff(Person):
    designation = "Staff"

    def __init__(self, first_name, second_name):
        super(Staff, self).__init__(first_name, second_name)
        self.office_allocated = None
        self.employee_id = 0


class Fellow(Person):
    designation = "Fellow"

    def __init__(self, first_name, second_name, wants_accommodation):
        super(Fellow, self).__init__(first_name, second_name)
        self.wants_accommodation = wants_accommodation
        self.office_allocated = None
        self.living_space_allocated = None
        self.employee_id = 0

    # @staticmethod
    # def printe():
    #     print("Yo!")


# mwas = Fellow('Dennis', 'Mwangi', 'N')
# print(mwas.designation)
# print(mwas.wants_accommodation)
# print(mwas.first_name)
# print(mwas)
# print(mwas.id)
# # mwas.printe()
# Fellow.printe()

# shem = Staff("Shem", "Ogumbe")
# print(shem.first_name)
# print(shem.second_name)
# print(shem.designation)

# print(shem.__dict__)
# print(mwas.__dict__)
