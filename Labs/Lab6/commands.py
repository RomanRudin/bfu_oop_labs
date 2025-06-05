from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from v_keyboard import VirtualKeyboard #Basicly imports VirtualKeyboard only as an annotation reference


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
    def __init__(self, char: str, keyboard) -> None:
        self.keyboard = keyboard
        self.char = char
        
    def execute(self) -> str:
        self.keyboard.output["text"] += self.char
        return f"{self.char}"
        
    def undo(self) -> str:
        self.keyboard.output["text"] = self.keyboard.output["text"][:-1]
        return f"removed '{self.char}'"
        
    def redo(self) -> str:
        return self.execute()
    


class VolumeUpCommand(Command):
    def __init__(self, keyboard: VirtualKeyboard, amount:  int = 20) -> None:
        self.keyboard = keyboard
        self.amount = amount
        
    def execute(self) -> str:
        self.keyboard.output["volume"] += self.amount
        return f"volume increased +{self.amount}%"
        
    def undo(self) -> str:
        self.keyboard.output["volume"] -= self.amount
        return f"volume decreased +{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()



class VolumeDownCommand(Command):
    def __init__(self, keyboard: VirtualKeyboard, amount:  int = 20) -> None:
        self.keyboard = keyboard
        self.amount = amount
        
    def execute(self) -> str:
        self.keyboard.output["volume"] -= self.amount
        return f"volume decreased -{self.amount}%"
        
    def undo(self) -> str:
        self.keyboard.output["volume"] += self.amount
        return f"volume increased -{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()
    


class MediaPlayerCommand(Command):
    def __init__(self, keyboard: VirtualKeyboard, was_playing: bool = False) -> None:
        self.keyboard = keyboard
        self.was_playing = was_playing
        
    def execute(self) -> str:
        self.was_playing = self.keyboard.output["media_playing"]
        self.keyboard.output["media_playing"] = True
        return "media player launched"
        
    def undo(self) -> str:
        self.keyboard.output["media_playing"] = self.was_playing
        return "media player closed"
        
    def redo(self) -> str:
        return self.execute()
    