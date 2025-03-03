Спасибо Мише за лекцию

Point2d:
 - x: int
 - y: int

 - строковое представление: __str__, __repr__
 - добавить проверку на то, что 0 <= x <= SCREEN_WIDTH, 0 <= y <= SCREEN_HEIGHT

 Vector2d:
 - x: int
 - y: int
 - vector2d from x, y
 - vector2d from start point2d, end point2d

 - строковое представление: __str__, __repr__
 - реализовать протокол Secuence: __getitem__(доступ по индексу), __len__(длина)
 - реализовать изменения по индексу: __setitem__

 - модуль: __abs__
 - сравнение: __le__, __ge__, __eq__
 - сложение и вычитание __add__, __sub__
 - умножение на число __mul__
 - деление на число __div__
 - скалярное умножение __mul__, __matmul__