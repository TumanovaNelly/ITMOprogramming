from dataclasses import dataclass
import re
from typing import Tuple, List, Dict


class ExpectedError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return super().__str__()


@dataclass(frozen=True)
class Person:
    surname: str
    name: str
    patronymic: str = None

    def __str__(self):
        return f"{self.surname} {self.name}" + (f" {self.patronymic}" if self.patronymic is not None else "")


@dataclass(frozen=True)
class Address:
    country: str
    region: str
    town: str
    street: str

    def __str__(self):
        return f"{self.country}. {self.region}. {self.town}. {self.street}."


class PhoneNumber:
    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, phone_number: str):
        if not re.fullmatch("\+\d-\d{3}-\d{3}-\d{2}-\d{2}", phone_number):
            raise ValueError("Invalid phone number")
        self.__number = phone_number

    def __init__(self, phone_number):
        self.number = phone_number

    def __str__(self):
        return self.number


class Identify:
    @property
    def identify(self) -> str:
        return self.__identify

    @identify.setter
    def identify(self, identify: str):
        if not re.fullmatch("\d{5}", identify):
            raise ValueError("Invalid ident")
        self.__identify = identify

    def __init__(self, identify):
        self.identify = identify

    def __str__(self):
        return self.identify


class Priority:
    PRIORITIES = dict(
        LOW=0,
        MIDDLE=1,
        MAX=2
    )

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority: str):
        if priority not in self.PRIORITIES:
            raise ValueError("Invalid priority")
        self.__priority_name = priority
        self.__priority = self.PRIORITIES[priority]

    def __init__(self, priority: str):
        self.priority = priority

    def __str__(self):
        return f"{self.__priority_name}"


class ProductsList:
    def __init__(self):
        self.products: Dict[str, int] = dict()

    def __str__(self) -> str:
        products = []
        for key, value in self.products.items():
            products.append(key + (f" x{value}" if value > 1 else ""))
        return ", ".join(products)

    def add(self, product: str) -> None:
        self.products[product] = self.products.get(product, 0) + 1


@dataclass(frozen=True)
class Order:
    identify: Identify
    customer: Person
    address: Address
    phone: PhoneNumber
    priority: Priority
    products: ProductsList

    def __lt__(self, other):
        return self.priority.priority > other.priority.priority \
            if self.address.country == other.address.country \
            else self.address.country < other.address.country

    def __str__(self):
        return f"""ORDER #{self.identify} [{self.priority} priority]
FOR {self.customer} (phone: {self.phone}) 
TO {self.address}
{self.products}"""


class OrdersReader:
    def __init__(self):
        self.exceptions: List[Tuple[str, int, str]] = []

    def read_data_from_file(self, filename: str) -> List[Order]:
        orders: List[Order] = []

        with open(filename, encoding="utf-8") as file:
            for order_data in file.readlines():
                try:
                    orders.append(self.read_order_data(order_data))
                except ExpectedError:
                    pass
        return orders

    def read_order_data(self, order_data: str) -> Order:
        (identify_data,
         products_data,
         customer_data,
         address_data,
         phone_data,
         priority_data) = map(str.strip, order_data.split(";"))

        identify = self.read_identify_data(identify_data)
        products = self.read_products_data(products_data)
        customer = self.read_customer_data(customer_data)
        priority = self.read_priority_data(priority_data)

        address, phone = None, None
        code = 0
        try: address = self.read_address_data(address_data)
        except ValueError:
            code = 1
            self.exceptions.append((identify.identify, code, address_data if address_data else "no data"))
        try: phone = self.read_phone_data(phone_data)
        except ValueError:
            code = 2
            self.exceptions.append((identify.identify, code, phone_data if phone_data else "no data"))
        if code: raise ExpectedError("Invalid order data")

        return Order(identify=identify,
                      products=products,
                      customer=customer,
                      address=address,
                      phone=phone,
                      priority=priority)

    def read_identify_data(self, identify_data: str) -> Identify:
        return Identify(identify_data.strip())

    def read_products_data(self, products_data: str) -> ProductsList:
        products = ProductsList()
        for product in map(str.strip, products_data.split(",")):
            products.add(product)
        return products

    def read_customer_data(self, customer_data: str) -> Person:
        data = list(map(str.strip, customer_data.split()))
        if len(data) < 2 or len(data) > 3:
            raise ValueError("Invalid customer data")
        return Person(*data)

    def read_address_data(self, address_data: str) -> Address:
        data = list(map(str.strip, address_data.split('.')))
        if len(data) != 4:
            raise ValueError("Invalid address data")
        return Address(*data)

    def read_phone_data(self, phone_data: str) -> PhoneNumber:
        return PhoneNumber(phone_data.strip())

    def read_priority_data(self, priority_data: str) -> Priority:
        return Priority(priority_data.strip())


if __name__ == '__main__':
    reader = OrdersReader()
    orders = reader.read_data_from_file("orders.txt")

    with open("order_country.txt", "w", encoding="utf-8") as file:
        for order in sorted(orders):
            print(order.identify, order.products,
                  order.customer, order.address,
                  order.phone, order.priority,
                  sep=';', file=file)

    with open("non_valid_orders.txt", "w", encoding="utf-8") as file:
        for error in reader.exceptions:
            print(*error, sep=';', file=file)