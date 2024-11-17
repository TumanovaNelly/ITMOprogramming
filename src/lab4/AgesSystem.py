from typing import List, Union
from sortedcontainers import SortedDict


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.__name = name
        if age > 123: raise ValueError("Age must be less than or equal to 123.")
        self.__age = age

    def get_age(self) -> int:
        return self.__age

    def __lt__(self, other_person: 'Person') -> bool:
        return self.__name < other_person.__name if self.__age == other_person.__age else self.__age > other_person.__age

    def __str__(self) -> str:
        return f'{self.__name} ({self.__age})'


class AgeGroup:
    def __init__(self, min_age: int, max_age: Union[int, None]) -> None:
        self.__min_age = min_age
        self.__max_age = max_age
        self.__persons: List[Person] = list()

    def add_person(self, person: Person) -> None:
        self.__persons.append(person)

    def print(self) -> None:
        if len(self.__persons) == 0: return
        if self.__max_age is None:
            print(f'{self.__min_age}+: ', end="")
        else:
            print(f'{self.__min_age}-{self.__max_age}: ', end='')
        print(*sorted(self.__persons), sep=', ')


class Groups:
    def __init__(self, borders: List[int]):
        self.__borders = [-1] + sorted(borders)
        self.__groups = SortedDict()
        for i in range(len(self.__borders) - 1):
            self.__groups[self.__borders[i] + 1] = AgeGroup(self.__borders[i] + 1, self.__borders[i + 1])
        self.__groups[self.__borders[-1] + 1] = AgeGroup(self.__borders[-1] + 1, None)

    def add_person_to_group(self, person: Person) -> None:
        self.__groups[self.__find_first_less_or_equal(person.get_age())].add_person(person)

    def print(self):
        for group in reversed(self.__groups.values()):
            group.print()

    def __find_first_less_or_equal(self, number) -> int:
        left = 0
        right = len(self.__borders) - 1
        while left <= right:
            mid = right - (right - left) // 2
            if self.__borders[mid] + 1 > number:
                right = mid - 1
            else:
                left = mid + 1

        return self.__borders[right] + 1


def main():
    groups = Groups(list(map(int, input("Enter the age limits: ").split())))

    while True:
        line = input()
        if line == 'END': break
        name, age = line.split(',')
        name = name.strip()
        age = int(age)
        groups.add_person_to_group(Person(name, age))

    groups.print()


if __name__ == '__main__':
    main()
