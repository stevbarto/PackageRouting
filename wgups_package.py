from datetime import datetime
import re


class package:
    """
    Class representation of a package object.  Parameters requiring int values or string values which
    represent digits will return a runtime error if imroper values or tupes are presented.  These are
    specifically the id, deadline, zip_code, weight, and status values.

    Attributes
    ----------
    id : int
        Unique package identification number.
    address : str
        Address where the package will be delivered.
    deadline : date
        Date time group of the deadline for delivery of the package.
    city : str
        The name of the city where the package should be delivered.
    zip_code : str
        The zip code for package delivery.  Consists of digits only, but is a string object.
    weight : int
        Integer weight of the package in kilograms.
    status : int
        Integer value of the package status.  1 = AT HUB, 2 = IN TRANSIT, 3 = OUT FOR DELIVERY, 3 = DELIVERED.

    Methods
    -------

    """

    truck_id = "No truck"

    address = "No Address"

    connected_packages = []

    hold_hour = -1
    hold_min = -1

    city = 'Salt Lake City'

    status_hour = 8
    status_min = 0

    waitlist = 0

    wait_hour = -1

    wait_min = -1

    STATUS_LIST = ["AT HUB", "ENROUTE", "DELIVERED"]

    def __init__(self, id, address, deadline, city, zip_code, weight, status):
        if isinstance(id, int):
            self.id = id
        else:
            raise RuntimeError("Parameter id must be an integer value.")

        if isinstance(address, str):
            self.address = address
        else:
            raise RuntimeError("Parameter address must be a str object.")

        if isinstance(deadline, datetime):
            self.deadline = deadline
        else:
            raise RuntimeError("Parameter deadline must be a datetime object.")

        if isinstance(city, str):
            self.city = city
        else:
            raise RuntimeError("Parameter city must be a str object.")

        if isinstance(zip_code, str) and len(zip_code) == 5 and self.only_digits(zip_code) == 1:
            self.zip_code = zip_code
        else:
            raise RuntimeError("Parameter zip_code must be a str object of length 5 and only digits.")

        if isinstance(weight, int):
            self.weight = weight
        else:
            raise RuntimeError("Parameter weight must be an int value.")

        if isinstance(status, int):
            self.status = status
        else:
            raise RuntimeError("Parameter status must be an int value.")

        self.instructions = ""

    def __getitem__(self):
        return self

    def get_id(self):
        return self.id

    def get_address(self):
        """
        Method to return the address destination for the pakage
        :return: String value address
        """
        return self.address

    def get_deadline(self):
        return self.deadline

    def get_city(self):
        return self.city

    def set_city(self, city):
        self.city = city

    def get_zip_code(self):
        return self.zip_code

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code

    def get_weight(self):
        return self.weight

    def get_status(self):
        tod_string = " AM"
        hour_string = self.status_hour
        if self.status_hour > 12:
            hour_string = self.status_hour - 12
            tod_string = " PM"

        if self.status_min < 10:
            min_string = "0" + str(self.status_min)
        else:
            min_string = str(self.status_min)



        status_string = self.STATUS_LIST[self.status - 1] + " at " + str(hour_string) + ":" \
                        + min_string + tod_string

        return status_string

    def set_address(self, address):
        self.address = address

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_status(self, status, hour, min):
        self.status = status
        self.status_hour = hour
        self.status_min = min

    def set_instructions(self, instructions):
        self.instructions = instructions

    def get_instructions(self):
        return self.instructions

    def only_digits(self, string):
        only_digs = 1

        letters = "abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        characters = "!@#$%^&*()_+{}[]|\\:;\"\'<,>.?/ \n\r\t\b\f"

        for i in range(len(string)):
            if string[i] in letters or string[i] in characters:
                only_digs = 0

        return only_digs

    def set_truck(self, truck_id):
        self.truck_id = truck_id

    def get_truck(self):
        return self.truck_id

    def connect_package(self, package):
        already_there = 0
        for i in range(len(self.connected_packages)):
            if package.get_id == self.connected_packages[i].get_id():
                already_there = 1
        if already_there == 0:
            self.connected_packages.append(package)

    def set_hold(self, hour, mintue):
        self.waitlist = 1
        self.wait_hour = hour
        self.wait_min = mintue

    def get_hold(self):
        return [self.wait_hour, self.wait_min]



