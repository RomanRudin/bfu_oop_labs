from user_repository import UserRepository
from user import User
from auth_service import AuthService
from typing import Optional
COLORING = "\033[{}m{}\033[0m"

def text_color(text: str) -> str:
    return COLORING.format(33, text)
def beautiful_bool(value: bool) -> str:
    return COLORING.format(32 if value else 31, "True" if value else "False")
def beautiful_none(value: Optional[str]) -> str:
    return COLORING.format(33 if value is None else 32, value)



if __name__ == "__main__":
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    users = [
        User(0, "admin", "secret", "Administrator", "admin@stud.kantiana.com"),
        User(1, "user1", "password", "Ishanov Sergey Alexandrovich", "example@stud.kantiana.com", "Alexandra Nevskogo 14a")
    ]
    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)

    print(f"1. Trying automatic sign in:")
    print(f"Is authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Current user:   {beautiful_none(auth_service.current_user)}")
    print()

    print("2. Trying sign in with wrong password:")
    print(f"Success:        {beautiful_bool(auth_service.sign_in("admin", "wrongpass"))}")
    print(f"Is Authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Current user:   {beautiful_none(auth_service.current_user)}")
    print()

    print("3. Successful sign in:")
    print(f"Success:        {beautiful_bool(auth_service.sign_in("admin", "secret"))}")
    print(f"is authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Current user:   {beautiful_none(auth_service.current_user)}")
    print()

    print("4. Signing out:")
    auth_service.sign_out()
    print(f"Is authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Is Authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Current user:   {beautiful_none(auth_service.current_user)}")
    print()

    print("5. Authorization after signing out:")
    print(f"Success:        {beautiful_bool(auth_service.sign_in("user1", "password"))}")
    print(f"is authorized:  {beautiful_bool(auth_service.is_authorized)}")
    print(f"Current user:   {beautiful_none(auth_service.current_user)}")
    print()

    print("6. Updating user data:")
    user = user_repo.get_by_login("user1")
    user.name = "Rudin Roman"
    user_repo.update(user)
    print("Updated user:")
    print(COLORING.format(32, user_repo.get_by_id(user.id)))
    user.name = "Ishanov Sergey Alexandrovich"
    user_repo.update(user)