from abc import ABC, ABCMeta, abstractmethod


#? Варинаты реализации интерфейсов в питоне:
'''
Abstract Class
'''
class MyAbstractClass(ABC):
    @abstractmethod
    def my_abstract_method(self):
        ...

class MyConcreteClass(MyAbstractClass):
    def my_abstract_method(self):
        pass



'''
Informal Interface
'''
class MyInformalInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return (hasattr(subclass, "my_method") and 
                callable(subclass.my_method))
    
# Supports MyInformalInterface
class MyConcreteClass2:
    def my_method(self) -> None:
        pass



'''
Formal Interface
'''
class MyFormalInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return (hasattr(subclass, "my_method") and 
                callable(subclass.my_method))

    @abstractmethod
    def my_method(self):
        ...

class MyConcreteClass3(MyFormalInterface):
    def my_method(self) -> None:
        pass



#? Но в питоне принято юзать протоколы, а не интерфейсы
'''
Protocol
'''
from typing import Protocol

class MyProtocol(Protocol):
    def my_method(Self):
        ...

class MyConcreteClass4:
    def my_method(self) -> None:
        pass



#? Использование:
def perform_my_method(item: MyProtocol) -> None:
    item.my_method()


#? Пример протокола:
class HasSizedClass:
    # Supports Sized protocol
    def __len__(self) -> int:
        return 10
    
obj = HasSizedClass()
# len() проверяет, поддерживает ли obj Sized протокол
print(len(obj))