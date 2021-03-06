

class DeliveryLocation:

    package_ids = []

    def __init__(self, id, name, address, zip_code, hub):
        self.id = id
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.hub = hub

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def add_package(self, package_id):
        self.package_ids.append(package_id)
