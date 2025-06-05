from typing import Protocol, Optional, TypeVar, List, Dict, Sequence, Any
from user import User
from data_repository import DataRepository, DataRepositoryProtocol

LOGIN = "login"


class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]: 
        ...



class UserRepository(DataRepository[User], UserRepositoryProtocol):
    def __init__(self, file_path: str = 'Labs/Lab5/data/users.json') -> None:
        super().__init__(file_path, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for item in self._load_data():
            if item[LOGIN] == login: #! TODO
                return User(**item)
        return None