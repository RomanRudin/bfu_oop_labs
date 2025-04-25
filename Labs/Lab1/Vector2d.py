from typing import Generator, Self
import math
from point2d import Point2d, WIDTH, HEIGHT

class Vector2d:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @classmethod
    def frompoints(cls, p1: Point2d, p2: Point2d) -> Self: #Or can be written "Vector2d"
        return cls(p2.x - p1.x, p2.y - p1.y)

    @property
    def x(self) -> float:
        return self._x    
    
    @x.setter
    def x(self, x: float) -> None:
        self._x = x
        
    @property
    def y(self) -> float:
        return self._y    
    
    @y.setter
    def y(self, y: float) -> None:
        self._y = y

    def __getitem__(self, index) -> float: # Check slots
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError("Index out of range")

    def __setitem__(self, index: float, value: float) -> None:
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError("Index out of range")

    def __iter__(self) -> Generator[float]:
        yield self.x
        yield self.y

    def __len__(self) -> float:
        return 2
 
    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __abs__(self) -> float:
        return math.sqrt((self.x * self.x) + (self.y * self.y)) # A bit faster, than ((self.x ** 2) + (self.y ** 2)) ** 0.5, so if you need to optimize - than use that

    def __add__(self, value: Self) -> Self:
        return Vector2d(self.x + value.x, self.y + value.y)

    def __sub__(self, value: Self) -> Self:
        return Vector2d(self.x - value.x, self.y - value.y)

    def __mul__(self, value: float) -> Self:
        return Vector2d(self.x * value, self.y * value)

    def __rmul__(self, value: float) -> Self:
        return Vector2d(self.x * value, self.y * value)

    def __truediv__(self, value: float) -> Self: #! Does it need to be floategers or float everywhere?
        return Vector2d(self.x // value, self.y // value) 
    
    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y
    
    @staticmethod   # Can be done better with classmethod
    def dot_product(vector1: Self, vector2: Self) -> float:
        return vector1.x * vector2.x + vector1.y * vector2.y
    
    def cross(self, other: Self) -> Self:
        return Vector2d(self.x * other.y - self.y * other.x, 0)

    @staticmethod
    def cross_product(vector1: Self, vector2: Self) -> Self:
        return Vector2d(vector1.x * vector2.y - vector1.y * vector2.x, 0)

    def triple(self, vector2: Self, vector3: Self) -> float:
        return self.dot(Vector2d.cross(vector2, vector3))
    
    @staticmethod
    def triple_product(vector1: Self, vector2: Self, vector3: Self) -> float:
        return vector1.dot(Vector2d.cross(vector2, vector3))
