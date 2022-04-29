import driver
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
    MAX_DISTANCE = 140
    packages = wgups_hash_table.hashTable(30, 1)
    package_load_queue = []
    packages_delivered = []
    assigned_addresses = []
    visited_stops = []
    hubs = []
    trucks = []
    drivers = []
    routes = []
    special_cases = []
    wait_list = []
    visited = []
    map = map_graph.MapGraph()
    locations = []
    current_hub = hub.Hub(-1, "None", "None", "None", "None", "None")
    min_weight = -1
    hour_string = ''
    min_string = ''

    def __init__(self):
        # self.dist_queue = []
        # self.location_queue = []
        self.location_id = 1

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

                if self.min_weight < 0:
                    self.min_weight = weight

                if weight < self.min_weight:
                    self.min_weight = weight

                new_package = wgups_package.package(id, address, deadline, city, zip_code, weight, status)

                if instructions != '':
                    new_package.set_instructions(instructions)
                    self.special_cases.append(new_package)

                self.packages.insert(new_package.get_id(), new_package)

            print("Package data imported")

    def import_locations(self):
        with open('WGUPSDistanceTable.csv', mode='r') as location_file:
            reader = csv.reader(location_file)

            i = 0

            print("Importing location data from " + location_file.name)

            for row in reader:
                i = i + 1

                # Filter the header of the csv file
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

                    new_string = ''
                    if location_address[0] == ' ':
                        n = 1
                        while n < len(location_address):
                            new_string = new_string + location_address[n]
                            n = n + 1

                        location_address = new_string

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

                    # add the hub to the list of hubs to facilitate future growth to multiple hubs
                    self.hubs.append(new_hub)

                    # inserts a new vertex list in the adjacency matrix, the index + 1 will correspond to the id number
                    self.map.insert_vertex()

                    # add the hub to the location list in an index corresponding to the adjacency matrix
                    self.locations.append(new_hub)

                    # set the current hub that will be used for package routing
                    self.current_hub = new_hub

                    self.make_trucks(new_hub)

                    # get the distance data that exists for the current row
                    self.map.insert_edge(self.locations[0], self.locations[0], 0.0)

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

                    new_string = ''
                    if location_address[0] == ' ':
                        n = 1
                        while n < len(location_address):
                            new_string = new_string + location_address[n]
                            n = n + 1

                        location_address = new_string

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

                    self.map.insert_vertex()

                    self.locations.append(location)

                    # get the distance data that exists for the current row
                    n = 2
                    while n - 2 < len(self.locations):
                        if row[n] != '':
                            j = new_hub.get_id()
                            k = n - 2
                            self.map.insert_edge(location, self.locations[k], float(row[n]))
                        n = n + 1

        for i in range(len(self.locations)):
            self.assigned_addresses.append(0)
        print("Location data imported")

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
        is_num = 1
        i = 0

        while i < len(numbers):
            if char == numbers[i]:
                return 1
            i = i + 1

        return 0

    def same_string(self, string1, string2):

        if len(string1) != len(string2):
            return 0

        match = 1
        for i in range(len(string1)):
            if string1[i] != string2[i]:
                match = 0

        return match

    def load_package(self, truck_id, package, hour, minute):
        open_truck = self.trucks[truck_id - 1]
        if len(open_truck.delivery_queue) < open_truck.MAX_LOAD:
            open_truck.load_package(package, hour, minute)

    def queue_packages(self):
        # create a load queue
        load_queue = []

        # populate load queue
        for i in range(self.packages.listSize):
            if len(self.packages.table[i]) > 0:
                package = self.packages.table[i][0]

                if package.waitlist == 0 and package.get_truck() == "No truck":
                    load_queue.append(package)

        # sort load queue by deadline
        self.package_load_queue = self.sort_package_queue_by_deadline(load_queue)

        for i in range(len(self.package_load_queue)):
            package = self.package_load_queue[i]
            for j in range(len(self.locations)):
                location = self.locations[j]
                location_index = location.get_id() - 1
                if package.get_address() == location.get_address():
                    if self.assigned_addresses[location_index] == 1:
                        self.assigned_addresses[location_index] = 0

    def sort_package_queue_by_deadline(self, queue):

        index = 1
        cache = ''

        while index < len(queue):

            i = index

            j = i - 1

            while j >= 0:

                package_i = queue[i]
                deadline_i = package_i.get_deadline()

                package_j = queue[j]
                deadline_j = package_j.get_deadline()

                if deadline_i < deadline_j:
                    cache = queue[i]
                    queue[i] = queue[j]
                    queue[j] = cache

                    i = i - 1

                j = j - 1

            index = index + 1

        return queue

    def load_truck(self, current_truck, hour, minute, load_queue):

        self.hour_string = hour
        self.min_string = minute

        # self.recursive_load(hub, truck, queue, self.visited)
        # self.recursive_load2(hub.get_id(), truck, self.visited)

        # get the base list of distances to begin routing
        base_list = self.map.adj_matrix[0]

        base_hub = self.locations[0]

        furthest_point = 0

        for i in range(len(base_list)):
            if self.assigned_addresses[i] == 0:
                if base_list[i] > base_list[furthest_point]:
                    furthest_point = i

        furthest_location = self.locations[furthest_point]

        route_queue = self.iterative_route(base_hub.get_id(), furthest_location.get_id())

        for i in range(len(route_queue)):
            if current_truck.get_load() >= current_truck.MAX_LOAD:
                break
            current_location = route_queue.pop(0)
            current_address = current_location.get_address()
            loaded = 0
            for j in range(len(load_queue)):
                if current_truck.get_load() >= current_truck.MAX_LOAD:
                    break
                current_package = load_queue.pop(0)
                if current_package.get_address() == current_address:
                    current_truck.load_package(current_package, hour, minute)
                    current_truck.add_stop(current_location)
                    self.assigned_addresses[current_location.get_id() - 1] = 1
                    loaded = 1
                else:
                    load_queue.append(current_package)
            if loaded == 0:
                route_queue.append(current_location)

    #        plq_length = len(self.package_load_queue)

    #        package = None

    #       for i in range(plq_length):
    #           # while current_truck.get_load() < 16:
    #           if current_truck.get_load() < current_truck.MAX_LOAD:
    #               break

    #           package = self.package_load_queue.pop(0)

    #           for j in range(len(route_queue)):
    #               if package.get_address() == route_queue[j].get_address():
    #                   if current_truck.get_load() < current_truck.MAX_LOAD:
    #                       current_truck.load_package(package, hour, minute)

    #                       package = None

    #                       plq_length = len(self.package_load_queue)

    #                        self.location_queue[route_queue[j].get_id() - 1] = 1

    #                        current_truck.add_stop(route_queue[j])

    #                        break

    def recursive_load(self, location, current_truck, queue, visited):

        if current_truck.get_load() >= current_truck.MAX_LOAD:
            return

        visited.append(location.get_id())

        waitlisted = 0

        row = self.get_location(location)

        list = self.map.adj_matrix[row]

        col = 0

        closest_dist = 1000

        closest_node = self.locations[0]

        been_there = 0
        # Iterate to get the closest node in the load queue
        for i in range(len(queue)):

            been_there = 0
            col = self.get_location(queue[i])

            for k in range(len(visited)):
                if self.locations[col].get_id() == visited[k]:
                    been_there = 1

            if 0.0 < float(list[col]) < float(closest_dist) and been_there == 0:
                if col != row:
                    closest_dist = list[col]
                    closest_node = self.locations[col]

        closest_loaded_dist = 1000
        closest_loaded_node = None

        for j in range(len(self.wait_list)):
            if self.wait_list[j].get_id() == closest_node.get_id():
                waitlisted = 1

        if len(current_truck.delivery_queue) > 0:
            col = self.get_location(current_truck.delivery_queue[0])

            closest_loaded_node = self.locations[col]

            been_there = 0
            # Iterate to get the closest location of any packages loaded
            for i in range(len(current_truck.delivery_queue)):

                been_there = 0
                col = self.get_location(current_truck.delivery_queue[i])

                for k in range(len(visited)):
                    if self.locations[col].get_id() == visited[k]:
                        been_there = 1

                if 0.0 < float(list[col]) < float(closest_loaded_dist) and been_there == 0:
                    if col != row:
                        closest_loaded_dist = list[col]
                        closest_loaded_node = self.locations[col]

        next_node = None
        load_packages = 0

        if float(closest_dist) <= float(closest_loaded_dist):
            next_node = closest_node
            load_packages = 1
        else:
            next_node = closest_loaded_node

        if load_packages == 1 and waitlisted == 0:
            for i in range(len(queue)):
                if queue[i].get_address() == next_node.get_address():
                    current_truck.load_package(queue[i], self.hour_string, self.min_string)
            self.recursive_load(next_node, current_truck, queue, visited)
        else:
            self.recursive_load(next_node, current_truck, queue, visited)

    def recursive_load2(self, location_id, current_truck, visited):

        if current_truck.get_load() >= current_truck.MAX_LOAD:
            return 0

        row = location_id - 1

        for i in range(len(visited)):
            if row == visited[i]:
                return 0

        for i in range(len(self.wait_list)):
            if row == i:
                return 0

        visited.append(row)

        for i in range(len(self.package_load_queue)):
            load_queue_location = self.package_load_queue[i]
            ref_location = self.locations[row]
            if load_queue_location.get_address() == ref_location.get_address():
                current_truck.load_package(self.package_load_queue[i], self.hour_string, self.min_string)

        adjacent_list = self.map.adj_matrix[row]

        sorted_lists = self.sort_nums(adjacent_list)

        sorted_dist = sorted_lists[0]

        sorted_loc = sorted_lists[1]

        nearest = adjacent_list[1]

        for i in range(len(sorted_dist)):
            if self.recursive_load2(sorted_loc[i].get_id(), current_truck, visited) == 1:
                return 1

        return 0

    def iterative_route(self, location_id, dest_id):
        # Create a queue of visited locations
        visited_queue = []

        # Create a log of visited locations and populate it as unvisited (0)
        visited_log = []
        for i in range(len(self.locations)):
            visited_log.append(0)

        # Set the initial start location to visited (1)
        visited_log[location_id - 1] = 1

        # Look for locations in the assigned addresses log and set them to visited, these have had packages delivered
        for i in range(len(self.assigned_addresses)):
            if self.assigned_addresses[i] == 1:
                visited_log[i] = 1

        # Create the path array that will contain the route
        path = []

        # Put the initial location into the queue
        visited_queue.append(location_id)

        # Assign the initial location id for looping
        current_loc_id = location_id

        # =======================================================================================================
        # ==============================================START LOOP HERE==========================================
        # =======================================================================================================
        while len(visited_queue) > 0:

            if len(path) >= len(self.locations):
                break

            if len(visited_queue) <= 0:
                break

            # Grab the next up location in the queue to get its nearest neighbor
            prev_loc_id = current_loc_id
            current_loc_id = visited_queue.pop(0)

            # If we have reached the destination ID, break the loop
            if current_loc_id == dest_id & len(path) > 0:
                break

            # Get the list of distances from the adjacency matrix for this location
            adjacent_list = self.map.adj_matrix[current_loc_id - 1]

            # Arbitrarily set the closest index to 0
            closest_index = 0

            if visited_log[closest_index]:
                if 0 <= closest_index < len(adjacent_list) - 1:
                    closest_index = closest_index + 1
                elif closest_index == len(adjacent_list) - 1:
                    closest_index = closest_index - 1

            while adjacent_list[closest_index] == 0.0:
                if 0 <= closest_index < len(adjacent_list) - 1:
                    closest_index = closest_index + 1
                elif closest_index == len(adjacent_list) - 1:
                    closest_index = closest_index - 1

            # =========================== INNER LOOP TO FIND THE CLOSEST NEIGHBOR ==============================
            for i in range(len(adjacent_list)):

                # next_loc_id = self.locations[i].get_id()

                # checks here!
                # wait listed?

                # If the location is unvisited:
                if visited_log[i] == 0:
                    # And it is closer than the closest index based on the distance list:
                    if 0.0 < adjacent_list[i] < adjacent_list[closest_index]:
                        # Capture this index as the closest
                        closest_index = i

            # Add the closest neighbor to the queue, mark it as visited,
            # add it to path, remove it form loc queue
            visited_queue.append(closest_index + 1)
            visited_log[closest_index] = 1
            path.append(self.locations[closest_index])
            if self.locations[closest_index].get_id() == dest_id:
                break
            # self.location_queue[closest_index] = 1
            # next_loc_id = self.locations[i].get_id()

        return path

    def get_location(self, node):

        row = 0

        node_address = node.get_address()

        for i in range(len(self.locations)):
            if self.locations[i].get_address() == node_address:
                row = i

        return row

    def sort_nums(self, old_list):

        list1 = old_list

        list2 = self.locations

        lists = []

        index = 1
        cache = 0

        while index < len(list1):

            i = index

            j = i - 1

            while j >= 0:

                if list1[i] < list1[j]:
                    # TODO: Instead of just sorting the distnaces, I need a good location list to sort as well to match
                    cache = list1[i]
                    loc_cache = list2[i]
                    list1[i] = list1[j]
                    list2[i] = list2[j]
                    list1[j] = cache
                    list2[j] = loc_cache

                    i = i - 1

                j = j - 1

            index = index + 1

            lists.append(list1)
            lists.append(list2)

        return lists

    def make_trucks(self, new_hub):
        truck1 = truck.Truck(1, new_hub)
        truck2 = truck.Truck(2, new_hub)
        truck3 = truck.Truck(3, new_hub)
        self.trucks.append(truck1)
        self.trucks.append(truck2)
        self.trucks.append(truck3)
        for i in range(2):
            self.drivers.append(driver.Driver(i))
        for i in range(len(self.drivers)):
            self.trucks[i].set_driver(self.drivers[i])

    def get_stop_time(self, truck_param):

        truck_one_leg = truck_param.get_next_leg()

        t1_last = truck_one_leg[0].get_id()
        t1_next = truck_one_leg[1].get_id()

        print(t1_last)
        print(t1_next)

        truck_one_leg = self.map.adj_matrix[t1_last - 1][t1_next - 1]

        t1_leg_time = truck_one_leg / 18

        t1_leg_hr = 0
        t1_leg_min = 0

        while t1_leg_time > 1:
            if t1_leg_time > 1:
                t1_leg_hr = t1_leg_hr + 1
                t1_leg_time = t1_leg_time - 1

        t1_leg_min = int(t1_leg_time * 60)

        t1_target_hour = self.trucks[0].stop_hour + t1_leg_hr
        t1_target_min = self.trucks[0].stop_hour + t1_leg_min

        stop_time = [t1_target_hour, t1_target_min]

        return stop_time
