import re
from dataclasses import dataclass
from typing import Tuple, List, Dict


class AcceptableError(Exception):
    """
    Допустимая для работы системы ошибка
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return super().__str__()


@dataclass(frozen=True)
class Person:
    """
    Класс, содержащий данные о человеке.
    :var surname (str): Фамилия.
    :var name (str): Имя.
    :var patronymic (str, optional): Отчество.
    """
    surname: str
    name: str
    patronymic: str = None

    def __str__(self) -> str:
        """
        Формирует строку с информацией о ФИО.
        :return: Строка в формате "Фамилия Имя Отчество".
        """
        return f"{self.surname} {self.name}" + (f" {self.patronymic}" if self.patronymic is not None else "")


@dataclass(frozen=True)
class Address:
    """
    Класс, содержащий данные об адресе.
    :var country (str): Страна.
    :var region (str): Регион.
    :var town (str): Город.
    :var street (str): Улица.
    """
    country: str
    region: str
    town: str
    street: str

    def __str__(self) -> str:
        """
        Формирует строку с адресом.
        :return: Строка в формате "Страна. Регион. Город. Улица.".
        """
        return f"{self.country}. {self.region}. {self.town}. {self.street}."


class PhoneNumber:
    """
    Класс, представляющий телефонный номер.
    :var number: Телефонный номер в формате "+X-XXX-XXX-XX-XX".
    """

    @property
    def number(self) -> str:
        return self.__number

    @number.setter
    def number(self, phone_number: str) -> None:
        if not re.fullmatch(r"\+\d-\d{3}-\d{3}-\d{2}-\d{2}", phone_number):
            raise ValueError("Invalid phone number")
        self.__number = phone_number

    def __init__(self, phone_number: str):
        self.number = phone_number

    def __str__(self) -> str:
        """
        Возвращает строковое представление телефонного номера.
        :return: Телефонный номер.
        """
        return self.number


class Identify:
    """
    Класс, представляющий идентификатор заказа.
    :var identify (str): Идентификатор в формате "XXXXX".
    """

    @property
    def identify(self) -> str:
        return self.__identify

    @identify.setter
    def identify(self, identify: str) -> None:
        if not re.fullmatch(r"\d{5}", identify):
            raise ValueError("Invalid ident")
        self.__identify = identify

    def __init__(self, identify: str):
        self.identify = identify

    def __str__(self) -> str:
        """
        Возвращает строковое представление идентификатора.
        :return: Идентификатор.
        """
        return self.identify


class Priority:
    """
    Класс, представляющий приоритет заказа.
    :var priority: Приоритет заказа (LOW, MIDDLE, MAX).
    """
    PRIORITIES = dict(
        LOW=0,
        MIDDLE=1,
        MAX=2
    )

    @property
    def priority(self) -> int:
        return self.__priority

    @priority.setter
    def priority(self, priority: str) -> None:
        if priority not in self.PRIORITIES:
            raise ValueError("Invalid priority")
        self.__priority_name = priority
        self.__priority = self.PRIORITIES[priority]

    def __init__(self, priority: str):
        self.priority = priority

    def __str__(self) -> str:
        """
        Возвращает строковое представление приоритета.
        :return: Название приоритета.
        """
        return f"{self.__priority_name}"


class ProductsList:
    """
    Класс, представляющий список товаров заказа.
    :var products: Словарь с товарами и их количеством.
    """

    def __init__(self):
        self.products: Dict[str, int] = dict()

    def __str__(self) -> str:
        """
        Возвращает строковое представление списка товаров.
        :return: Строка с перечислением товаров.
        """
        products = []
        for key, value in self.products.items():
            products.append(key + (f" x{value}" if value > 1 else ""))
        return ", ".join(products)

    def add(self, product: str) -> None:
        """
        Добавляет товар в список.
        :param product: Название товара.
        """
        product = product.strip()
        if not product: raise ValueError("Invalid product")
        self.products[product] = self.products.get(product, 0) + 1


@dataclass(frozen=True)
class Order:
    """
    Класс, представляющий заказ.
    :var identify: Идентификатор заказа.
    :var customer: Клиент, сделавший заказ.
    :var address: Адрес доставки.
    :var phone: Телефон клиента.
    :var priority: Приоритет заказа.
    :var products: Список товаров в заказе.
    """
    identify: Identify
    customer: Person
    address: Address
    phone: PhoneNumber
    priority: Priority
    products: ProductsList

    def __lt__(self, other: "Order") -> bool:
        """
        Сравнивает заказы для сортировки.

        Заказы сравниваются по алфавитному порядку страны (все кроме России) или,
        если заказы с одной страны, по приоритету
        (страна с более высоким приоритетом меньше).

        :param other: Другой заказ для сравнения.
        :return: True, если текущий заказ менее приоритетен, чем другой.
        """
        if self.address.country == other.address.country:
            return self.priority.priority > other.priority.priority
        elif self.address.country == "Россия":
            return True
        elif other.address.country == "Россия":
            return False
        else: return self.address.country < other.address.country

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа.
        :return: Информация о заказе.
        """
        return f"""ORDER #{self.identify} [{self.priority} priority]
FOR {self.customer} (phone: {self.phone}) 
TO {self.address}
{self.products}"""


