from typing import Any, Generator, Self
import math

WIDTH, HEIGHT = 1024, 750

# Try using slots
# Try using pydantic

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




class Vector2d:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def frompoints(cls, p1: Point2d, p2: Point2d) -> Self: #Or can be written "Vector2d"
        return cls(p2.x - p1.x, p2.y - p1.y)

    @property
    def x(self) -> int:
        return self._x    
    
    @x.setter
    def x(self, x: int) -> None:
        # if not (0 <= x <= WIDTH):
            # raise ValueError("Wrong x value")
        self._x = x
        
    @property
    def y(self) -> int:
        return self._y    
    
    @y.setter
    def y(self, y: int) -> None:
        # if not (0 <= y <= HEIGHT):
            # raise ValueError("Wrong y value")
        self._y = y

    def __getitem__(self, index) -> int:
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError("Index out of range")

    def __setitem__(self, index: int, value: int) -> None:
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError("Index out of range")

    def __iter__(self) -> Generator[int, Any, None]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2
 
    def __eq__(self, value: object) -> bool:
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

    def __mul__(self, value: int) -> Self:
        return Vector2d(self.x * value, self.y * value)

    def __rmul__(self, value: int) -> Self:
        return Vector2d(self.x * value, self.y * value)

    def __truediv__(self, value: int) -> Self: #! Does it need to be integers or float everywhere?
        return Vector2d(self.x // value, self.y // value) 
    
    def dot(self, other: Self) -> int:
        return self.x * other.x + self.y * other.y
    
    @staticmethod
    def dot_product(vector1: Self, vector2: Self) -> int:
        return vector1.x * vector2.x + vector1.y * vector2.y
    
    #TODO
    def cross(self, other: Self) -> Self:
        return Vector2d(self.x * other.y - self.y * other.x, 0)

    #TODO
    @staticmethod
    def cross_product(vector1: Self, vector2: Self) -> Self:
        return Vector2d(vector1.x * vector2.y - vector1.y * vector2.x, 0)

    def triple(self, vector2: Self, vector3: Self) -> int:
        return self.dot(Vector2d.cross(vector2, vector3))
    
    @staticmethod
    def triple_product(vector1: Self, vector2: Self, vector3: Self) -> int:
        return vector1.dot(Vector2d.cross(vector2, vector3))



if __name__ == "__main__":
    # Тестирование Point2d
    p1 = Point2d(50, 100)
    p2 = Point2d(800, 600)  # Значения будут ограничены
    print(p1)  # Point2d(50, 100)
    print(p2)  # Point2d(800, 600)
    print(p1 == p2)  # False

    # Тестирование Vector2d
    v1 = Vector2d(3, 4)
    v2 = Vector2d.frompoints(p1, p2)
    print(v1)  # Vector2d(3, 4)
    print(v2)  # Vector2d(750, 500)
    print(abs(v1))  # 5.0

    # Операции с векторами
    print(v1 + v2)  # Vector2d(753, 504)
    print(v2 - v1)  # Vector2d(747, 496)
    print(v1 * 2)   # Vector2d(6, 8)
    print(3 * v1)   # Vector2d(9, 12)
    print(v2 / 2)   # Vector2d(375, 250)

    # Произведения
    print(v1.dot(v2))          # 3*750 + 4*500 = 4250
    print(Vector2d.dot_product(v1, v2))  # 4250
    print(v1.cross(v2))        # 3*500 - 4*750 = -1500
    print(Vector2d.cross_product(v1, v2)) # -1500

    # Смешанное произведение
    v3 = Vector2d(2, 5)
    print(v1.triple(v2, v3))  # v1 ⋅ (v2 × v3)
    print(Vector2d.triple_product(v1, v2, v3))  # v1 ⋅ (v2 × v3)