from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, Optional, TypeVar, List, Dict, Sequence, Any
import os, json
from functools import total_ordering


T = TypeVar('T')

class SupportUserFormatProtocol:
    id: int
    login: str
    password: str


@dataclass
@total_ordering
class User:
    id: int
    login: str
    password: str = field(repr=False, compare=False)
    name: str = field(compare=False)
    email: Optional[str] = field(default=False, compare=False)
    address: Optional[str] = field(default=False, compare=False)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.name.lower() < other.name.lower()


class DataRepositoryProtocol(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        ...
    def get_by_id(self, id: int) -> Optional[T]:
        ...
    def add(self, item: T) -> None:
        ...
    def update(self, item:T ) -> None:
        ...
    def delete(self, item: T) -> None:
        ...



class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]: 
        ...



class DataRepository(DataRepositoryProtocol[T]):
    def __init__(self, file_path: str, entity_type: type):
        self.file_path = file_path
        self.entity_type = entity_type
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def _load_data(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all(self) -> Sequence[T]:
        return [self.entity_type(**item) for item in self._load_data()]

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._load_data():
            if item['id'] == id:
                return self.entity_type(**item)
        return None

    def add(self, item: T) -> None:
        data = self._load_data()
        data.append(item.__dict__)
        self._save_data(data)

    def update(self, item: T) -> None:
        data = self._load_data()
        for i, entry in enumerate(data):
            if entry['id'] == item.id:
                data[i] = item.__dict__
                break
        self._save_data(data)

    def delete(self, item: T) -> None:
        data = self._load_data()
        data = [entry for entry in data if entry['id'] != item.id]
        self._save_data(data)



class UserRepository(DataRepository[User], UserRepositoryProtocol):
    def __init__(self, file_path: str = 'Lans/Lab5/data/users.json'):
        super().__init__(file_path, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for item in self._load_data():
            if item['login'] == login:
                return User(**item)
        return None



class AuthServiceProtocol(Protocol):
    def sign_in(user: User) -> bool:
        ...
    def sign_out(user: User) -> None:
        ...
    @property
    def is_authorized(user: User) -> bool:
        ...
    @property
    def auto_sign_in(user: User) -> Optional[User]:
        ...



class AuthService:
    SESSION_FILE = 'Lans/Lab5/data/session.json'

    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo
        self._current_user: Optional[User] = None
        self._load_session()

    def _load_session(self) -> None:
        try:
            with open(self.SESSION_FILE, 'r') as f:
                session = json.load(f)
                self._current_user = self.user_repo.get_by_id(session['user_id'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self._current_user = None

    def _save_session(self) -> None:
        if self._current_user:
            with open(self.SESSION_FILE, 'w') as f:
                json.dump({'user_id': self._current_user.id}, f)

    def sign_in(self, login: str, password: str) -> bool:
        user = self.user_repo.get_by_login(login)
        if user and user.password == password:
            self._current_user = user
            self._save_session()
            return True
        return False

    def sign_out(self) -> None:
        self._current_user = None
        try:
            os.remove(self.SESSION_FILE)
        except FileNotFoundError:
            pass

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user

if __name__ == "__main__":
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    users = [
        User(1, "admin", "secret", "Administrator", "admin@example.com"),
        User(2, "user1", "pass123", "John Doe", "john@example.com", "Street 123")
    ]
    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)

    print("1. Попытка автоматической авторизации:")
    print(f"Авторизован: {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}\n")

    print("2. Авторизация с неверными данными:")
    print("Успешно:", auth_service.sign_in("admin", "wrongpass"))
    print(f"Авторизован: {auth_service.is_authorized}\n")

    print("3. Успешная авторизация:")
    print("Успешно:", auth_service.sign_in("admin", "secret"))
    print(f"Авторизован: {auth_service.is_authorized}")
    print(f"Текущий пользователь: {auth_service.current_user}\n")

    print("4. Выход из системы:")
    auth_service.sign_out()
    print(f"Авторизован: {auth_service.is_authorized}\n")

    print("5. Повторная авторизация после выхода:")
    print("Успешно:", auth_service.sign_in("user1", "pass123"))
    print(f"Текущий пользователь: {auth_service.current_user}\n")

    print("6. Обновление данных пользователя:")
    user = user_repo.get_by_login("user1")
    if user:
        user.name = "John Smith"
        user_repo.update(user)
        print("Обновленный пользователь:", user_repo.get_by_id(user.id))