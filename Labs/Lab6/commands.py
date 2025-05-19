from abc import ABC, abstractmethod
from typing import Self
from output_state import OutputState

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
    def __init__(self, char: str, output: OutputState) -> None:
        self.output = output
        self.char = char
        
    def execute(self) -> str:
        self.output.add_char(self.char)
        return f"{self.char}"
        
    def undo(self) -> str:
        self.output.remove_char()
        return f"removed '{self.char}'"
        
    def redo(self) -> str:
        return self.execute()
    

class VolumeUpCommand(Command):
    def __init__(self, output: OutputState, amount:  int = 20) -> None:
        self.output = output
        self.amount = amount
        
    def execute(self) -> str:
        self.output.volume += self.amount
        return f"volume increased +{self.amount}%"
        
    def undo(self) -> str:
        self.output.volume -= self.amount
        return f"volume decreased +{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()
    
    @classmethod
    def from_dict(cls, data: dict, output: OutputState) -> Self:
        return cls({
            "output": output,
            "amount": data["amount"]
        })


class VolumeDownCommand(Command):
    def __init__(self, output: OutputState, amount:  int = 20) -> None:
        self.output = output
        self.amount = amount
        
    def execute(self) -> str:
        self.output.volume -= self.amount
        return f"volume decreased -{self.amount}%"
        
    def undo(self) -> str:
        self.output.volume += self.amount
        return f"volume increased -{self.amount}%"
        
    def redo(self) -> str:
        return self.execute()
    
    @classmethod
    def from_dict(cls, data: dict, output: OutputState) -> Self:
        return cls({
            "output": output,
            "amount": data["amount"]
        })

class MediaPlayerCommand(Command):
    def __init__(self, output: OutputState, was_playing: bool = False) -> None:
        self.output = output
        self.was_playing = was_playing
        
    def execute(self) -> str:
        self.was_playing = self.output.media_playing
        self.output.media_playing = True
        return "media player launched"
        
    def undo(self) -> str:
        self.output.media_playing = self.was_playing
        return "media player closed"
        
    def redo(self) -> str:
        return self.execute()
    
    @classmethod
    def from_dict(cls, data: dict, output: OutputState) -> Self:
        return cls({
           "output": output,
            "was_playing": data["was_playing"]
        })