class OrdersReader:
    """
    Класс для чтения и обработки заказов из файла.
    :var exceptions: Список исключений с информацией
        об ошибочных строках.
    """

    def __init__(self):
        self.exceptions: List[Tuple[str, int, str]] = []

    def read_data_from_file(self, filename: str) -> List[Order]:
        """
        Читает заказы из файла.
        :param filename: Имя файла с заказами.
        :return Список успешно прочитанных заказов.
        """
        orders: List[Order] = []

        with open(filename, encoding="utf-8") as file:
            for order_data in file.readlines():
                try:
                    orders.append(self.read_order_data(order_data))
                except AcceptableError:
                    pass
        return orders

    def read_order_data(self, order_data: str) -> Order:
        """
        Читает данные одного заказа из строки.
        :param order_data: Строка с данными заказа.
        :return: Объект заказа.
        """
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
        try:
            address = self.read_address_data(address_data)
        except ValueError:
            code = 1
            self.exceptions.append((identify.identify, code, address_data if address_data else "no data"))
        try:
            phone = self.read_phone_data(phone_data)
        except ValueError:
            code = 2
            self.exceptions.append((identify.identify, code, phone_data if phone_data else "no data"))
        if code:
            raise AcceptableError("Invalid order data")

        return Order(identify=identify,
                     products=products,
                     customer=customer,
                     address=address,
                     phone=phone,
                     priority=priority)

    def read_identify_data(self, identify_data: str) -> Identify:
        """
        Читает и валидирует данные идентификатора.
        :param identify_data: Данные идентификатора.
        :return: Объект идентификатора.
        """
        return Identify(identify_data.strip())

    def read_products_data(self, products_data: str) -> ProductsList:
        """
        Читает и парсит данные о товарах.
        :param products_data: Строка с данными о товарах.
        :return: Список товаров.
        """
        products = ProductsList()
        for product in products_data.split(","):
            products.add(product)
        return products

    def read_customer_data(self, customer_data: str) -> Person:
        """
        Читает и валидирует данные клиента.
        :param customer_data: Данные клиента.
        :return: Объект клиента.
        """
        data = list(map(str.strip, customer_data.split()))
        if len(data) < 2 or len(data) > 3:
            raise ValueError("Invalid customer data")
        return Person(*data)

    def read_address_data(self, address_data: str) -> Address:
        """
        Читает и валидирует адрес.
        :param address_data: Данные адреса.
        :return: Объект адреса.
        """
        data = list(map(str.strip, address_data.split('.')))
        if len(data) != 4:
            raise ValueError("Invalid address data")
        return Address(*data)

    def read_phone_data(self, phone_data: str) -> PhoneNumber:
        """
        Читает и валидирует телефонный номер.
        :param phone_data: Данные телефонного номера.
        :return: Объект телефонного номера.
        """
        return PhoneNumber(phone_data.strip())

    def read_priority_data(self, priority_data: str) -> Priority:
        """
        Читает и валидирует данные приоритета.
        :param priority_data: Данные приоритета.
        :return: Объект приоритета.
        """
        return Priority(priority_data.strip())


def main():
    """
    Основная функция программы.
    Читает заказы из файла, сортирует их по приоритету и стране,
    сохраняет корректные заказы в файл `order_country.txt`, а
    некорректные данные записывает в файл `non_valid_orders.txt`.
    """
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


if __name__ == '__main__':
    main()
