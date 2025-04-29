from user_repository import UserRepository
from user import User
from auth_service import AuthService


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