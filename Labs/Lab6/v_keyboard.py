from typing import Optional
import json
from commands import *
from memento import KeyboardMemento

class VirtualKeyboard:
    def __init__(self) -> None:
        self.key_bindings: dict[str, Command] = {}
        self.history: list[dict[str, Command]] = []
        self.undo_stack: list[dict[str, Command]] = []

        self.init_default_bindings()
        
    def init_default_bindings(self) -> None:
        self.bind_key("a", PrintCharCommand("a"))
        self.bind_key("b", PrintCharCommand("b"))
        self.bind_key("c", PrintCharCommand("c"))
        self.bind_key("d", PrintCharCommand("d"))
        self.bind_key("ctrl++", VolumeUpCommand())
        self.bind_key("ctrl+-", VolumeDownCommand())
        self.bind_key("ctrl+p", MediaPlayerCommand())
        self.bind_key("undo", None)  
        self.bind_key("redo", None)  
        
    def bind_key(self, key: str, command: Optional[Command]) -> None:
        self.key_bindings[key] = command
        
    def press_key(self, key: str) -> str | None:
        if key == "undo":
            return self.undo()
        elif key == "redo":
            return self.redo()
            
        command = self.key_bindings.get(key)
        if not command and len(key) == 1:
            self.bind_key(key, PrintCharCommand(key))
            command = self.key_bindings.get(key)
        if command:
            result = command.execute()
            self.history.append({"key": key, "command": command})
            self.undo_stack.clear()  
            return result
        return f"Unknown key: {key}"
        
    def undo(self) -> str:
        if not self.history:
            return "Nothing to undo"
            
        command = self.history.pop()
        result = command["command"].undo()
        self.undo_stack.append(command)
        return f"undo: {result}"
        
    def redo(self) -> str:
        if not self.undo_stack:
            return "Nothing to redo"
            
        command = self.undo_stack.pop()
        result = command["command"].redo()
        self.history.append(command)
        return f"redo: {result}"
        
    def save_state(self, filename: str = "Labs/Lab6/data/keyboard_state.json") -> None:
        memento = KeyboardMemento.from_keyboard(self)
        try:
            with open(filename, "w") as f:
                json.dump(memento.state, f, indent=4)
        except Exception as e:
            print(f"Error saving state: {e}")
            raise e

    def load_state(self, filename: str = "Labs/Lab6/data/keyboard_state.json") -> bool:
        try:
            with open(filename, "r") as f:
                state = json.load(f)
            
            PrintCharCommand.text = state['text']
            class_names = {cls.__name__: cls for cls in Command.__subclasses__()}
                
            self.key_bindings.clear()
            for key, command_data in state.get('key_bindings', {}).items():
                if command_data is None:
                    self.key_bindings[key] = None
                else:
                    command = class_names[command_data['class']](**command_data['state'])
                    self.key_bindings[key] = command

            self.history = [
                {"key": key, "command": self.key_bindings[key]} 
                for key in state.get('history', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]

            self.undo_stack = [
                {"key": key, "command": self.key_bindings[key]} 
                for key in state.get('undo_stack', [])
                if key in self.key_bindings.keys() and self.key_bindings[key] is not None
            ]
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Error loading state: {e}")
            return False



