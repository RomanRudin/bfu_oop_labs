import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Self

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...
    @abstractmethod
    def undo(self) -> None:
        ...
    @abstractmethod
    def redo(self) -> None:
        ...



class PrintCharCommand(Command):
    def __init__(self, char: str, output) -> None:
        self.char = char
        self.output = output
        
    def execute(self) -> str:
        self.output.add_char(self.char)
        return f"{self.char}"
        
    def undo(self) -> str:
        self.output.remove_char()
        return f"removed '{self.char}'"
        
    def redo(self) -> str:
        return self.execute()

class VolumeUpCommand(Command):
    def __init__(self, output) -> None:
        self.output = output
        self.amount = 20
        
    def execute(self) -> str:
        self.output.volume += self.amount
        return f"volume was increased +{self.amount}%"
        
    def undo(self) -> str:
        self.output.volume -= self.amount
        return f"volume was decreased +{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()

class VolumeDownCommand(Command):
    def __init__(self, output) -> None:
        self.output = output
        self.amount = 20
        
    def execute(self) -> str:
        self.output.volume -= self.amount
        return f"volume was decreased -{self.amount}%"
        
    def undo(self) -> str:
        self.output.volume += self.amount
        return f"volume was increased -{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()

class MediaPlayerCommand(Command):
    def __init__(self, output) -> None:
        self.output = output
        self.was_playing = False
        
    def execute(self) -> str:
        self.was_playing = self.output.media_playing
        self.output.media_playing = True
        return "media player was launched"
        
    def undo(self) -> str:
        self.output.media_playing = self.was_playing
        return "media player was closed"
        
    def redo(self) -> str:
        return self.execute()
    


class OutputState:
    def __init__(self) -> None:
        self.text = ""
        self.volume = 50
        self.media_playing = False
        
    def add_char(self, char: str) -> None:
        self.text += char
        
    def remove_char(self) -> None:
        if self.text:
            self.text = self.text[:-1]
            
    def get_state(self) -> dict[str, str | int | bool]:
        return {
            "text": self.text,
            "volume": self.volume,
            "media_playing": self.media_playing
        }
        
    def set_state(self, state: dict) -> None:
        self.text = state.get("text", "")
        self.volume = state.get("volume", 50)
        self.media_playing = state.get("media_playing", False)

# Класс для сохранения состояния (Memento)
class KeyboardMemento:
    def __init__(self, state: dict) -> None:
        self.state = state
        
    @classmethod
    def from_keyboard(cls, keyboard) -> Self:
        return cls({
            "key_bindings": keyboard.key_bindings,
            "output_state": keyboard.output.get_state()
        })

# Класс виртуальной клавиатуры
class VirtualKeyboard:
    def __init__(self) -> None:
        self.key_bindings: Dict[str, Command] = {}
        self.output = OutputState()
        self.history: List[Command] = []
        self.undo_stack: List[Command] = []
        
        # Инициализация стандартных команд
        self.init_default_bindings()
        
    def init_default_bindings(self) -> None:
        self.bind_key("a", PrintCharCommand("a", self.output))
        self.bind_key("b", PrintCharCommand("b", self.output))
        self.bind_key("c", PrintCharCommand("c", self.output))
        self.bind_key("d", PrintCharCommand("d", self.output))
        self.bind_key("ctrl++", VolumeUpCommand(self.output))
        self.bind_key("ctrl+-", VolumeDownCommand(self.output))
        self.bind_key("ctrl+p", MediaPlayerCommand(self.output))
        self.bind_key("undo", None)  # Специальная обработка
        self.bind_key("redo", None)  # Специальная обработка
        
    def bind_key(self, key: str, command: Optional[Command]) -> None:
        self.key_bindings[key] = command
        
    def press_key(self, key: str) -> str | None:
        if key == "undo":
            return self.undo()
        elif key == "redo":
            return self.redo()
            
        command = self.key_bindings.get(key)
        if command:
            result = command.execute()
            self.history.append(command)
            self.undo_stack.clear()  # Очищаем стек redo при новом действии
            return result
        return f"Unknown key: {key}"
        
    def undo(self):
        if not self.history:
            return "Nothing to undo"
            
        command = self.history.pop()
        result = command.undo()
        self.undo_stack.append(command)
        return f"undo: {result}"
        
    def redo(self):
        if not self.undo_stack:
            return "Nothing to redo"
            
        command = self.undo_stack.pop()
        result = command.redo()
        self.history.append(command)
        return f"redo: {result}"
        
    def save_state(self, filename: str = "keyboard_state.json"):
        memento = KeyboardMemento.from_keyboard(self)
        with open(filename, "w") as f:
            json.dump(memento.state, f)
            
    def load_state(self, filename: str = "keyboard_state.json"):
        try:
            with open(filename, "r") as f:
                state = json.load(f)
                
            self.key_bindings = state.get("key_bindings", {})
            self.output.set_state(state.get("output_state", {}))
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False



if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    
    # Проверяем, есть ли сохраненное состояние
    if not keyboard.load_state():
        print("No saved state found, using defaults")
    
    # Файл для записи лога
    with open("keyboard_log.txt", "w") as log_file:
        def print_and_log(message):
            print(message)
            log_file.write(message + "\n")
        
        # Симуляция нажатий клавиш
        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("b"))
        print_and_log(keyboard.press_key("c"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("redo"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl+-"))
        print_and_log(keyboard.press_key("ctrl+p"))
        print_and_log(keyboard.press_key("d"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        
        # Сохраняем состояние
        keyboard.save_state()
        print_and_log("Keyboard state saved")
