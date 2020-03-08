# 메타클래스는 서브클래스가 정의될 때마다 검증 코드를 실행하는 신뢰할 만한 방법을 제공한다.
# 보통 클래스 검증 코드는 클래스의 객체가 생설될 때 __init__ 메서드에서 실행된다.

# 메타클래스는 type 을 상속하여 정의한다.
# 메타클래슨느 기본으로 자체의 __new__ 메서드에 연관된 class 문의 콘텐츠를 받는다
# 여기서 타입이 실제로 생성되기 전에 클래스 정보를 수정할 수 있다.


class Meta(type):
    def __new__(cls, *args, **kwargs):
        print(cls, *args, **kwargs)
        return type.__new__(cls, *args, **kwargs)


# 메타클래스는 클래스의 이름, 클래스가 상속하는 부모클래스, class 에 정의한 모든 클래스 속성에 접근할 수 있다.
class MyClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


class ValidatePolygon(type):
    def __new__(cls, *args, **kwargs):
        # 추상 Polygon 클래스는 검증하지 않음
        if args[1] != (object,):
            if args[2].get('sides') < 3:
                raise ValueError('Polygons need 3+ sides')

        return super().__new__(cls, *args, **kwargs)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None  # 서브클래스에서 설정

    @classmethod
    def interior_angels(cls):
        return (cls.sides - 2) * 180


# class Triangle(Polygon):
#     sides = 3

print('Before class')


class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')

    def __init__(self):
        print(1)

# 서브클래스 타입의 객체를 생성하기에 앞서 서브클래스가 정의 시점부터 제대로 구성되었음을 보장하려면
# 메타클래스를 사용하자
# 메타클래스의 __new__ 메서드는 class 문의 본문 전체가 처리된 후에 실행된다.
