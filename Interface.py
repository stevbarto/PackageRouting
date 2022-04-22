import package_router
import datetime


class Interface:

    def __init__(self):
        self.router = package_router.PackageRouter()

    def run(self):

        self.router.import_locations()

        self.router.import_packages()

        index_date = datetime.datetime.now()

        time = datetime.datetime(index_date.year, index_date.month, index_date.day, 8, 00, 00, 00)

        self.main_interface(time)

    def main_interface(self, time):
        user_input = ''

        time_interval = datetime.timedelta(minutes=5)

        display_time = time

        display_time = display_time - time_interval

        print("\n----------WGUPS PACKAGE ROUTING----------")
        print("\nRun/Continue routes, press ENTER\nMenu, press M\nExit program, press X\n")

        while user_input != 'x' and user_input != 'X':

            display_time = display_time + time_interval

            self.print_time(display_time)
            self.print_trucks()

            user_input = input("Input: ")

            if user_input == '\n':
                continue
            elif user_input == 'm' or user_input == 'M':
                self.user_menu()

    def user_menu(self):
         print("\n----------USER MENU----------")
         print("\nExit menu, press X\n")

         menu_input = ''

         while menu_input != 'x' and menu_input != 'X':

             menu_input = input("Input: ")



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

        print(display_hour + ':' + display_minute + ' ' + display_t_o_d)

    def print_trucks(self):
        pass
