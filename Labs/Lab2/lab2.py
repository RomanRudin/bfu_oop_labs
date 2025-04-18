import json
from enum import Enum
from typing import Self

class Color(Enum):
    TRANSPARENT = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    

class Printer:
    _font: dict[str, list[str]] = {}
    _char_width: int = 5
    _char_height: int = 5

    def __init__(self, color: Color, position: tuple[int, int], symbol: str, background_color: Color = Color.TRANSPARENT) -> None:
        self.color = color
        self.background_color = background_color
        self.position = position
        self.symbol = symbol
        self.initial_x, self.initial_y = position
        self.current_x, self.current_y = position

    @classmethod
    def load_font(cls, filename: str = "font.json") -> None:
        try:
            with open(filename, "r") as f:
                cls._font = json.load(f)
            if cls._font:
                sample_char = next(iter(cls._font.values()))
                cls._char_height = len(sample_char)
                cls._char_width = len(sample_char[0])
        except Exception as e:
            print(f"Error loading font file: {e}")

    @classmethod
    def print_(cls, text: str, color: Color, position: tuple[int, int], symbol: str, background_color: Color = Color.BLACK) -> None:
        if not cls._font:
            cls.load_font()
        
        x, y = position
        for char in text:
            if char not in cls._font:
                raise ValueError(f"Character {char} is not in the font file")
            
            for line_num, line in enumerate(cls._font[char]):
                rendered = line.replace("*", symbol)
                print(f"\033[{y + line_num + 1};{x + 1}H\033[{color.value}m\033[{background_color.value + 10}m{rendered}\033[0m", end="")
            
            x += cls._char_width
        print()

    def __enter__(self) -> Self:
        print(f"\033[{self.color.value}m\033[{self.background_color.value + 10}m", end="") 
        return self

    def __exit__(self, *args) -> None:
        print(f"\033[0m", end="")

    def print(self, text: str) -> None:
        x, y = self.current_x, self.current_y
        for char in text:
            if char not in self._font:
                continue
            
            for line_num, line in enumerate(self._font[char]):
                rendered = line.replace("*", self.symbol)
                print(f"\033[{y + line_num + 1};{x + 1}H{rendered}", end="")
            
            x += self._char_width
        self.current_x = x



if __name__ == "__main__":
    for _ in range(30):
        print()
    Printer.load_font(filename="Labs/Lab2/font.json")
    Printer.print_("AB", Color.RED, (5, 5), "#", background_color=Color.TRANSPARENT)
    with Printer(Color.GREEN, (0, 10), "@", background_color=Color.BLACK) as printer:
        printer.print("OOP LABS ARE COOL")
        # printer.print("AB")