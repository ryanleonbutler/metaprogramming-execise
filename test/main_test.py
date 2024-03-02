import unittest
from textwrap import dedent
from unittest import TestCase

from metaprogramming_exercise.main import Dog, Person


# Tests
class RecordTests(TestCase):
    def test_creation(self):
        Person(name="JAMES", age=110, income=24000.0)
        with self.assertRaises(TypeError):
            Person(name="JAMES", age=160, income=24000.0)
        with self.assertRaises(TypeError):
            Person(name="JAMES")
        with self.assertRaises(TypeError):
            Person(name="JAMES", age=-1, income=24000.0)
        with self.assertRaises(TypeError):
            Person(name="JAMES", age="150", income=24000.0)
        with self.assertRaises(TypeError):
            Person(name="JAMES", age="150", wealth=24000.0)

    def test_properties(self):
        james = Person(name="JAMES", age=34, income=24000.0)
        self.assertEqual(james.age, 34)
        with self.assertRaises(AttributeError):
            james.age = 32

    def test_str(self):
        james = Person(name="JAMES", age=34, income=24000.0)
        correct = dedent(
            """
        Person(
          # The name
          name='JAMES'

          # The person's age
          age=34

          # The person's income
          income=24000.0
        )
        """
        ).strip()
        self.assertEqual(str(james), correct)

    def test_dog(self):
        mike = Dog(name="mike", habitat="land", weight=50.0, bark="ARF")
        self.assertEqual(mike.weight, 50)


if __name__ == "__main__":
    unittest.main()
