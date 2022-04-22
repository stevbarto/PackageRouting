class Truck:

    status_list = {'HUB', 'ENROUTE', 'AT STOP'}
    status = 0
    packages = []
    weight = 0
    stops = []
    current_stop = 0

    def __init__(self, id):
        self.id = id

    def load_package(self, package):
        self.packages.append(package)
        self.weight = self.weight + package.get_weight()

    def deliver_package(self):
        deliver_me = self.packages.pop(0)
        self.weight = self.weight - deliver_me.get_weight()

    def set_status(self, status):
        if 1 <= status <= 3:
            self.status = status
        else:
            raise RuntimeError("Invalid selection, enter status between 1 and 3!")
