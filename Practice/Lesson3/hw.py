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


    #! Getters and setters must be in function
    @property
    def name(self) -> str:
        return self._name   
    @name.setter
    def name(self, name: str) -> None:
        # Before data change
        self._name = name
        # After data has chenged
        for listener in self.__data_changed_listeners:
            listener.on_property_changed(self, 'name')


    @property
    def email(self) -> str:
        return self._email   
    @name.setter
    def email(self, email: str) -> None:
        # Before data change
        if not all(listener.on_property_changing(self, 'email') for listener in self.__data_changed_listeners):
            raise Exception('The given value')
        self._email = email
        # After data has chenged
        for listener in self.__data_changed_listeners:
            listener.on_property_changed(self, 'email')

    def add_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        self.__data_changed_listeners.add(listener)
    def remove_data_changed_listeners(self, listener: PropertyChangedProtocol) -> None:
        self.__data_changed_listeners.remove(listener)

        
class MyDataChangedListener:
    def on_property_changed(self, obj: SupportsPropertyChangedProtocol, prop_name: str) -> None:
        print(f'A property "{prop_name}" changed')
    def on_property_changing(self, obj: SupportsPropertyChangedProtocol, prop_name: str, old_value, new_value) -> bool:
        match prop_name:
            case 'email':
                pass
            case 'name':
                pass
        return True


p = Person(name='Vasya', email='vasya@example.com')
listener1 = MyDataChangedListener()
p.add_data_changed_listeners(listener1)
p.name = 'Petya'
p.email = "Oleg"