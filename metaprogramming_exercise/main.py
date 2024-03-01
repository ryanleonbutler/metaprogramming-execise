from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """

    label: str
    precondition: Callable[[Any], bool] = None


# Record and supporting classes here


class Record:
    pass


# Usage of Record
class Person(Record):
    """
    A simple person record
    """

    name: str = Field(label="The name")
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)


class Named(Record):
    """
    A base class for things with names
    """

    name: str = Field(label="The name")


class Animal(Named):
    """
    An animal
    """

    habitat: str = Field(
        label="The habitat",
        precondition=lambda x: x in ["air", "land", "water"],
    )
    weight: float = Field(
        label="The animals weight (kg)", precondition=lambda x: 0 <= x
    )


class Dog(Animal):
    """
    A type of animal
    """

    bark: str = Field(label="Sound of bark")
