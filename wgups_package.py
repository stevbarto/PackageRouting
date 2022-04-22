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

    address = "No Address"

    STATUS_LIST = ["AT HUB", "IN TRANSIT", "OUT FOR DELIVERY", "DELIVERED"]

    def __init__(self, id, address, deadline, city, state, zip_code, weight, status):
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

    def get_zip_code(self):
        return self.zip_code

    def get_weight(self):
        return self.weight

    def get_status(self):
        return self.STATUS_LIST[self.status - 1]

    def set_address(self, address):
        self.address = address

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_status(self, status):
        self.status = status

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