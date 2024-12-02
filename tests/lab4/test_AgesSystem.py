import unittest
from src.lab4.AgesSystem import Person, AgeGroup, Groups


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.groups = Groups([18, 30, 50])

    def test_add_person_to_group(self):
        person1 = Person("Alice", 35)
        person2 = Person("Bob", 14)
        person3 = Person("Charlie", 15)
        person4 = Person("Dave", 60)

        self.groups.add_person_to_group(person1)
        self.groups.add_person_to_group(person2)
        self.groups.add_person_to_group(person3)
        self.groups.add_person_to_group(person4)

        self.assertEqual(len(self.groups._Groups__groups[0]._AgeGroup__persons), 2)  # 0-18
        self.assertEqual(len(self.groups._Groups__groups[19]._AgeGroup__persons), 0)  # 19-30
        self.assertEqual(len(self.groups._Groups__groups[31]._AgeGroup__persons), 1)  # 31-50
        self.assertEqual(len(self.groups._Groups__groups[51]._AgeGroup__persons), 1)  # 51+

    def test_add_person_with_invalid_age(self):
        with self.assertRaises(ValueError):
            Person("InvalidPerson", 124)

    def test_group_print(self):
        person1 = Person("Alice", 75)
        person2 = Person("Bob", 15)
        person3 = Person("Charlie", 15)
        person4 = Person("Dave", 60)

        self.groups.add_person_to_group(person1)
        self.groups.add_person_to_group(person2)
        self.groups.add_person_to_group(person3)
        self.groups.add_person_to_group(person4)

        expected_output = (
            "51+: Alice (75), Dave (60)\n"
            "0-18: Bob (15), Charlie (15)\n"
        )

        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.groups.print()
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue().strip(), expected_output.strip())

    def test_empty_group_print(self):
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.groups.print()
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue().strip(), "")


if __name__ == "__main__":
    unittest.main()
