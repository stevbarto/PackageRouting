import package_router
import datetime


class Interface:
    """
    Interface class, controlls all display elements, user input, and overall logic to run the program.
    """
    # Instance variables used in running the interface
    time = ''
    status_list = ['HUB', 'ENROUTE', 'AT STOP']
    step1 = 0
    step2 = 0
    step3 = 0

    def __init__(self):
        """
        Constructor method for the interface object, starts the package router instance
        """
        self.router = package_router.PackageRouter()

    def run(self):
        """
        Run method, entry point for the interface to initiate. Begins data imports and designates the current time for
        the application methods.
        :return: None
        """
        # Imports locations and packages using the package router methods
        self.router.import_locations()
        self.router.import_packages()

        # Initiates the program run time at 8:00 am with the current year, month, and day
        index_date = datetime.datetime.now()
        self.time = datetime.datetime(index_date.year, index_date.month, index_date.day, 8, 00, 00, 00)

        # Initiates the main interface menu
        self.main_interface(self.time)

    def main_interface(self, time):
        """
        Main interface menu method, runs the main application menu.
        :param time: datetime object set to the start time for the work day (8:00 AM)
        :return: None
        """
        # Initiation of stop variable for running the main menu
        user_input = ''

        # =========================================================================================
        # ============================= Initiate main menu loop here ==============================
        # =========================================================================================
        while user_input != 'x' and user_input != 'X':
            # Print header
            print("\n\n----------WGUPS PACKAGE ROUTING----------")
            print("Run routes, press R\nExit program, press X\n")
            # Input prompt and message
            user_input = input("Enter selection: ")
            # Initiate the routes
            if user_input == 'r' or user_input == 'R':
                self.run_routes()

    def print_status(self, hour, minute):
        """
        Method to print the current status update for packages and truck distance.
        :param hour: int hour value
        :param minute: int minute value
        :return: None
        """
        # Print header for the status screen
        print("\n\n" + self.print_time(hour, minute))
        print("-------------------------------------------------------PACKAGE "
              "STATUS------------------------------------------------------")
        print("Trk ID    Pkg ID    Dest. Address                           Deadline       City                Zip "
              "Code      Weight    Status")
        print("------    ------    -------------                           --------       ----                "
              "--------      ------    ------")
        # Build the package list for display
        package_list = []
        for i in range(len(self.router.packages.table)):
            if self.router.packages.search(i + 1) is not None:
                package_list.append(self.router.packages.search(i + 1))

        # loop to get and print the package data
        for j in range(len(package_list)):

            package = package_list[j]

            truck_id = str(package.get_truck())

            gap1 = ""
            i = len(truck_id)
            while i < 10:
                gap1 = gap1 + "."
                i = i + 1

            package_id = str(package.get_id())

            gap2 = ""
            i = len(package_id)
            while i < 10:
                gap2 = gap2 + "."
                i = i + 1

            address = package.get_address()

            gap3 = ""
            i = len(address)
            while i < 40:
                gap3 = gap3 + "."
                i = i + 1

            deadline = self.print_time(package.get_deadline().hour, package.get_deadline().minute)

            gap4 = ""
            i = len(deadline)
            while i < 15:
                gap4 = gap4 + "."
                i = i + 1

            city = package.get_city()

            gap5 = ""
            i = len(city)
            while i < 20:
                gap5 = gap5 + "."
                i = i + 1

            zip_code = package.get_zip_code()

            weight = str(package.get_weight()) + " kg"

            gap6 = ""
            i = len(weight)
            while i < 10:
                gap6 = gap6 + "."
                i = i + 1

            status = package.get_status()
            # Print statement for each package
            print(truck_id + gap1 + package_id + gap2 + address + gap3 + deadline + gap4 + city + gap5
                  + zip_code + "........." + weight + gap6 + status)

        # Print the truck distances and total distance
        dist1 = self.router.trucks[0].route_distance
        dist2 = self.router.trucks[1].route_distance
        dist3 = self.router.trucks[2].route_distance
        print("\nUpcoming stops:")
        print("Truck 1 total distance: " + str(dist1))
        print("Truck 2 total distance: " + str(dist2))
        print("Truck 3 total distance: " + str(dist3))
        combined = dist1 + dist2 + dist3
        print("Combined total distance: " + str(combined))

    def auto_load_special_cases(self, hour, minute):
        """
        Method which simulates user input to handle special cases of package.
        :param hour: int value for the hour
        :param minute: int value for the minutes
        :return: None
        """
        # Generate the current time in total minutes for comparison
        time = minute + (hour * 60)

        # If time is within parameters for the first set of special cases handle them
        if time < 555 and self.step1 == 0:
            # Package 3: Can only be on truck 2
            self.router.load_package(2, self.router.special_cases[0], hour,
                                     minute)
            # Package 6: Delayed on flight---will not arrive to depot until 9:05 am
            self.router.special_cases[1].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[1].get_id())
            # Package 9: Wrong address listed
            self.router.special_cases[2].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[2].get_id())

            truck = self.router.trucks[0]
            # Package 14: Must be delivered with 15, 19
            truck.load_package(self.router.special_cases[3], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)
            # Package 16: Must be delivered with 13, 19
            truck.load_package(self.router.special_cases[4], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)
            # Package 18: Can only be on truck 2
            self.router.load_package(2, self.router.special_cases[5], self.time.hour,
                                     self.time.minute)
            # Package 20: Must be delivered with 13, 15
            truck.load_package(self.router.special_cases[6], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)
            # Package 25: Delayed on flight---will not arrive to depot until 9:05 am
            self.router.special_cases[7].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[7].get_id())
            # Package 28: Delayed on flight---will not arrive to depot until 9:05 am
            self.router.special_cases[8].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[8].get_id())
            # Package 32: Delayed on flight---will not arrive to depot until 9:05 am
            self.router.special_cases[9].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[9].get_id())
            # Package 36: Can only be on truck 2
            self.router.load_package(2, self.router.special_cases[10], self.time.hour,
                                     self.time.minute)
            # Package 38: Can only be on truck 2
            self.router.load_package(2, self.router.special_cases[11], self.time.hour,
                                     self.time.minute)

            # Remove all packages that were loaded at this point
            self.router.special_cases.pop(0)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(5)
            self.router.special_cases.pop(5)

            self.step1 = 1

        elif 555 <= time < 620 and self.step2 == 0:
            # Take wait list packages from above that can be loaded at this point in time and queue them
            self.router.package_load_queue.append(self.router.special_cases[0])
            self.router.special_cases[0].waitlist = 0
            self.router.special_cases[0].status = 1
            self.router.wait_list.pop(0)
            self.router.package_load_queue.append(self.router.special_cases[2])
            self.router.special_cases[2].waitlist = 0
            self.router.special_cases[2].status = 1
            self.router.wait_list.pop(1)
            self.router.package_load_queue.append(self.router.special_cases[3])
            self.router.special_cases[3].waitlist = 0
            self.router.special_cases[3].status = 1
            self.router.wait_list.pop(1)
            self.router.package_load_queue.append(self.router.special_cases[4])
            self.router.special_cases[4].waitlist = 0
            self.router.special_cases[4].status = 1
            self.router.wait_list.pop(1)
            self.router.special_cases.pop(0)
            self.router.special_cases.pop(1)
            self.router.special_cases.pop(1)
            self.router.special_cases.pop(1)

            self.step2 = 1

        elif time >= 620 and self.step3 == 0:
            # Change the address on the final package and queue it for loading
            self.router.special_cases[0].set_address("410 S State St")
            self.router.special_cases[0].set_city("Salt Lake CIty")
            self.router.special_cases[0].set_zip_code("84111")

            self.router.package_load_queue.append(self.router.special_cases[0])
            self.router.special_cases[0].waitlist = 0
            self.router.special_cases[0].status = 1
            self.router.wait_list.pop(0)

            self.router.special_cases = []

            self.step3 = 1

    def print_time(self, hour, minute):
        """
        Method to print the time in proper format for display.
        :param hour: int hour value
        :param minute: int minute value
        :return: str object with the time in proper format
        """
        # If the hour comes back over 24, bring it back within bounds
        while hour > 24:
            hour = hour - 12

        # Dictate the proper hour number for the time of day, designate the right time of day string
        if hour == 24 or hour == 0:
            display_hour = str(hour - 12)
            display_t_o_d = "AM"
        elif 24 > hour > 11:
            display_hour = str(hour - 12)
            display_t_o_d = "PM"
        else:
            display_hour = str(hour)
            display_t_o_d = "AM"

        # Generate the minute portion and ensure it is formatted
        display_minute = str(minute)

        if len(display_minute) == 1:
            display_minute = '0' + display_minute
        # Return an assembled time string
        return display_hour + ':' + display_minute + ' ' + display_t_o_d

    def run_routes(self):
        """
        Method to iteratively run the truck routes until complete or midnight is reached.  Pause point can be
        designated to stop execution at a necessary time
        :return: None
        """
        # Initiate variable to print a status
        pause_print = 1

        # Display user instructions
        print("Press C to continue running route.\nEnter pause time: ")

        #Prompt user input and generate time variables
        stop_min = ''

        stop_hour = input("Enter hour: ")
        if self.router.is_num(stop_hour):
            stop_min = input("Enter minute: ")
        else:
            stop_hour = ''

        if stop_hour != 'c' or stop_hour != 'C':
            pause_print = 0

        pause_mark = (stop_hour * 60) + stop_min

        display_hour = 0

        display_minute = 0

        display_time = (8 * 60) - 1

        time_interval = 1
        # If no pause points are designated this determines how often a status should print during looping
        print_interval = 60
        # Control variable to determine when looping should stop
        all_delivered = 0

        # ==============================================================================================
        # ==================================== Initiate route loop here ================================
        # ==============================================================================================
        while all_delivered == 0:
            # Increment the display time
            display_time = display_time + time_interval
            # Generate the hour value
            display_hour = int(display_time / 60)
            # Ensure the hour is within bounds
            while display_hour > 24:
                display_hour = display_hour - 12
            # Generate the display minute
            display_minute = int(display_time % 60)

            # Load special cases and queue packages for load
            if len(self.router.special_cases) > 0:
                self.auto_load_special_cases(display_hour, display_minute)
                self.router.queue_packages()

            # ======================== Loop through trucks for loading ========================
            for i in range(len(self.router.trucks)):
                # If the truck has a driver and is at the hub:
                if self.router.trucks[i].driver != -1 and self.router.trucks[i].at_hub == 1:
                    # Load and dispatch the truck
                    self.router.load_truck(self.router.trucks[i], display_hour, display_minute,
                                           self.router.package_load_queue)
                    self.router.trucks[i].toggle_at_hub()
            # ======================= Loop through trucks for deliveries ========================
            for i in range(len(self.router.trucks)):
                # Get truck
                truck = self.router.trucks[i]
                # If the route queue is empty, get locations based on existing package addresses
                if len(truck.route_queue) == 0:
                    for f in range(len(truck.delivery_queue)):
                        for g in range(len(self.router.locations)):
                            if truck.delivery_queue[f].get_address() == \
                                    self.router.locations[g].get_address():
                                truck.add_stop(self.router.locations[g])
                # If the truck is not at the hub, handle delivery cases
                if truck.at_hub == 0:
                    # Get the dime stamp where the truck will be at the next stop
                    next_stop_time = self.router.get_stop_time(truck)
                    # Convert to minutes
                    next_time_hack = (next_stop_time[0] * 60) + next_stop_time[1]
                    # If the time hack is here, deliver packages
                    if display_time >= next_time_hack:
                        # Append the distance based on the leg just completed
                        truck.route_distance = truck.route_distance + self.router.get_leg_distance(truck)
                        # If the truck is at the hub, load again and roll out
                        if truck.next_stop.get_id() == 1:
                            self.router.queue_packages()
                            # If there are packages waiting, load them
                            if len(self.router.package_load_queue) > 0:
                                self.router.load_truck(truck, display_hour, display_minute,
                                                       self.router.package_load_queue)
                        # If there are still packages left:
                        if len(truck.delivery_queue) > 0:
                            # Deliver any for this location, returns an array of IDs
                            delivered = truck.deliver_packages(display_hour, display_minute)
                            # Use array of IDs to update statuses
                            for j in range(len(delivered)):
                                self.router.packages.search(delivered[j]).set_status(3, display_hour, display_minute)
                            # Update data relating to stops and status
                            truck.complete_stop(display_hour, display_minute)
                        # If the truck is empty, head home now to reload or complete
                        elif len(truck.delivery_queue) == 0:
                            truck.set_next_stop(self.router.locations[0])
                # If the truck is at the hub:
                elif truck.at_hub == 1:
                    # And if there are still special cases, handle them
                    if len(self.router.special_cases) > 0:
                        self.auto_load_special_cases(display_hour, display_minute)
                    # If the truck has a driver, queue, load, and dispatch
                    if truck.driver != -1:
                        self.router.queue_packages()
                        self.router.load_truck(self.router.trucks[i], display_hour, display_minute,
                                               self.router.package_load_queue)
                        truck.toggle_at_hub()
                        # If the route queue is empyt, get package addresses to complete deliveries
                        if len(truck.route_queue) > 0:
                            truck.set_next_stop(truck.route_queue[0])
                        else:
                            truck.set_next_stop(truck.package_queue[0].get_address())
            # Logic to handle printing instructions
            if pause_print == 0:
                if display_minute % print_interval == 0:
                    self.print_status(display_hour, display_minute)
            elif pause_print == 1:
                if pause_mark == display_time:
                    self.print_status(display_hour, display_minute)
            # Determine if packages are delivered or if its midnight, if so end the loop.
            all_delivered = 1
            for i in range(self.router.packages.size):
                package_status = self.router.packages.search(i + 1).status
                if package_status != 3:
                    all_delivered = 0

            if display_time >= 1440:
                all_delivered = 1
                package_status = self.router.packages.search(i + 1).status
                print("Its midnight! All your drivers went home!!!!")
        # Print the final status.
        self.print_status(display_hour, display_minute)

