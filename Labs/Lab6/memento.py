from typing import Self

class KeyboardMemento:
    def __init__(self, state: dict) -> None:
        self.state = state
        
    @classmethod
    def from_keyboard(cls, keyboard) -> Self:
        key_bindings = {}
        for bind, command in keyboard.key_bindings.items():
            if command is None:
                key_bindings[bind] = [None, None]
            else:
                command_dict = command.__dict__
                command_dict.pop("keyboard")
                key_bindings[bind] = [str(command.__class__.__name__), command_dict]

        return cls({
            "key_bindings": key_bindings,
            "output_state": keyboard.output
        })