

class Room(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def free_spaces(self):
        free_spaces = self.max_capacity - self.current_occupancy
        return free_spaces


class Office(Room):
    room_type = 'OFFICE'
    max_capacity = 6

    def __init__(self, name):
        super(Office, self).__init__(name)
        self.current_occupancy = 0


class LivingSpace(Room):
    room_type = 'LIVING SPACE'
    max_capacity = 4

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.current_occupancy = 0
