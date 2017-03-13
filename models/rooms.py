

class Room(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Office(Room):
    room_type = 'Office'
    max_capacity = 6

    def __init__(self, name):
        super().__init__(name)
        self.current_occupancy = 0
        self.free_spaces = self.max_capacity - self.current_occupancy
        self.allocated


class LivingSpace(Room):
    room_type = 'Living Space'
    max_capacity = 4

    def __init__(self, name):
        super().__init__(name)
        self.current_occupancy = 0
        self.free_spaces = self.max_capacity - self.current_occupancy
