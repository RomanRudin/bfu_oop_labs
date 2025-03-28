from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Protocol

@dataclass
class User:
    id: int
    login: str
    password: str = field(repr=False, compare=False)
    name: str = field(compare=False)
    email: Optional[str] = field(default=False, compare=False)
    address: Optional[str] = field(default=False, compare=False)

@dataclass
class Product:
    id: int
    name: str
    price: float

@dataclass 
class Order:
    id: int
    number: str
    date: datetime
    user_id: int

@dataclass
class OrderProducts:
    id: int
    order_id: int
    product_id: int
    count: int
    order: Order
    product: Product

# T = TypeVar('T')

# CRUD - create, read, update, delete
class DataRepositoryPrototcol[T](Protocol):
    def get_all(self) -> list[T]:
        ...

    def get_by_id(self, id: int) -> Optional[T]:
        ...

    def add(self, obj: T) -> None:
        ...

    def update(self, obj: T) -> None:
        ...

    def delete(self, obj: T) -> None:
        ...

class UserRepositoryProtocol(DataRepositoryPrototcol[User]):
    def get_by_login(self, login: str) -> Optional[User]:
        ...

class ProductRepositoryProtocol(DataRepositoryPrototcol[Product]):
    def get_by_name(self, name: str) -> Optional[Product]:
        ...

class DataRepository[T]:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_all(self) -> list[T]:
        data: list[T] = []
        with open(self.file_path, 'rb') as file:
            for line in file:
                #  restore T
                item: T = None
                data.append(item)

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self.get_all():
            if item.id == id:
                return item
        return None
    
    ...


# Supports UserRepositoryProtocol
class UserRepository(DataRepository[User]):
    def get_by_login(self, login: str) -> Optional[User]:
        for item in self.get_all():
            if item.login == login:
                return item
        
        return None
    

class MemoryDataRepository[T](DataRepositoryPrototcol):
    def __init__(self, data: list[T]) -> None:
        self.data: list[T] = data

    def get_all(self) -> list[T]:
        return self.data
    

class MemoryUserRepository(MemoryDataRepository[User]):
    def get_by_login(self, login: str) -> Optional[User]:
        for item in self.get_all():
            if item.login == login:
                return item
        return None
    
def get_users(user_repository: DataRepositoryPrototcol) -> list[User]:
    return user_repository.get_all()


#  Extra
class SourceService[T: DataRepositoryPrototcol]:
    def get_repo_instance(repo_type: type) -> DataRepositoryPrototcol:
        ...

...



if __name__ == "__main__":
    user_repository = MemoryUserRepository()
    users = get_users(user_repository)
    ...