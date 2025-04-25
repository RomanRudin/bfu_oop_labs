from typing import Any
from protocols import PropertyChangingListenerProtocol, DataChangingProtocol, COLORING

class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name != 'name':
            return True
        if not isinstance(new_value, str):
            print(COLORING.format(31, "Error: Name must be a string!"))
            return False
        if not new_value.isalpha():
            print(COLORING.format(31, "Error: Name must contain only letters!"))
            return False
        if len(new_value) < 2:
            print(COLORING.format(31, "Error: Name too short!"))
            return False
        print(COLORING.format(33, f"Name of {str(obj)} is changing from {old_value} to {new_value}"))
        return True
    

class EmailValidator(PropertyChangingListenerProtocol):
    def on_property_changing(self, obj: DataChangingProtocol, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name != 'email':
            return True
        if not isinstance(new_value, str):
            print(COLORING.format(31, "Error: Email must be a string!"))
            return False
        if not ("@stud.kantiana.ru" in new_value):
            print(COLORING.format(31, "Error: Email must be under BFU domain. Email is not correct."))
            return False
        print(COLORING.format(33, f"Email of {str(obj)} is changing from {old_value} to {new_value}"))
        return True