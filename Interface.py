import package_router
import datetime


class Interface:
    time = ''
    status_list = ['HUB', 'ENROUTE', 'AT STOP']
    total_route_time = ''
    step1 = 0
    step2 = 0
    step3 = 0

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
            print("Run routes, press R\nMenu, press M\nExit program, press X\n")

            user_input = input("Enter selection: ")

            while len(self.router.wait_list) > 0:
                self.router.special_cases.append(self.router.wait_list.pop(0))

            if user_input == 'r' or user_input == 'R':
                self.run_routes()

    def print_status(self, hour, minute):
        print("\n\n" + self.print_time(hour, minute))
        print("-------------------------------------------------------PACKAGE "
              "STATUS------------------------------------------------------")
        print("Trk ID    Pkg ID    Dest. Address                           Deadline       City                Zip "
              "Code      Weight    Status")
        print("------    ------    -------------                           --------       ----                "
              "--------      ------    ------")

        package_list = []
        for i in range(len(self.router.packages.table)):
            if self.router.packages.search(i + 1) is not None:
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
            print(truck_id + gap1 + package_id + gap2 + address + gap3 + deadline + gap4 + city + gap5
                  + zip_code + "........." + weight + gap6 + status)

        print("\nUpcoming stops:")
        print("Truck 1 next stop: " + self.router.trucks[0].next_stop.get_address())
        print("Truck 2 next stop: " + self.router.trucks[1].next_stop.get_address())
        print("Truck 3 next stop: Not on route")

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

    def auto_load_special_cases(self, hour, minute):

        time = minute + (hour * 60)

        if time < 555 and self.step1 == 0:
            self.router.load_package(2, self.router.special_cases[0], hour,
                                     minute)

            self.router.special_cases[1].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[1].get_id())

            self.router.special_cases[2].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[2].get_id())

            truck = self.router.trucks[0]

            truck.load_package(self.router.special_cases[3], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)

            truck.load_package(self.router.special_cases[4], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(19), self.time.hour, self.time.minute)

            self.router.load_package(2, self.router.special_cases[5], self.time.hour,
                                     self.time.minute)

            truck.load_package(self.router.special_cases[6], self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(13), self.time.hour, self.time.minute)
            truck.load_package(self.router.packages.search(15), self.time.hour, self.time.minute)

            self.router.special_cases[7].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[7].get_id())

            self.router.special_cases[8].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[8].get_id())

            self.router.special_cases[9].set_hold(hour, minute)
            self.router.wait_list.append(self.router.special_cases[9].get_id())

            self.router.load_package(2, self.router.special_cases[10], self.time.hour,
                                     self.time.minute)

            self.router.load_package(2, self.router.special_cases[11], self.time.hour,
                                     self.time.minute)

            self.router.special_cases.pop(0)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(2)
            self.router.special_cases.pop(5)
            self.router.special_cases.pop(5)

            self.step1 = 1

        elif 555 <= time < 620 and self.step2 == 0:
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
            self.router.special_cases[0].set_address("410 S State St")
            self.router.special_cases[0].set_city("Salt Lake CIty")
            self.router.special_cases[0].set_zip_code("84111")

            self.router.package_load_queue.append(self.router.special_cases[0])
            self.router.special_cases[0].waitlist = 0
            self.router.special_cases[0].status = 1
            self.router.wait_list.pop(0)

            self.router.special_cases = []

            self.step3 = 1

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

    def print_time(self, hour, minute):

        while hour > 24:
            hour = hour - 12

        if hour == 24 or hour == 0:
            display_hour = str(hour - 12)
            display_t_o_d = "AM"
        elif 24 > hour > 11:
            display_hour = str(hour - 12)
            display_t_o_d = "PM"
        else:
            display_hour = str(hour)
            display_t_o_d = "AM"

        display_minute = str(minute)

        if len(display_minute) == 1:
            display_minute = '0' + display_minute

        return display_hour + ':' + display_minute + ' ' + display_t_o_d

    def run_routes(self):

        user_input = ''

        pause_print = 1

        print("Press C to continue running route.\nEnter pause time: ")

        stop_min = ''

        stop_hour = input("Enter hour: ")
        if self.router.is_num(stop_hour):
            stop_min = input("Enter minute: ")
        else:
            stop_hour = ''

        if stop_hour != 'c' or stop_hour != 'C':
            pause_print = 0

        pause_mark = (stop_hour * 60) + stop_min

        display_time = (8 * 60) - 1

        time_interval = 1

        print_interval = 60

        all_delivered = 0

        while all_delivered == 0:

            display_time = display_time + time_interval

            display_hour = int(display_time / 60)

            while display_hour > 24:
                display_hour = display_hour - 12

            display_minute = int(display_time % 60)

            if len(self.router.special_cases) > 0:
                # self.load_special_cases()
                self.auto_load_special_cases(display_hour, display_minute)

                self.router.queue_packages()

            for i in range(len(self.router.trucks)):
                if self.router.trucks[i].driver != -1 and self.router.trucks[i].at_hub == 1:
                    self.router.queue_packages()
                    self.router.load_truck(self.router.trucks[i], display_hour, display_minute,
                                           self.router.package_load_queue)
                    self.router.trucks[i].toggle_at_hub()

            for i in range(len(self.router.trucks)):

                truck = self.router.trucks[i]

                if len(truck.route_queue) == 0:
                    for f in range(len(truck.delivery_queue)):
                        for g in range(len(self.router.locations)):
                            if truck.delivery_queue[f].get_address() == \
                                    self.router.locations[g].get_address():
                                truck.add_stop(self.router.locations[g])

                if truck.at_hub == 0:
                    next_stop_time = self.router.get_stop_time(truck)

                    next_time_hack = (next_stop_time[0] * 60) + next_stop_time[1]

                    if display_time >= next_time_hack:

                        if truck.next_stop.get_id() == 1:
                            # TODO: Do i load like normal or force load the rest?
                            self.router.queue_packages()

                            if len(self.router.package_load_queue) > 0:
                                self.router.load_truck(truck, display_hour, display_minute,
                                                       self.router.package_load_queue)

                        if len(truck.delivery_queue) > 0:

                            delivered = truck.deliver_packages(display_hour, display_minute)

                            for j in range(len(delivered)):
                                self.router.packages.search(delivered[j]).set_status(3, display_hour, display_minute)

                            truck.complete_stop(display_hour, display_minute)

                        elif len(truck.delivery_queue) == 0:
                            truck.set_next_stop(self.router.locations[0])

                elif truck.at_hub == 1:
                    if len(self.router.special_cases) > 0:
                        # self.load_special_cases()
                        self.auto_load_special_cases(display_hour, display_minute)

                    if truck.driver != -1:
                        self.router.queue_packages()

                        self.router.load_truck(self.router.trucks[i], display_hour, display_minute,
                                               self.router.package_load_queue)
                        truck.toggle_at_hub()
                        if len(truck.route_queue) > 0:
                            truck.set_next_stop(truck.route_queue[0])
                        else:
                            truck.set_next_stop(truck.package_queue[0].get_address())

            if pause_print == 0:
                if display_minute % print_interval == 0:
                    self.print_status(display_hour, display_minute)
            elif pause_print == 1:
                if pause_mark == display_time:
                    self.print_status(display_hour, display_minute)

            all_delivered = 1
            for i in range(self.router.packages.size):
                package_status = self.router.packages.search(i + 1).status
                if package_status != 3:
                    all_delivered = 0

            if display_time >= 1440:
                all_delivered = 1
                package_status = self.router.packages.search(i + 1).status
                print("Its midnight! All your drivers went home!!!!")
