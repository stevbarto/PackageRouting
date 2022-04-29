import unittest
import datetime
import hub
import delivery_location
import linked_list
import map_graph
import package_router
import wgups_hash_table
import wgups_package
from linked_list import LinkedList


class TestMethods(unittest.TestCase):
    """
    Test class for the WGUPS routing program.  Contains test cases to validate requirements before coding
    and detect bugs prior to product release.

    Methods
    -------
    test_createPackage()
        Tests wgups_package.Package methods

    test_testChainingList()
        Tests chaining_list.ChainingList methods

    test_createHashTable()
        Tests wgups_hash_table.HashTable methods

    """

    def test_createPackage(self):
        # Tests for invalid object types in package parameters, all shoudl return RuntimeError
        timeNow = datetime.datetime.now()
        if timeNow.hour + 2 < 24:
            time_hack = timeNow.hour + 2
        else:
            time_hack = 24 - timeNow.hour + 2

        deadline = datetime.datetime(timeNow.year, timeNow.month, timeNow.day, time_hack)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package("1", "test address", deadline, "city", "state", "76558", 4, 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, 3, deadline, "city", "state", "76558", 4, 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", 4, "city", "state", "76558", 4, 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, 4, "state", "76558", 4, 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", 76558, 4, 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", "76558", "4", 1)

        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", "76558", 4, "1")

        # Test for invalid structures in parameters.
        # Zip code boundary case: too few digits.
        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", "7655", 4, 1)
        # Zip code boundary case: too many digits.
        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", "765589", 4, 1)
        # Zip code boundary case: Non digit characters in zip code.
        with self.assertRaises(RuntimeError):
            errorPackage1 = wgups_package.package(1, "test address", deadline, "city", "state", "76t68", 4, 1)

        testPackage = wgups_package.package(1, "test address", deadline, "city", "state", "76558", 4, 1)
        self.assertEqual(testPackage.get_id(), 1)
        self.assertEqual(testPackage.get_address(), "test address")
        self.assertEqual(testPackage.get_deadline(), deadline)
        self.assertEqual(testPackage.get_city(), "city")
        self.assertEqual(testPackage.get_zip_code(), "76558")
        self.assertEqual(testPackage.get_weight(), 4)
        self.assertEqual(testPackage.get_status(), "AT HUB")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package("1", "test address", "deadline", "city", "state", "76558", 4, "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, 1, "deadline", "city", "state", "76558", 4, "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, "test address", 1, "city", "state", "76558", 4, "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, "test address", "deadline", 1, "state", "76558", 4, "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, "test address", "deadline", "city", "state", 76558, 4, "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, "test address", "deadline", "city", "state", "76558", "4", "status")

        with self.assertRaises(RuntimeError):
            invalidPackage = wgups_package.package(1, "test address", "deadline", "city", "state", "76558", 4, 1)

    def test_chainingList(self):

        # Test handling of packages for the hash table

        time_now = datetime.datetime.now()
        if time_now.hour + 2 < 24:
            time_hack = time_now.hour + 2
        else:
            time_hack = 24 - time_now.hour + 2

        deadline = datetime.datetime(time_now.year, time_now.month, time_now.day, time_hack)

        testPackage1 = wgups_package.package(1, "address1", deadline, "city1", "state", '11111', 41, 1)
        testPackage2 = wgups_package.package(2, "address2", deadline, "city2", "state", '22222', 42, 1)
        testPackage3 = wgups_package.package(3, "address4", deadline, "city4", "state", '44444', 44, 1)
        testPackage4 = wgups_package.package(4, "address4", deadline, "city4", "state", '44444', 44, 1)

        testList = LinkedList()
        testList.insert(testPackage1, 0)
        self.assertEqual(testList.size, 1)
        testList.insert(testPackage2, 0)
        self.assertEqual(testList.size, 2)
        testList.insert(testPackage3, 0)
        self.assertEqual(testList.size, 3)

        # testList.delete(testPackage4)
        self.assertEqual(testList.delete(testPackage4), 0)
        # TODO: Do I need to implement a check to avoid duplicate items being added to the hash list?
        # If I do, that reduces the time complexity of insertion due to comparisons every time
        # However the n complexity will be the size of the separate chaining list at the index only...
        testList.delete(testPackage3)
        self.assertEqual(testList.size, 2)
        testList.delete(testPackage1)
        self.assertEqual(testList.size, 1)
        testList.delete(testPackage2)
        self.assertEqual(testList.size, 0)

        self.assertEqual(testList.delete(testPackage1), 0)

        # Test handling of adjacency lists of locations for the graph

        location1 = delivery_location.DeliveryLocation(1, "location1", "1 Street", "city", "state", "11111")
        location2 = delivery_location.DeliveryLocation(2, "location2", "1 Street", "city", "state", "11111")
        location3 = delivery_location.DeliveryLocation(3, "location3", "1 Street", "city", "state", "11111")

        location_list = linked_list.LinkedList()

        location_list.insert(location1, 4)
        location_list.insert(location2, 5)
        location_list.insert(location3, 6)

        self.assertIsInstance(location_list.get_item(1), linked_list.LinkedList.Node)

        self.assertIsInstance(location_list.get_item(2), linked_list.LinkedList.Node)

        self.assertIsInstance(location_list.get_item(1), linked_list.LinkedList.Node)

    def test_createHashTable(self):
        timeNow = datetime.datetime.now()
        if timeNow.hour + 2 < 24:
            time_hack = timeNow.hour + 2
        else:
            time_hack = 24 - timeNow.hour + 2

        deadline = datetime.datetime(timeNow.year, timeNow.month, timeNow.day, time_hack)

        testTable = wgups_hash_table.hashTable(5, 3)
        self.assertEqual(testTable.size, 0)
        testTable.insert(1, "address1", deadline, "city1", "state", '11111', 41, 1)
        self.assertEqual(testTable.size, 1)
        testTable.insert(2, "address2", deadline, "city2", "state", '22222', 42, 1)
        self.assertEqual(testTable.size, 2)
        return_package = testTable.search(2, "address2", deadline, "city2", "state", '22222', 42, 1)
        self.assertEqual(return_package.get_address(), "address2")
        return_package = testTable.search(1, "address1", deadline, "city1", "state", '11111', 41, 1)
        self.assertEqual(return_package.get_address(), "address1")
        testTable.remove(2, "address2", deadline, "city2", "state", '22222', 42, 1)
        self.assertEqual(testTable.size, 1)
        testTable.remove(1, "address1", deadline, "city1", "state", '11111', 41, 1)
        self.assertEqual(testTable.size, 0)
        # self.assertEqual(testTable.hash(10, 0))
        # self.assertEqual(testTable.hash(21, 1))
        # self.assertEqual(testTable.hash(65, 5))
        # TODO: Need to fix the rehash sizes and tests to make sure its working.
        testTable.insert(1, "address1", deadline, "city1", "state", '11111', 41, 1)
        self.assertEqual(testTable.listSize, 5)
        testTable.insert(2, "address2", deadline, "city2", "state", '22222', 42, 1)
        self.assertEqual(testTable.listSize, 5)
        testTable.insert(3, "address3", deadline, "city3", "state", '33333', 43, 1)
        self.assertEqual(testTable.listSize, 5)
        testTable.insert(4, "address4", deadline, "city4", "state", '44444', 44, 1)
        self.assertEqual(testTable.listSize, 5)
        testTable.insert(5, "address5", deadline, "city5", "state", '55555', 45, 1)
        self.assertEqual(testTable.listSize, 5)
        testTable.insert(6, "address6", deadline, "city6", "state", '66666', 46, 1)
        self.assertEqual(testTable.listSize, 5)
        return_package = testTable.search(6, "address6", deadline, "city6", "state", '66666', 46, 1)
        self.assertEqual(return_package.get_address(), "address6")

    def test_create_map_graph(self):
        test_hub = hub.Hub(1, "HUBBY McHUBFACE", "address", "city", "state", "22222")

        location1 = delivery_location.DeliveryLocation(1, "First Stop", "address1", "zip", test_hub.id)
        location2 = delivery_location.DeliveryLocation(2, "second Stop", "address2", "zip", test_hub.id)
        location3 = delivery_location.DeliveryLocation(3, "third stop", "address3", "zip", test_hub.id)

        map = map_graph.MapGraph()

        map.insert_vertex(location1)
        self.assertEqual(1, map.size)
        map.insert_vertex(location2)
        self.assertEqual(2, map.size)
        map.insert_vertex(location3)
        self.assertEqual(3, map.size)

        map.insert_edge(location1, location2, 4)  # Valid Add
        self.assertEqual(2, map.get_vertex(location1.get_id()).size)
        test_list = map.get_vertex(location1.get_id())
        test_location = test_list.get_item(location2.get_id())
        test_val = test_location.get_value()
        self.assertEqual(4, test_list.get_item(location2.get_id()).get_value())
        self.assertEqual(2, map.get_vertex(location2.get_id()).size)
        self.assertEqual(4, map.get_vertex(location2.get_id()).get_item(location1.get_id()).value)
        self.assertEqual(1, map.get_vertex(location3.get_id()).size)
        map.insert_edge(location1, location3, 7)  # Valid Add
        self.assertEqual(3, map.get_vertex(location1.get_id()).size)
        self.assertEqual(7, map.get_vertex(location1.get_id()).get_item(location3.get_id()).value)
        self.assertEqual(2, map.get_vertex(location2.get_id()).size)
        self.assertEqual(7, map.get_vertex(location3.get_id()).get_item(location1.get_id()).value)
        self.assertEqual(2, map.get_vertex(location3.get_id()).size)

        map.insert_edge(location2, location1, 3)  # Invalid Add
        self.assertEqual(3, map.get_vertex(location1.get_id()).size)
        self.assertEqual(4, map.get_vertex(location2.get_id()).get_item(location1.get_id()).value)
        self.assertEqual(2, map.get_vertex(location2.get_id()).size)
        self.assertEqual(4, map.get_vertex(location1.get_id()).get_item(location2.get_id()).value)
        self.assertEqual(2, map.get_vertex(location3.get_id()).size)
        map.insert_edge(location2, location3, 9)  # Valid Add
        self.assertEqual(3, map.get_vertex(location1.get_id()).size)
        self.assertEqual(9, map.get_vertex(location2.get_id()).get_item(location3.get_id()).value)
        self.assertEqual(3, map.get_vertex(location2.get_id()).size)
        self.assertEqual(9, map.get_vertex(location3.get_id()).get_item(location2.get_id()).value)
        self.assertEqual(3, map.get_vertex(location3.get_id()).size)

        map.insert_edge(location3, location1, 8)  # Invalid Add
        self.assertEqual(3, map.get_vertex(location1.get_id()).size)
        self.assertEqual(7, map.get_vertex(location3.get_id()).get_item(location1.get_id()).value)
        self.assertEqual(3, map.get_vertex(location2.get_id()).size)
        self.assertEqual(7, map.get_vertex(location1.get_id()).get_item(location3.get_id()).value)
        self.assertEqual(3, map.get_vertex(location3.get_id()).size)
        map.insert_edge(location3, location2, 7)  # Invalid Add
        self.assertEqual(3, map.get_vertex(location1.get_id()).size)
        self.assertEqual(9, map.get_vertex(location3.get_id()).get_item(location2.get_id()).value)
        self.assertEqual(3, map.get_vertex(location2.get_id()).size)
        self.assertEqual(9, map.get_vertex(location2.get_id()).get_item(location3.get_id()).value)
        self.assertEqual(3, map.get_vertex(location3.get_id()).size)




