from typing import Self
from commands import PrintCharCommand

class KeyboardMemento:
    def __init__(self, state: dict) -> None:
        self.state = state
        
    @classmethod
    def from_keyboard(cls, keyboard) -> Self:
        text = PrintCharCommand.text

        key_bindings = {}
        for key, command in keyboard.key_bindings.items():
            if command is None:
                key_bindings[key] = None
            else:
                key_bindings[key] = {
                    'class': str(command.__class__.__name__),
                    'state': command.__dict__.copy()
                    }

        return cls({
            'text': text,
            'key_bindings': key_bindings,
            'history': [command["key"] for command in keyboard.history],
            'undo_stack': [command["key"] for command in keyboard.undo_stack]
            })