#include <iostream>
#include <string>
#include <winuser.h>
/*
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
*/

const int SCREEN_WIDTH = GetSystemMetrics(SM_CXSCREEN);
const int SCREEN_HEIGHT = GetSystemMetrics(SM_CYSCREEN);

class point2d {
private:
	int _x;
	int _y;
public:
	point2d() { _x = _y = 0; };
	point2d(int x, int y) {
		if (0 <= x && x <= SCREEN_WIDTH && 0 <= y && y <= SCREEN_HEIGHT) {
			_x = x;
			_y = y;
		}
	}
	point2d(const point2d& other) {
		_x = other.getX();
		_y = other.getY();
	}
	point2d operator=(const point2d& other) {
		_x = other.getX();
		_y = other.getY();
	}
	~point2d() = default;
	std::string str() {
		return '(' + std::to_string(_x) + ',' + std::to_string(_y) + ')';
	}
	int getX() const { return _x; }
	int& setX() { return _x; }
	int getY() const { return _y; }
	int& setY() { return _y; }
};

class vector2d {
private:
	int _x;
	int _y;
public:
	vector2d() { _x = _y = 0; }
	vector2d(int x, int y) {
		_x = x;
		_y = y;
	}
};

int main() {

	return 0;
}