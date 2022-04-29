import package_router
import datetime


class Interface:
    time = ''
    status_list = ['HUB', 'ENROUTE', 'AT STOP']
    total_route_time = ''

    def __init__(self):
        self.router = package_router.PackageRouter()

    def run(self):

        self.router.import_locations()

        self.router.import_packages()

        index_date = datetime.datetime.now()

        self.time = datetime.datetime(index_date.year, index_date.month, index_date.day, 8, 00, 00, 00)
        self.total_route_time = datetime.datetime(index_date.year, index_date.month, index_date.day, 0, 0)

        self.main_interface(self.time)

    def main_interface(self, time):
        user_input = ''

        time_interval = datetime.timedelta(minutes=5)

        display_time = time

        display_time = display_time - time_interval

        while user_input != 'x' and user_input != 'X':
            print("\n\n----------WGUPS PACKAGE ROUTING----------")
            print("Run or Continue routes, press C\nMenu, press M\nExit program, press X\n")

            user_input = input("Enter selection: ")

            if user_input == 'c' or user_input == 'C':

                if len(self.router.special_cases) > 0:
                    # self.load_special_cases()
                    self.auto_load_special_cases()

                self.router.queue_packages()

                for i in range(len(self.router.trucks)):
                    if self.router.trucks[i].driver != -1 and self.router.trucks[i].at_hub == 1:
                        self.router.queue_packages()
                        self.router.load_truck(self.router.trucks[i],
                                               display_time.hour, display_time.minute, self.router.package_load_queue)

                display_time = display_time + time_interval
                self.total_route_time = self.total_route_time + time_interval

                for i in range(len(self.router.trucks)):

                    truck = self.router.trucks[i]

                    if truck.at_hub == 0:
                        next_stop_time = self.router.get_stop_time(truck)

                        if display_time.hour >= next_stop_time[0] and display_time.minute >= next_stop_time[1]:

                            if truck.next_stop.get_id() == 1:
                                truck.toggle_at_hub()

                            if len(truck.route_queue) > 0:
                                truck.deliver_packages(next_stop_time[0], next_stop_time[1])
                                truck.complete_stop(next_stop_time[0], next_stop_time[1])

                            elif len(truck.route_queue) == 0:
                                truck.set_next_stop(self.router.locations[0])

                    elif truck.at_hub == 1:
                        if len(self.router.special_cases) > 0:
                            # self.load_special_cases()
                            self.auto_load_special_cases()

                        self.router.queue_packages()

                        if truck.driver != -1:
                            self.router.queue_packages()
                            self.router.load_truck(self.router.trucks[i],
                                                   display_time.hour, display_time.minute,
                                                   self.router.package_load_queue)
                            truck.toggle_at_hub()
                            if len(truck.route_queue) > 0:
                                truck.set_next_stop(truck.route_queue[0])

                self.print_status(display_time)

    def print_status(self, display_time):
        print("\n\n" + self.print_time(display_time))
        print("\n-------------------------------------------------------PACKAGE "
              "STATUS------------------------------------------------------")
        print("Trk ID    Pkg ID    Dest. Address                           Deadline       City                Zip "
              "Code      Weight    Status")
        print("------    ------    -------------                           --------       ----                "
              "--------      ------    ------")

        package_list = []
        for i in range(len(self.router.packages.table)):
            if self.router.packages.search(i + 1) != None:
                package_list.append(self.router.packages.search(i + 1))

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

            deadline = self.print_time(package.get_deadline())

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
            print(truck_id + gap1 + package_id + gap2 + address + gap3 + deadline + gap4 + city + gap5
                  + zip_code + "........." + weight + gap6 + status)

    def load_special_cases(self):
        menu_input = ''
        i = 0

        while menu_input != 'x' or menu_input != 'X':
            package = self.router.special_cases[i]

            print("\n\n------PACKAGES REQUIRE DECISION PRIOR TO SHIPPING!------")

            print("Go to next package, press N")
            print("Add package dependencies and load together, press A")
            print("Load package on designated truck, enter truck number 1-3")
            print("To wait-list a package press W")
            print("To exit to main menu press X")

            print("\nPackage ID number " + str(package.get_id()) +
                  " instructions: " + package.get_instructions() + "\n")

            menu_input = input("Enter selection: ")

            if menu_input == '1':
                self.router.load_package(1, package, self.time.hour, self.time.minute)
                self.router.special_cases.remove(package)
                i = 0
            elif menu_input == '2':
                self.router.load_package(2, self.router.packages.search(package.get_id()), self.time.hour,
                                         self.time.minute)
                self.router.special_cases.remove(package)
                i = 0
            elif menu_input == '3':
                self.router.load_package(3, package, self.time.hour, self.time.minute)
                self.router.special_cases.remove(package)
                i = 0
            elif menu_input == 'a' or menu_input == 'A':
                self.dependency_menu(self.router.special_cases[i], self.time.hour, self.time.minute)
                i = 0
            elif menu_input == 'w' or menu_input == 'W':
                package.set_hold()
                self.router.wait_list.append(package.get_id())
                self.router.special_cases.remove(package)
                i = 0
            elif menu_input == 'n' or menu_input == 'N':
                i = i + 1
                if i == len(self.router.special_cases):
                    i = 0
                continue

            if len(self.router.special_cases) <= 0 or menu_input == 'x' or menu_input == 'X':
                return

    def auto_load_special_cases(self):

        self.router.load_package(2, self.router.packages.search(self.router.special_cases[0].get_id()), self.time.hour,
                                 self.time.minute)

        self.router.special_cases[1].set_hold()
        self.router.wait_list.append(self.router.special_cases[1].get_id())

        self.router.special_cases[2].set_hold()
        self.router.wait_list.append(self.router.special_cases[2].get_id())

        truck = self.router.trucks[0]

        truck.load_package(self.router.special_cases[3], self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)

        truck.load_package(self.router.special_cases[4], self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)

        self.router.load_package(2, self.router.packages.search(self.router.special_cases[5].get_id()), self.time.hour,
                                 self.time.minute)

        truck.load_package(self.router.special_cases[6], self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
        truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)

        self.router.special_cases[7].set_hold()
        self.router.wait_list.append(self.router.special_cases[7].get_id())

        self.router.special_cases[8].set_hold()
        self.router.wait_list.append(self.router.special_cases[8].get_id())

        self.router.special_cases[9].set_hold()
        self.router.wait_list.append(self.router.special_cases[9].get_id())

        self.router.load_package(2, self.router.packages.search(self.router.special_cases[10].get_id()), self.time.hour,
                                 self.time.minute)

        self.router.load_package(2, self.router.packages.search(self.router.special_cases[11].get_id()), self.time.hour,
                                 self.time.minute)

        self.router.special_cases = []

    def dependency_menu(self, current_package, hour, minute):

        menu_input = ''

        ref_package = None

        dependency = [current_package]

        while menu_input != 'x' and menu_input != 'X':
            print("\n\n----------ADD DEPENDENCIES----------")
            print(current_package.get_instructions())
            print("Enter package id number to add a dependency to package " + str(current_package.get_id()) + ": ")
            print("When complete, to remove package and exit to previous menu, press X\n")

            if len(dependency) > 0:
                print("Current dependencies: ")
                for i in range(len(dependency)):
                    print(dependency[i].get_id())

            menu_input = input("Enter selection: ")

            is_num = 1

            for i in range(len(menu_input)):
                if self.router.is_num(menu_input[i]) == 0:
                    is_num = 0

            if is_num == 1:
                selected_id = int(menu_input)
                ref_package = self.router.packages.search(selected_id)
                dependency.append(ref_package)

            if ref_package is not None:
                # ref_package.connect_package(current_package)
                # current_package.connect_package(ref_package)
                pass

        truck = self.router.trucks[0]

        if self.router.trucks[0].get_load() >= 16:
            truck = self.router.trucks[1]

        if self.router.trucks[1].get_load() >= 16:
            truck = self.router.trucks[2]

        for i in range(len(dependency)):
            truck.load_package(dependency[i], hour, minute)

        self.router.special_cases.remove(current_package)

        print("\n\n")

    def wait_list_menu(self, package):
        menu_input = ''
        wait_hour = ''
        wait_min = ''

        while menu_input != 'x' or menu_input != 'X':
            print("\n\n----------WAITLIST PACKAGE----------")
            print(package.get_instructions())
            print("Enter hours then minutes to waitlist package " + str(package.get_id()) + ": ")
            print("If wait-list is unknown time, press U")
            print("To exit to previous menu press X")

            wait_hour = input("Enter hour time(24 hour format): ")
            if wait_hour == 'x' or wait_hour == 'X':
                return
            wait_min = input("Enter minute time: ")
            if wait_min == 'x' or wait_min == 'X':
                return

            is_num = 1

            for i in range(len(wait_hour)):
                if self.router.is_num(wait_hour[i]) == 0:
                    is_num = 0
                if self.router.is_num(wait_min[i]) == 0:
                    is_num = 0

            if is_num == 1 or wait_hour == 'u' or wait_hour == 'U':
                package.set_hold(wait_hour, wait_min)
                self.router.wait_list.append(package.get_id())
                self.router.special_cases.remove(package)
                return

    def print_time(self, time):
        if time.hour > 11:
            display_hour = str(time.hour - 12)
            display_t_o_d = "PM"
        else:
            display_hour = str(time.hour)
            display_t_o_d = "AM"

        display_minute = str(time.minute)

        if len(display_minute) == 1:
            display_minute = '0' + display_minute

        return display_hour + ':' + display_minute + ' ' + display_t_o_d
