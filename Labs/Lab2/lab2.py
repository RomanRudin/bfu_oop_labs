import json
from enum import Enum
from typing import Dict, List, Tuple, Self

class Color(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

class Printer:
    _font: Dict[str, List[str]] = {}
    _char_width: int = 0
    _char_height: int = 0

    def __init__(self, color: Color, position: Tuple[int, int], symbol: str) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.initial_x, self.initial_y = position
        self.current_x, self.current_y = position

    @classmethod
    def load_font(cls, filename: str = "font.json") -> None:
        with open(filename, "r") as f:
            cls._font = json.load(f)
            if cls._font:
                sample_char = next(iter(cls._font.values()))
                cls._char_height = len(sample_char)
                cls._char_width = len(sample_char[0]) if cls._char_height > 0 else 0

    @classmethod
    def print_(cls, text: str, color: Color, position: Tuple[int, int], symbol: str) -> None:
        if not cls._font:
            cls.load_font()
        
        x, y = position
        for char in text:
            if char not in cls._font:
                continue
            
            for line_num, line in enumerate(cls._font[char]):
                rendered = line.replace("*", symbol)
                print(f"\033[{y + line_num + 1};{x + 1}H\033[{color.value}m{rendered}\033[0m", end="")
            
            x += cls._char_width
        print()

    def __enter__(self) -> Self:
        print("\033[s", end="")
        print(f"\033[{self.color.value}m", end="") 
        return self

    def __exit__(self, *args) -> None:
        print("\033[0m\033[u", end="") 

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
    with open("Labs/Lab2/font.json", "w") as f:
        json.dump({
            "A": ["  *  ", " * * ", "*****", "*   *", "*   *"],
            "B": ["**** ", "*   *", "**** ", "*   *", "**** "]
        }, f)

    Printer.load_font(filename="Labs/Lab2/font.json")
    Printer.print_("AB", Color.RED, (5, 5), "#")
    with Printer(Color.GREEN, (5, 10), "@") as p:
        p.print("AB")
        p.print("BA")

    # import os
    # os.remove("font.json")