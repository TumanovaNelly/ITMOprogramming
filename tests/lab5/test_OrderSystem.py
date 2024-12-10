import unittest
from src.lab5.OrderSystem import (Person, Address, Order, PhoneNumber, Priority,
                                  ProductsList, AcceptableError, OrdersReader, Identify)


class TestPerson(unittest.TestCase):
    def test_person_creation(self):
        person = Person("Doe", "John", "Smith")
        self.assertEqual(str(person), "Doe John Smith")

        person_without_patronymic = Person("Doe", "Jane")
        self.assertEqual(str(person_without_patronymic), "Doe Jane")


class TestAddress(unittest.TestCase):
    def test_address_creation(self):
        address = Address("USA", "California", "Los Angeles", "Main Street")
        self.assertEqual(str(address), "USA. California. Los Angeles. Main Street.")


class TestPhoneNumber(unittest.TestCase):
    def test_valid_phone_number(self):
        phone = PhoneNumber("+1-123-456-78-90")
        self.assertEqual(str(phone), "+1-123-456-78-90")

    def test_invalid_phone_number(self):
        self.assertRaises(ValueError, PhoneNumber, "123456")


class TestIdentify(unittest.TestCase):
    def test_valid_identify(self):
        identify = Identify("12345")
        self.assertEqual(str(identify), "12345")

    def test_invalid_identify(self):
        self.assertRaises(ValueError, Identify, "abc")



class TestPriority(unittest.TestCase):
    def test_valid_priority(self):
        priority = Priority("MAX")
        self.assertEqual(str(priority), "MAX")
        self.assertEqual(priority.priority, 2)

    def test_invalid_priority(self):
        self.assertRaises(ValueError, Priority, "INVALID")


class TestProductsList(unittest.TestCase):
    def setUp(self):
        self.products = ProductsList()

    def test_add_products(self):
        self.products.add("Apple")
        self.products.add("Banana")
        self.products.add("Apple")
        self.assertEqual(str(self.products), "Apple x2, Banana")

    def test_invalid_products_add(self):
        self.assertRaises(ValueError, self.products.add, "  ")


class TestOrder(unittest.TestCase):
    def test_order_comparison_simple(self):
        order1 = Order(
            identify=Identify("12345"),
            customer=Person("Doe", "John"),
            address=Address("Canada", "California", "Los Angeles", "Main Street"),
            phone=PhoneNumber("+1-123-456-78-90"),
            priority=Priority("MAX"),
            products=ProductsList()
        )

        order2 = Order(
            identify=Identify("54321"),
            customer=Person("Smith", "Jane"),
            address=Address("USA", "Ontario", "Toronto", "Queen Street"),
            phone=PhoneNumber("+1-987-654-32-10"),
            priority=Priority("MIDDLE"),
            products=ProductsList()
        )

        self.assertLess(order1, order2)

        order1 = Order(
            identify=Identify("12345"),
            customer=Person("Doe", "John"),
            address=Address("USA", "California", "Los Angeles", "Main Street"),
            phone=PhoneNumber("+1-123-456-78-90"),
            priority=Priority("MAX"),
            products=ProductsList()
        )

        self.assertLess(order1, order2)

    def test_order_comparison_russia(self):
        order1 = Order(
            identify=Identify("12345"),
            customer=Person("Doe", "John"),
            address=Address("USA", "California", "Los Angeles", "Main Street"),
            phone=PhoneNumber("+1-123-456-78-90"),
            priority=Priority("MAX"),
            products=ProductsList()
        )

        order2 = Order(
            identify=Identify("54321"),
            customer=Person("Smith", "Jane"),
            address=Address("Россия", "Ontario", "Toronto", "Queen Street"),
            phone=PhoneNumber("+1-987-654-32-10"),
            priority=Priority("MIDDLE"),
            products=ProductsList()
        )

        self.assertLess(order2, order1)

        order1 = Order(
            identify=Identify("12345"),
            customer=Person("Doe", "John"),
            address=Address("Россия", "California", "Los Angeles", "Main Street"),
            phone=PhoneNumber("+1-123-456-78-90"),
            priority=Priority("MAX"),
            products=ProductsList()
        )

        self.assertLess(order1, order2)


class TestOrdersReader(unittest.TestCase):
    def test_read_valid_order_data(self):
        reader = OrdersReader()
        order_data = (
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX"
        )
        order = reader.read_order_data(order_data)
        self.assertEqual(order.identify.identify, "12345")
        self.assertEqual(str(order.customer), "Doe John")
        self.assertEqual(str(order.address), "USA. California. Los Angeles. Main Street.")
        self.assertEqual(str(order.phone), "+1-123-456-78-90")
        self.assertEqual(str(order.priority), "MAX")
        self.assertEqual(str(order.products), "Apple x2, Banana")

    def test_read_invalid_address_order_data(self):
        reader = OrdersReader()
        invalid_order_data = (
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles;+1-123-456-78-90;MAX",
            "12345;Apple, Apple, Banana;Doe John;;+1-123-456-78-90;MAX"
        )
        for order_data in invalid_order_data:
            self.assertRaises(AcceptableError, reader.read_order_data, order_data)
        self.assertEqual(reader.exceptions, [("12345", 1, 'USA. California. Los Angeles'),
                                                    ("12345", 1, 'no data')])

    def test_read_invalid_phone_order_data(self):
        reader = OrdersReader()
        invalid_order_data = (
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;123-456-78-90;MAX",
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;;MAX"
        )
        for order_data in invalid_order_data:
            self.assertRaises(AcceptableError, reader.read_order_data, order_data)
        self.assertEqual(reader.exceptions, [("12345", 2, '123-456-78-90'),
                                                    ("12345", 2, 'no data')])

    def test_read_invalid_other_order_data(self):
        reader = OrdersReader()
        invalid_order_data = (
            "1234;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            ";Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            "12345;Apple, , Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            "12345;  ;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            "12345;Apple, Apple, Banana;John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            "12345;Apple, Apple, Banana;;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX",
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MIX",
            "12345;Apple, Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;"
        )
        for order_data in invalid_order_data:
            self.assertRaises(ValueError, reader.read_order_data, order_data)


if __name__ == "__main__":
    unittest.main()
