from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Field(Generic[T]):
    """Defines a generic field with a label and pre/post conditions.

    Args:
        label (str): The label for the field.
        precondition (Callable[[Any], bool]): A callable that takes a value
            and returns a bool indicating if the precondition is satisfied.
            Defaults to a lambda that always returns True.
        postcondition (Callable[[Any], bool]): A callable that takes a value
            and returns a bool indicating if the postcondition is satisfied.
            Defaults to a lambda that always returns True.

    Attributes:
        label (str): The label for the field.
        precondition (Callable[[Any], bool]): The precondition callable.
        postcondition (Callable[[Any], bool]): The postcondition callable.
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


class RecordMeta(type):
    """Metaclass that extracts Field attributes to build the fields property.

    Attributes:
        fields (dict): Dict mapping field names to Field instances extracted
            from Record subclass attributes. Added to subclass dict.
    """

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

    @property
    def fields_list(self):
        return list(self.__getattribute__("fields").keys())

    def __setattr__(self, key, value, init=False) -> None:
        if not init:
            raise AttributeError(f"Cannot set {key} after construction")
        super().__setattr__(key, value)


# Usage of Record
class Person(Record):
    """Base class for defining records with typed fields.

    Records are immutable after construction. Fields are defined as
    class attributes typed with Field subclasses.

    Keyword Args:
        Field values to initialize

    Attributes:
        fields (dict): Dict mapping field names to Field instances

    Raises:
        TypeError: If invalid field value that fails field precondition
    """

    name: Field[str] = Field(label="The name")
    age: Field[int] = Field(
        label="The person's age", precondition=lambda x: 0 <= x <= 150
    )
    income: Field[float] = Field(
        label="The person's income", precondition=lambda x: 0 <= x
    )

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
    """A base class for things with names.

    Attributes:
        name (str): The name of the object. This is specified as a required
            Field with the label "The name".
    """

    name: Field[str] = Field(label="The name")


class Animal(Named):
    """An animal with a name, habitat, and weight.

    Attributes:
        name (str): The name of the animal
        habitat (str): The habitat of the animal (air, land, water)
        weight (float): The weight of the animal in kg (> 0)
    """

    habitat: Field[str] = Field(
        label="The habitat",
        precondition=lambda x: x in ["air", "land", "water"],
    )
    weight: Field[float] = Field(
        label="The animals weight (kg)", precondition=lambda x: 0 <= x
    )


class Dog(Animal):
    """A dog with a name, habitat, weight, and bark sound.

    Attributes:
        name (str): The name of the dog
        habitat (str): The habitat of the dog (air, land, water)
        weight (float|int): The weight of the dog in kg (> 0)
        bark (str): The sound of the dog's bark
    """

    bark: Field[str] = Field(label="Sound of bark")
    weight: Field[float | int] = Field(
        label="The animals weight (kg)",
        precondition=lambda x: 0 <= x,
        postcondition=lambda x: isinstance(int(x), (float, int)),
    )
