from typing import Self

WIDTH, HEIGHT = 1024, 750

#TODO Try using slots
#TODO Try using pydantic

class Point2d:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x    
    
    @x.setter
    def x(self, x: int) -> None:
        if not (0 <= x <= WIDTH):
            raise ValueError("Wrong x value")
        self._x = x
        
    @property
    def y(self) -> int:
        return self._y    
    
    @y.setter
    def y(self, y: int) -> None:
        if not (0 <= y <= HEIGHT):
            raise ValueError("Wrong y value")
        self._y = y

    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return f"Point2d({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)
