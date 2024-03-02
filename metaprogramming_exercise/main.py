from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Callable


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """

    def __init__(
        self,
        label: str,
        precondition: Callable[[Any], bool] = lambda x: True,
        postcondition: Callable[[Any], bool] = lambda x: True,
    ):
        self.label = label
        self.precondition = precondition
        self.postcondition = postcondition


# Record and supporting classes here
class RecordMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
        attrs["fields"] = fields
        return super().__new__(cls, name, bases, attrs)


class Record(metaclass=RecordMeta):
    def __init__(self, **kwargs) -> None:
        for key, field in self.__getattribute__("fields").items():
            value = kwargs.get(key)
            if not field.precondition(value):
                raise TypeError(f"Invalid value for {field.label}")
            self.__setattr__(key, value, init=True)

    def __setattr__(self, key, value, init=False) -> None:
        if not init:
            raise AttributeError(f"Cannot set {key} after construction")
        super().__setattr__(key, value)


# Usage of Record
class Person(Record):
    """
    A simple person record
    """

    name: Field = Field(label="The name")
    age: Field = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: Field = Field(label="The person's income", precondition=lambda x: 0 <= x)

    def __str__(self) -> str:
        return dedent(
            f"""
              {self.__class__.__name__}(
              # The name
              name='{self.name}'

              # The person's age
              age={self.age}

              # The person's income
              income={self.income}
            )
        """
        ).strip()


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
    weight: float | int = Field(
        label="The animals weight (kg)",
        precondition=lambda x: 0 <= x,
        postcondition=lambda x: int(x),
    )
