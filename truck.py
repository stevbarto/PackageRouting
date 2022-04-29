import driver
import hub
import wgups_hash_table


class Truck:

    AVG_SPEED = 18
    MAX_LOAD = 16

    def __init__(self, id, hub):
        self.last_stop = -1
        self.next_stop = -1
        self.id = id
        self.delivery_queue = []
        self.route_queue = []
        self.dist_queue = []
        self.driver = -1
        self.weight = 0
        self.load = 0
        self.route_distance = 0.0
        self.stop_hour = 0
        self.stop_min = 0
        self.at_hub = 1
        self.hub = hub

        self.last_stop = hub
        self.next_stop = hub

    def load_package(self, package, hour, min):
        present = 0
        for i in range(len(self.delivery_queue)):
            if self.delivery_queue[i].get_id() == package.get_id():
                present = 1

        if present == 0:
            if len(self.delivery_queue) <= self.MAX_LOAD:
                self.delivery_queue.append(package)
                package.set_truck(self.id)
                package.set_status(2, hour, min)
                self.load = self.load + 1
                self.weight = self.weight + package.get_weight()

    def deliver_packages(self, hour, min):
        location_address = self.route_queue[0].get_address()
        j = 0
        size = len(self.delivery_queue)
        while j < size:
            package_address = self.delivery_queue.pop(0)
            if package_address.get_address() == location_address:
                package_address.set_status(2, hour, min)
                self.load = self.load - 1
                size = len(self.delivery_queue)
            else:
                self.delivery_queue.append(package_address)
            j = j + 1

    def search_package(self, id):

        package = None

        for i in range(len(self.delivery_queue)):
            if self.delivery_queue[i].get_id() == id:
                package = self.delivery_queue[i]

        return package

    def set_driver(self, driver):
        self.driver = driver

    def get_delivery_queue(self):
        return self.delivery_queue

    def get_load(self):
        return self.load

    def add_stop(self, location):
        self.route_queue.append(location)

    def complete_stop(self, hour, min):
        self.stop_hour = hour
        self.stop_min = min
        #if len(self.dist_queue) > 0:
        #    self.dist_queue.pop(0)
        if len(self.route_queue) > 0:
            self.last_stop = self.route_queue.pop(0)
        if len(self.route_queue) > 0:
            self.next_stop = self.route_queue[0]

    def set_next_stop(self, stop):
        self.next_stop = stop

    def get_next_leg(self):
        leg = [self.last_stop, self.next_stop]
        return leg

    def toggle_at_hub(self):
        if self.at_hub == 1:
            self.at_hub = 0
        else:
            self.at_hub = 1

