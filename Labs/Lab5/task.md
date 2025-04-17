## Лабораторная работа 5 (система авторизации)

Создать систему авторизации и хранения информации о пользователях приложении, не зависящую от
источника данных, поддерживающую автоматическую авторизацию пользователей, реализующую взаимодействие с источником данных
обобщенным образом.

Реализуем через паттерн репозиторий

1. Создать класс User с атрибутами:
    id: int
    name: str
    login: str
    password: str (поле не должно показываться при строковом представлении класс)
    email: str (сделать поле необязательным)
    address: str (сделать поле необязательным)

- Сделать, чтобы коллекция классов User умела сортироваться по полю name.
- Реализовать через dataclass или через аналоги в других языках (C# и Java: record)

2. Создать интерфейс / протокол IDataRepository[T] / DataRepsitoryProtocol[T] для системы CRUD = Create, Read, Update, Delete для произвольного типа данных:
  - get_all(self) -> Sequence[T]
  - get_by_id(self, id: int) -> T | None
  - add(self, item: T) -> None
  - update(self, item: T) -> None
  - delete(self, item: T) -> None

2. Создать интерфейс / протокол IUserRepository ( IDataRepository[User]) / UserRepositoryProtocol (DataRepsitoryProtocol[User]) для взаимодействия с типом данных User
 - get_by_login(self, login: str) -> User | None

3. Создать реализацию  DataRepository[T](IDataRepository[T) / DataRepitoryProtocol[T] supports IDataRepsitoryProtocol[T]
  - Осуществляет хранение данных в файле
  - Можно использовать сторонние сериализаторы (Напр., pickle, json, xml)

4. Создать реализацию UserRepository(IUserRepository) / supports UserRepositoryProtocol на основе DataRepository[T](IDataRepository[T) / DataRepitoryProtocol[T]

5. Создать интерфейс / протокол IAuthService / AuthServiceProtocol
  - sign_in(self, user: User) -> None
  - sign_out(selg, user: User) -> None
  - is_authorized -> bool
  - current_user  -> User

6. Создать реализацию IAuthService / AuthServiceProtocol, которая хранит информацию о текущем пользователе в файле и автоматически авторизует пользователя при повторном заходе в программу в случае наличия соответствующей записи в файле

7. Продемонстрировать работу реализованной системы
 - добавление пользователя
 - редактирование свойств пользователя
 - авторизация пользователя
 - смена текущего пользователя
 - авторматическая авторизация при повторном заходе в программу