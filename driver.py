import truck


class Driver:
    truck = -1

    def __init__(self, id):
        self.id = id

    def set_truck(self, delivery_truck):
        self.truck = delivery_truck
