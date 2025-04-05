'''
Реализация не через интерфейсы или протоколы
'''
class Person:
    name: str
    email: str

    def __init__(self, name: str, email: str) -> None:
        self.__data_changed_listeners = set()
        self.name = name
        self.email = email

    #? Нам обязательны геттер и сеттер либо система работы через getattr, setattr чтобы создавать события
    # Getter
    @property
    def name(self) -> str:
        return self._name   
    # Setter
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        for listener in self.__data_changed_listeners:
            listener.on_property_changed(self, 'name')


    def add_data_changed_listeners(self, listener) -> None:
        self.__data_changed_listeners.add(listener)
    def remove_data_changed_listeners(self, listener) -> None:
        self.__data_changed_listeners.remove(listener)


class MyDataChangedListener:
    def on_property_changed(self, obj, prop_name: str) -> None:
        print(f'A property "{prop_name}" changed')


p = Person(name='Vasya', email='vasya@example.com')
listener = MyDataChangedListener()
p.add_data_changed_listeners(listener)
p.name = 'Petya'
p.name = "Oleg"




'''
Реализация через протоколы
'''
from typing import Protocol
class PropertyChangedProtocol(Protocol):
    def on_property_changed(self, obj: 'SupportsPropertyChangedProtocol', prop_name: str) -> None:
        ...
        
class SupportsPropertyChangedProtocol(Protocol):
    def add_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        ...
    def remove_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        ...


class Person:
    name: str
    email: str
    __data_changed_listeners: set[SupportsPropertyChangedProtocol]


    def __init__(self, name: str, email: str) -> None:
        self.__data_changed_listeners = set()
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        return self._name   
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        # After data chenged
        for listener in self.__data_changed_listeners:
            listener.on_property_changed(self, 'name')


    def add_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        self.__data_changed_listeners.add(listener)
    def remove_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        self.__data_changed_listeners.remove(listener)

        
class MyDataChangedListener:
    def on_property_changed(self, obj: SupportsPropertyChangedProtocol, prop_name: str) -> None:
        print(f'A property "{prop_name}" changed')

        
p = Person(name='Vasya', email='vasya@example.com')
listener = MyDataChangedListener()
p.add_data_changed_listeners(listener)
p.name = 'Petya'
p.name = "Oleg"