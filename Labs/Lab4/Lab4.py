from typing import Protocol, TypeVar, Any
from dataclasses import dataclass

#TODO Check lesson 3 .py

T = TypeVar('T')

class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        ...


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        ...
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        ...


class Observable(DataChangedProtocol):
    def __init__(self):
        self._listeners: list[PropertyChangedListenerProtocol] = []
    
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener not in self._listeners:
            self._listeners.append(listener)
    
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._listeners:
            listener.on_property_changed(self, property_name)


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj: Any, property_name: str, 
                            old_value: Any, new_value: Any) -> bool:
        ...


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        ...
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        ...


class ValidatableObservable(Observable, DataChangingProtocol):
    def __init__(self):
        super().__init__()
        self._validators: list[PropertyChangingListenerProtocol] = []
    
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        if listener not in self._validators:
            self._validators.append(listener)
    
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        if listener in self._validators:
            self._validators.remove(listener)
    
    def _validate_property_change(self, property_name: str, 
                                old_value: Any, new_value: Any) -> bool:
        return all(
            validator.on_property_changing(self, property_name, old_value, new_value)
            for validator in self._validators
        )


class Person(ValidatableObservable):
    def __init__(self, name: str, age: int):
        super().__init__()
        self._name = name
        self._age = age
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if self._validate_property_change('name', self._name, value):
            old = self._name
            self._name = value
            self._notify_property_changed('name')
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        if self._validate_property_change('age', self._age, value):
            old = self._age
            self._age = value
            self._notify_property_changed('age')


class ConsoleLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        print(f"[LOG] Property {property_name} changed in {obj}")


class AgeValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: Any, property_name: str, 
                            old_value: int, new_value: int) -> bool:
        if property_name == 'age':
            if new_value < 0:
                print("Error: Age cannot be negative!")
                return False
            if new_value > 120:
                print("Error: Age cannot be more than 120!")
                return False
        return True

class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: Any, property_name: str, 
                            old_value: str, new_value: str) -> bool:
        if property_name == 'name':
            if not new_value.isalpha():
                print("Error: Name must contain only letters!")
                return False
            if len(new_value) < 2:
                print("Error: Name too short!")
                return False
        return True

if __name__ == "__main__":
    person = Person("Alice", 30)
    logger = ConsoleLogger()
    person.add_property_changed_listener(logger)
    
    age_validator = AgeValidator()
    name_validator = NameValidator()
    person.add_property_changing_listener(age_validator)
    person.add_property_changing_listener(name_validator)
    
    print("--- Valid changes ---")
    person.name = "Bob"     # Valid
    person.age = 35         # Valid
    
    print("\n--- Invalid changes ---")
    person.age = -5         # Invalid
    person.name = "123"     # Invalid
    person.age = 150        # Invalid
    person.name = "A"       # Invalid
    
    print("\n--- Final values ---")
    print(f"Name: {person.name}, Age: {person.age}")