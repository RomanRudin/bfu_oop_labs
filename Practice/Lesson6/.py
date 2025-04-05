import json
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol


@dataclass
class User:
    id: int
    name: str
    email: str
    address: str

@dataclass
class Product:
    name: str
    amount: int
    price: float
    description: str


#! Отвратитлеьное решение:
class UserSerializer:
    def serialize(self, user: User, fmt: str) -> str:
        match fmt:
            case 'xml':
                ...
            case 'json':
                data = {
                    "id": user.id, 
                    "name": user.name, 
                    "email": user.email, 
                    "address": user.address
                    }
                return json.dumps(data)
            case _:
                raise ValueError('Not supported format')
            
user = User(...)
serializer = UserSerializer()
print (serializer.serialize(user, 'json'))


#! Всё ещё отвратитлеьное решение:
class UserSerializer:
    def serialize(self, user: User, fmt: str) -> str:
        match fmt:
            case 'xml':
                return self._serialize_to_xml(user)
            case 'json':
                return self._serialize_to_json(user)
            case _:
                raise ValueError('Not supported format')
    def _serialize_to_json(self, user: User) -> str:
        data = {
            "id": user.id, 
            "name": user.name, 
            "email": user.email, 
            "address": user.address
            }
        return json.dumps(data)

    def _serialize_to_xml(self, user: User) -> str:
        ...
# Or just simply without any class serializer, 
# just using three functions


#! Плохое решение:
class UserSerializer:
    def serialize(self, user: User, fmt: str) -> str:
        serializer = self._get_serializer(fmt)
        return serializer(user)
    
    def _get_serializer(self, fmt: str) -> callable:
        match fmt:
            case 'xml':
                return self._serialize_to_xml
            case 'json':
                return self._serialize_to_json
            
    def _serialize_to_json(self, user: User) -> str:
        data = {
            "id": user.id, 
            "name": user.name, 
            "email": user.email, 
            "address": user.address
            }
        return json.dumps(data)

    def _serialize_to_xml(self, user: User) -> str:
        ...


#! Хорошее решение, но не идеальное. Красивое, гибкое, но работает только с User:
#? serializers.py    
class UserSerializer(ABC):
    @abstractmethod
    def serialize(self, user: User) -> str:
        ...

    @abstractmethod
    def get_format(self) -> str:
        ...


class JSONUserSerializer(UserSerializer):
    def serialize(self, user: User) -> str:
        data = {
            "id": user.id, 
            "name": user.name, 
            "email": user.email, 
            "address": user.address
            }
        return json.dumps(data)
    
    def get_format(self) -> str:
        return 'json'
    

class XMLUserSerializer(UserSerializer):
    def serialize(self, user: User) -> str:
        ...

    def get_format(self) -> str:
        return 'xml'
    

class UserSerializerFabric:
    def __init__(self) -> None:
        self.serializers: list[UserSerializer] = []

    def register_serializer(self, serializer: UserSerializer) -> None:
        self.serializers.append(serializer)

    def get_serializer(self, fmt: str) -> UserSerializer:
        for serializer in self.serializers:
            if serializer.get_format() == fmt:
                return serializer
        raise ValueError('Not Supported format')

#? config.py    
# from serialisers import UserSerializerFabric, JSONUserSerializer, XMLUserSerializer
serializer_fabric = UserSerializerFabric()
serializer_fabric.register_serializer(JSONUserSerializer)
serializer_fabric.register_serializer(XMLUserSerializer)

#? data.py    
# class User:
    # ...

#? main.py    
# from data import User
# from config import serializer_fabric
user = User(...)
serializer = serializer_fabric.get_serializer('json')
serializer.serialize()



#! Самое гибкое и красивое решение:
class Serializer(ABC):
    @abstractmethod
    def open(self):
        ...
    
    @abstractmethod
    def add_property(self, prop_name: str, prop_value) -> None:
        ...

    @abstractmethod
    def to_str(self) -> str:
        ...

        
class SerializerFabric:
    def __init__(self) -> None:
        self.serializers: list[Serializer] = []

    def register_serializer(self, serializer: Serializer) -> None:
        self.serializers.append(serializer)

    def get_serializer(self, fmt: str) -> Serializer:
        for serializer in self.serializers:
            if serializer.get_format() == fmt:
                return serializer
        raise ValueError('Not Supported format')


class Serializable(Protocol):
    def serialize(self, serializer: Serializer) -> str:
        ...


# Fields can be marked with decorators (are they serializable and with which name)
@dataclass
class User:
    id: int
    name: str
    email: str
    address: str

    def serialize(self, serializer: Serializer) -> str:
        serializer.open()
        serializer.add_property('id', self.id)
        serializer.add_property('name, surname', self.name)
        serializer.add_property('gmail', self.email)
        return serializer.to_str()


@dataclass
class Product:
    name: str
    amount: int
    price: float
    description: str

    def serialize(self, serializer: Serializer) -> str:
        ...


# Can be done like a context manager and will be wonderfull, but not today
class JSONSerializer(Serializer):
    def open(self):
        self._data = []
    
    def add_property(self, prop_name: str, prop_value) -> None:
        self._data[prop_name] = prop_value        

    def to_str(self) -> str:
        json.dumps(self._data)


        
#? config.py    
# from serialisers import UserSerializerFabric, JSONUserSerializer, XMLUserSerializer
serializer_fabric = SerializerFabric()
serializer_fabric.register_serializer(JSONSerializer)

current_format = 'json'

#? data.py    
# class User:
    # ...

#? main.py    
# from data import User, Product
# from config import serializer_fabric
serializer = serializer_fabric.get_serializer(current_format)
user = User(...)
print(user.serialize(serializer))
product = Product(...)
print(product.serialize(serializer))