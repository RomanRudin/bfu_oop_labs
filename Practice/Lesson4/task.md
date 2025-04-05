1. СОздать класс User:
    - id: int
    - login: str
    - password: str (хэшировать, но не обязательно (библиотека secrets)) - (не должна появляться в _str__ методе)
    - email: str - (необязательно)
    - address: str - (необязательно)

Если на Python:     dataclass
Если на C#, Java:   record
Если на C++:        реализовать функционал руками


2. Реализовать петтерн проектирования Repository ("репозиторий"):
    Создать интерфейс \ протокол IDataRepository[T] (Шаблонный), реализОВАТЬ механизм CRUD (Create, Read, Update, Delete) (SQL: INSERT, SELECT, UPDATE, DELETE):
    
    Read:
    - get_by_id(id: int) -> User
    - get_all(filter: str, sorting: str) -> List[User]
    Create:
    - add(user: User)
    Update
    - update(user: User)
    Delete
    - delete(user: User)


3. Реализовать интрефейс \ протокол IUserRepository(IDataRepository[User])
    - get_by_login(login: str) -> User


4. Реализовать класс DataRepository(IDataRepository) таким образом, чтобы данные хранились на жёстком диске (txt, csv, json, xml, bson, serialization...)


5. Реализовать класс UserRepository(DataRepository, IUserRepository)


6. Реализовать интерфейс \ протокол IAuthService:
    - sign_in(user: User) - авторизоваться в системе
    - sign_out(user: User) - выйти из учётной записи
    - is_authorized(user: User) -> bool
    - auto_sign_in(user: User)


7. Реализуем класс, поддерживающий интерфейс \ протокол IAuthService, который работает по типу куков (куки):
    - реализовать автоматическую реализацию
    - а саму систему на основе текстового файла на жёстком диске


8. Продемонстрировать работу приложения:
    - регистрация пользователя
    - смена пользователя
    - исправить данные профиля
    - выйти из учётной записи


9. Графический интерфейс по желанию.