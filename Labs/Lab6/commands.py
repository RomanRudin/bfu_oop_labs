from __future__ import annotations
from abc import ABC, abstractmethod



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
    text = ""  # Хранение всего текста

    def __init__(self, char: str) -> None:
        self.char = char
        
    def execute(self) -> str:
        PrintCharCommand.text += self.char
        return PrintCharCommand.text
        
    def undo(self) -> str:
        PrintCharCommand.text = PrintCharCommand.text[:-1]
        return PrintCharCommand.text
        
    def redo(self) -> str:
        return self.execute()
    
    

class VolumeUpCommand(Command):
    def __init__(self, amount: int = 20, current_volume: int = 50) -> None:
        self.amount = amount
        self.current_volume = current_volume 
        
    def execute(self) -> str:
        self.current_volume += self.amount
        return f"volume increased +{self.amount}% (now: {self.current_volume}%)"
        
    def undo(self) -> str:
        self.current_volume -= self.amount
        return f"volume decreased +{self.amount}% (now: {self.current_volume}%)"
        
    def redo(self) -> str:
        return self.execute()



class VolumeDownCommand(Command):
    def __init__(self, amount: int = 20, current_volume: int = 50) -> None:
        self.amount = amount
        self.current_volume = current_volume  
        
    def execute(self) -> str:
        self.current_volume -= self.amount
        return f"volume decreased -{self.amount}% (now: {self.current_volume}%)"
        
    def undo(self) -> str:
        self.current_volume += self.amount
        return f"volume increased -{self.amount}% (now: {self.current_volume}%)"
        
    def redo(self) -> str:
        return self.execute()



class MediaPlayerCommand(Command):
    def __init__(self, is_playing: bool = False) -> None:
        self.is_playing = is_playing
        
    def execute(self) -> str:
        self.is_playing = True
        return "media player launched"
        
    def undo(self) -> str:
        self.is_playing = False
        return "media player closed"
        
    def redo(self) -> str:
        return self.execute()