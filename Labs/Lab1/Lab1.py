from Point2d import Point2d
from Vector2d import Vector2d


if __name__ == "__main__":
    p1 = Point2d(50, 100)
    p2 = Point2d(800, 600)
    print(p1)  # Point2d(50, 100)
    print(p2)  # Point2d(800, 600)
    print(p1 == p2)  # False

    v1 = Vector2d(3, 4)
    v2 = Vector2d.frompoints(p1, p2)
    print(v1)  # Vector2d(3, 4)
    print(v2)  # Vector2d(750, 500)
    print(abs(v1))  # 5.0

    print(v1 + v2)  # Vector2d(753, 504)
    print(v2 - v1)  # Vector2d(747, 496)
    print(v1 * 2)   # Vector2d(6, 8)
    print(3 * v1)   # Vector2d(9, 12)
    print(v2 / 2)   # Vector2d(375, 250)

    print(v1.dot(v2))          # 3*750 + 4*500 = 4250
    print(Vector2d.dot_product(v1, v2))  # 4250
    print(v1.cross(v2))        # 3*500 - 4*750 = -1500
    print(Vector2d.cross_product(v1, v2)) # -1500

    v3 = Vector2d(2, 5)
    print(v1.triple(v2, v3))  # v1 ⋅ (v2 × v3)
    print(Vector2d.triple_product(v1, v2, v3))  # v1 ⋅ (v2 × v3)