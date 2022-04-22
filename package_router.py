import wgups_hash_table
import wgups_package
import map_graph
import delivery_location
import csv
import datetime
import hub
import truck
import node
import linked_list


class PackageRouter:
    packages = wgups_hash_table.hashTable(30, 5)
    hubs = []
    trucks = []
    map = map_graph.MapGraph()
    current_hub = hub.Hub(-1, "None", "None", "None", "None", "None")

    def __init__(self):
        self.location_id = 1
        for i in range(4):
            self.trucks.append(truck.Truck(i))

    def import_packages(self):
        # Read in the package file to parse package data
        with open('WGUPSPackageFile.csv', mode='r') as package_file:
            reader = csv.reader(package_file)

            i = -1

            print("Importing package data from " + package_file.name)

            for row in reader:

                i = i + 1
                if i < 8:
                    continue

                id = int(row[0])
                address = row[1]
                city = row[2]
                state = row[3]
                zip_code = row[4]
                time = row[5]
                weight_string = row[6]
                weight = int(weight_string)
                instructions = row[7]

                # Algorithm to turn the time string into values for a datetime object
                is_hour = 1
                is_pm = 0
                hour_string = ''
                minute_string = ''

                for char in time:
                    if char == 'E':
                        hour_string = '17'
                        minute_string = '00'
                        break

                    if char == ':':
                        is_hour = 0
                        continue

                    if is_hour == 1 and len(hour_string) < 3:
                        hour_string = hour_string + char
                    elif is_hour == 0 and len(minute_string) < 3:
                        minute_string = minute_string + char
                    elif char == 'P':
                        is_pm = 1

                hour = int(hour_string)
                if is_pm == 1:
                    hour = hour + 12

                minute = int(minute_string)
                time_now = datetime.datetime.now()
                deadline = datetime.datetime(time_now.year, time_now.month, time_now.day, hour, minute, 0, 0)

                status = 1

                self.packages.insert(id, address, deadline, city, state, zip_code, weight, status)

            print("Package data imported")

    def import_locations(self):
        with open('WGUPSDistanceTable.csv', mode='r') as location_file:
            reader = csv.reader(location_file)

            i = 0

            print("Importing location data from " + location_file.name)

            distances = []

            for row in reader:
                i = i + 1

                if i >= 9:
                    distances.append([])

                if i < 9:
                    continue
                # Separate algorithm to capture the hub data, it is formatted differently than all other lines.
                elif i == 9:

                    # Initiate the location variables to facilitate looping later
                    location_name = ''
                    location_address = ''
                    location_city = ''
                    location_state = ''
                    location_zip = ''

                    # Pull the row into a string variable
                    address_string = row[0]

                    # get all the indices of new lines in the address string as break points
                    break_chars = self.get_breaks(address_string, '\n')

                    # Loop up to the first break point to get the location name
                    j = 0
                    while j < break_chars[0]:
                        location_name = location_name + address_string[j]
                        j = j + 1

                    # Loop from the first break to the second to get the address
                    j = break_chars[0] + 1
                    while j < break_chars[1]:
                        location_address = location_address + address_string[j]
                        j = j + 1

                    # Initiate a special variable to gather the remaining data after the last break point
                    location_data = ''

                    # Loop from the last break point to the end of the string to gather the remaining location data
                    j = break_chars[1] + 1
                    while j < len(address_string):
                        location_data = location_data + address_string[j]
                        j = j + 1

                    # Get the new break point for the remaining location data using the comma as a break point
                    break_chars = self.get_breaks(location_data, ',')

                    # Loop to the break point to get the city name
                    j = 0
                    while j < break_chars[0]:
                        location_city = location_city + location_data[j]
                        j = j + 1

                    # Loop from the break point to the end
                    # If a character is an alphabet character its part of the state abbreviation
                    # If a character is a digit its part of the zip code
                    j = break_chars[0] + 1
                    while j < len(location_data):
                        if self.is_alpha(location_data[j]) == 1:
                            location_state = location_state + location_data[j]
                        elif self.is_num(location_data[j]) == 1:
                            location_zip = location_zip + location_data[j]
                        j = j + 1

                    # Create the delivery location object, the id is from the ID list
                    new_hub = hub.Hub(self.location_id, location_name, location_address, location_city, location_state,
                                      location_zip)

                    # Increment the id list to ensure unique IDs are used
                    self.location_id = self.location_id + 1

                    self.hubs.append(new_hub)

                    self.map.insert_vertex(new_hub)

                    self.current_hub = new_hub

                    distance_index = 2
                    while distance_index < 29:
                        if row[distance_index] != '':
                            distances[new_hub.get_id() - 1].append(row[distance_index])
                        distance_index = distance_index + 1

                elif i > 9:
                    # row[0] is the address with name and street address split with a new line, no zip code
                    # row[1] is the street address and zip code split with a new line, zip code is in parentheses
                    # the hub has all the address data in row[0] and row[1] is the hub designation.
                    # row[2] to the end is all distance data
                    # Location ID numbers will be an incrementing variable
                    location_name = ''
                    location_address = ''
                    location_zip = ''

                    address_string = row[0]
                    address_data = row[1]

                    # print(address_string)
                    # print(address_data)

                    # Get the indices of the break between the location name and address
                    break_chars = self.get_breaks(address_string, '\n')

                    j = 0

                    # Loop to capture the location name
                    while j < break_chars[0]:
                        location_name = location_name + address_string[j]
                        j = j + 1

                    j = break_chars[0] + 1

                    # Loop to capture the address
                    while j < len(address_string):
                        location_address = location_address + address_string[j]
                        j = j + 1

                    break_chars = self.get_breaks(address_data, '\n')

                    j = break_chars[0] + 1

                    while j < len(address_data):
                        if address_data[j] != '(' or address_data[j] != ')':
                            location_zip = location_zip + address_data[j]
                        j = j + 1

                    if self.current_hub.id != -1:
                        location = delivery_location.DeliveryLocation(self.location_id, location_name, location_address,
                                                                      location_zip, self.current_hub)
                    else:
                        raise RuntimeError("No hub has been created!")

                    self.location_id = self.location_id + 1

                    if self.current_hub.id != -1:
                        self.current_hub.add_location(location)
                    else:
                        raise RuntimeError("No hub has been created!")

                    self.map.insert_vertex(location)

                    distance_index = 2
                    while distance_index < 29:
                        if row[distance_index] != '':
                            distances[location.get_id() - 1].append(row[distance_index])
                        distance_index = distance_index + 1

            # for each k, need to append k+n[l]
            l = 0
            length = len(self.map.adj_list)
            for k in range(length):
                for l in range(k):
                    if k == l:
                        continue
                    vertex1 = self.map.adj_list[k].base_node.next_node.item
                    vertex2 = self.map.adj_list[l].base_node.next_node.item
                    # print("k = " + str(k))
                    # print("l = " + str(l))
                    self.map.insert_edge(vertex1, vertex2, distances[k][l])
                    l = l + 1
                k = k + 1

        print("Location data imported")

    def load_and_route(self):
        pass

    def get_breaks(self, string, break_char):
        """
        Provides the indices of the break characters in the provided string
        :param string: String with breaks in it
        :param break_char: Character to be used as a break point
        :return: List containing indices of the break points
        """
        i = 0

        break_points = []

        while i < len(string):
            if string[i] == break_char:
                break_points.append(i)
            i = i + 1

        return break_points

    def is_alpha(self, char):
        """
        Determines if a character is part of the alphabet
        :param char: character
        :return: 0 if it is not, 1 if it is in the alphabet
        """
        alphabet_l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                      't', 'u', 'v', 'w', 'x', 'y', 'z']
        alphabet_u = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        i = 0

        while i < len(alphabet_l):
            if char == alphabet_l[i] or char == alphabet_u[i]:
                return 1
            i = i + 1

        return 0

    def is_num(self, char):
        """
        Determines if a character is a number
        :param char: character
        :return: 0 if it is not, 1 if it is a number
        """
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        i = 0

        while i < len(numbers):
            if char == numbers[i]:
                return 1
            i = i + 1

        return 0
