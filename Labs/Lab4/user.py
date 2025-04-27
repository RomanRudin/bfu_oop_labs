from data_changed import ConsoleLogger
from data_changing import NameValidator
from protocols import DataChangingProtocol, DataChangedProtocol, PropertyChangedListenerProtocol, PropertyChangingListenerProtocol
from typing import Any

class User(DataChangedProtocol, DataChangingProtocol):
    name: str
    email: str
    __data_changed_listeners: list[DataChangedProtocol]
    __data_changing_listeners: list[DataChangingProtocol]


    def __init__(self, name: str, email: str) -> None:
        self.__data_changed_listeners = list()
        self.__data_changing_listeners = list()
        self._name = None
        self.name = name
        self._email = None
        self.email = email

    @property
    def name(self) -> str:
        return self._name   
    @name.setter
    def name(self, name: str) -> None:
        if not self._validate_property_changing('name', self.name, name):
            return
        self._name = name
        self._notify_property_changed('name')

    @property
    def email(self) -> str:
        return self._email   
    @email.setter
    def email(self, email: str) -> None:
        if not self._validate_property_changing('email', self.email, email):
            return
        self._email = email
        self._notify_property_changed('email')

    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener not in self.__data_changed_listeners:
            self.__data_changed_listeners.append(listener)
    
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener in self.__data_changed_listeners:
            self.__data_changed_listeners.remove(listener)
    
    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self.__data_changed_listeners:
            listener.on_property_changed(self, property_name)


    def add_property_changing_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener not in self.__data_changing_listeners:
            self.__data_changing_listeners.append(listener)
    
    def remove_property_changing_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener in self.__data_changed_listeners:
            self.__data_changing_listeners.remove(listener)
    
    def _validate_property_changing(self, property_name: str, old_value: Any, new_value: Any) -> bool:
        return all(listener.on_property_changing(self, property_name, old_value, new_value) for listener in self.__data_changing_listeners)
    
    def __str__(self) -> str:
        return f"User(name={self.name}, email={self.email})"

