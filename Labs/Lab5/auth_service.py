from typing import Protocol, Optional
import os, json
from user_repository import UserRepositoryProtocol
from user import User


class AuthServiceProtocol(Protocol):
    def sign_in(user: User) -> bool:
        ...
    def sign_out(user: User) -> None:
        ...
    @property
    def is_authorized(user: User) -> bool:
        ...
    @property
    def current_user(user: User) -> Optional[User]:
        ...



class AuthService(AuthServiceProtocol):
    def __init__(self, user_repo: UserRepositoryProtocol, session_file: str = 'Labs/Lab5/data/session.json') -> None:
        self.SESSION_FILE = session_file
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
        if not self._current_user:
            return
        try:
            with open(self.SESSION_FILE, 'w') as file:
                json.dump({'user_id': self._current_user.id}, file)
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError

    def sign_in(self, login: str, password: str) -> bool: #! TODO
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
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user