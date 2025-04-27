from data_changed import ConsoleLogger
from data_changing import NameValidator, EmailValidator
from user import User

# Check lesson 3 .py


if __name__ == "__main__":
    user = User("Alice", "Example@stud.kantiana.ru")
    logger = ConsoleLogger()
    user.add_property_changed_listener(logger)
    
    name_validator = NameValidator()
    email_validator = EmailValidator()
    user.add_property_changing_listener(name_validator)
    user.add_property_changing_listener(email_validator)
    
    print("--- Valid changes ---")
    user.name = "Bob"     # Valid
    user.email = "Example@stud.kantiana.ru"         # Valid
    
    print()
    print("--- Invalid changes ---")
    user.name = -5         # Invalid
    user.name = "123"     # Invalid
    user.email = 150        # Invalid
    user.email = "A@mail.ru"       # Invalid
    
    print()
    print("--- Final values ---")
    print(f"Name: {user.name}, Email: {user.email}")