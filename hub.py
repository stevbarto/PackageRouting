class Hub:
    delivery_locations = []

    def __init__(self, id, name, address, city, state, zip_code):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def add_location(self, delivery_location):
        self.delivery_locations.append(delivery_location)

    def get_location(self, location_id):
        for i in range(len(self.delivery_locations)):
            if location_id == self.delivery_locations[i].id:
                return self.delivery_locations[i]

    def remove_location(self, location_id):
        for i in range(len(self.delivery_locations)):
            if location_id == self.delivery_locations[i].id:
                self.delivery_locations.remove(self.delivery_locations[i])

    def get_id(self):
        return self.id
