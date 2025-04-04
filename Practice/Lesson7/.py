from typing import Self
import math

WIDTH, HEIGHT = 1024, 650

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



class Vector2d:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def frompoints(cls, p1: Point2d, p2: Point2d) -> Self: #Or can be written "Vector2d"
        return cls(p2.x - p1.x, p2.y - p1.y)
    

    def __abs__(self) -> float:
        return math.sqrt((self.x * self.x) + (self.y * self.y)) # A bit faster, than ((self.x ** 2) + (self.y ** 2)) ** 0.5, so if you need to optimize - than use that


# Not from first lab
from dataclasses import dataclass
@dataclass
class Vector2dExtended:
    x: int
    y: int

    def __post_init__(self):
        if not (0 <= self.x <= WIDTH):
            raise ValueError("Wrong x value")
        if not (0 <= self.y <= HEIGHT):
            raise ValueError("Wrong y value")
        #Checking for validity
        pass


from pydantic import BaseModel, field_validator # has dataclasses inside
#Check for decorator usage
class Vector2dExtendedExtended(BaseModel):
    x: int
    y: int
    @field_validator('x')
    def x_validator(self) -> None:
        if not (0 <= self.x <= WIDTH):
            raise ValueError("Wrong x value")
    @field_validator('y')
    def y_validator(self) -> None:
        if not (0 <= self.x <= WIDTH):
            raise ValueError("Wrong x value")