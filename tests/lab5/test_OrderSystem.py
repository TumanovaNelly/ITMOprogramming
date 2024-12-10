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
        with self.assertRaises(ValueError):
            PhoneNumber("123456")


class TestIdentify(unittest.TestCase):
    def test_valid_identify(self):
        identify = Identify("12345")
        self.assertEqual(str(identify), "12345")

    def test_invalid_identify(self):
        with self.assertRaises(ValueError):
            Identify("abc")


class TestPriority(unittest.TestCase):
    def test_valid_priority(self):
        priority = Priority("MAX")
        self.assertEqual(str(priority), "MAX")
        self.assertEqual(priority.priority, 2)

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            Priority("INVALID")


class TestProductsList(unittest.TestCase):
    def test_add_products(self):
        products = ProductsList()
        products.add("Apple")
        products.add("Banana")
        products.add("Apple")
        self.assertEqual(str(products), "Apple x2, Banana")


class TestOrder(unittest.TestCase):
    def test_order_comparison(self):
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
            address=Address("Canada", "Ontario", "Toronto", "Queen Street"),
            phone=PhoneNumber("+1-987-654-32-10"),
            priority=Priority("MIDDLE"),
            products=ProductsList()
        )

        self.assertLess(order2, order1)


class TestOrdersReader(unittest.TestCase):
    def test_read_valid_order_data(self):
        reader = OrdersReader()
        order_data = (
            "12345;Apple, Banana;Doe John;USA. California. Los Angeles. Main Street;+1-123-456-78-90;MAX"
        )
        order = reader.read_order_data(order_data)
        self.assertEqual(order.identify.identify, "12345")
        self.assertEqual(str(order.customer), "Doe John")
        self.assertEqual(str(order.address), "USA. California. Los Angeles. Main Street.")
        self.assertEqual(str(order.phone), "+1-123-456-78-90")
        self.assertEqual(str(order.priority), "MAX")
        self.assertEqual(str(order.products), "Apple, Banana")

    def test_read_invalid_order_data(self):
        reader = OrdersReader()
        invalid_order_data = (
            "12345;Apple, Banana;Doe John;USA. California. Los Angeles;+1-123-456-78-90;MAX"
        )
        with self.assertRaises(AcceptableError):
            reader.read_order_data(invalid_order_data)


if __name__ == "__main__":
    unittest.main()
