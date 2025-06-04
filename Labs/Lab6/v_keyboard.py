from typing import Optional
import json
from commands import *
from memento import KeyboardMemento

class VirtualKeyboard:
    def __init__(self) -> None:
        self.key_bindings: dict[str, Command] = {}
        self.output = {"text": "", "volume": 0, "media_playing": False}
        self.history: list[Command] = []
        self.undo_stack: list[Command] = []

        self.init_default_bindings()
        
    def init_default_bindings(self) -> None:
        self.bind_key("a", PrintCharCommand("a",  self))
        self.bind_key("b", PrintCharCommand("b",  self))
        self.bind_key("c", PrintCharCommand("c",  self))
        self.bind_key("d", PrintCharCommand("d",  self))
        self.bind_key("ctrl++", VolumeUpCommand( self))
        self.bind_key("ctrl+-", VolumeDownCommand( self))
        self.bind_key("ctrl+p", MediaPlayerCommand( self))
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
            self.bind_key(key, PrintCharCommand(key, self))
            command = self.key_bindings.get(key)
        if command:
            result = command.execute()
            self.history.append(command)
            self.undo_stack.clear()  
            return result
        return f"Unknown key: {key}"
        
    def undo(self) -> str:
        if not self.history:
            return "Nothing to undo"
            
        command = self.history.pop()
        result = command.undo()
        self.undo_stack.append(command)
        return f"undo: {result}"
        
    def redo(self) -> str:
        if not self.undo_stack:
            return "Nothing to redo"
            
        command = self.undo_stack.pop()
        result = command.redo()
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

            class_names = {cls.__name__: cls for cls in Command.__subclasses__()}
                
            self.key_bindings = {}
            raw_key_bindings = state.get("key_bindings", {})
            for bind, command_data in raw_key_bindings.items():
                if command_data[0] is None:
                    self.key_bindings[bind] = None
                else:
                    command_data[1].update({"output": self.output})
                    command = class_names[command_data[0]](**command_data[1])
                    self.key_bindings[bind] = command
            self.output = state.get("output_state", {})
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
