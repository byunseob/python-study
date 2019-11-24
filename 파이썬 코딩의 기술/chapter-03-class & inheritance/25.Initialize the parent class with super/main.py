# 기존에는 자식 클래스에서 부모클래스의 __init__ 메소드를 직접 호출하는 방법으로 부모클래스를 초기화했다.


class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)


# 이 방법은 간단한 계층 구조에는 잘 동작하지만 많은 경우 제대로 동작하지 못한다.
# 클래스가 다중상속의 영향을 받는다면 슈퍼클래스의 __init__ 메소드를 직접 호출하는 행위는 예기치 못한 동작을 일으킬 수 있다.

# 한 가지 문제는 __init__ 의 호출 순서가 몯느 서브클래스에 걸쳐 명시되어 있지 않다는 점이다.
# 예를 들어 인스턴스의 value 필드로 연산을 수행하는 부모 클래스 두 개를 정의해보자.

class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


# 다음 클래스는 한 가지 순서로 부모 클래스들을 정의한다.

class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# 이 클래스의 인스턴스를 생성하면 부모 클래스의 순서와 일치하는 결과가 만들어진다.
foo = OneWay(5)
print("First ordering is (5 * 2) + 5 =", foo.value)


# 다음은 같은 부모클래스들을 다른 순서로 정의한 클래스다.

class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# 하지만 부모클래스 생성자 PlusFive.__init__, TimesTwo.__init__를 이전과 같은 순서로 호출한다.
# 이클래스의 동작은 부모 클래스를 정의한 순서와 일치하지 않는다.
bar = AnotherWay(5)
print("Second ordering still is", bar.value)


# 다른 문제는 다이아몬드 상속이다.
# 다이아몬드 상속은 서브클래스가 계층 구조에서 같은 슈퍼클래스르 둔 서러 다른 두 클래스에서 상속 받을때 발생한다.
# 다이아몬드 상속은 공통 슈퍼클래스의 __init__ 메서드를 여러 번 실행하게 해서 예상치 못한 동작을 일으킨다.

class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)


foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)


# 결과는 27 이어햐 하지만 두번째 부모 클래스의 생성자 PlusTow.__init__를 호출하는 코드가 있어서
# MyBaseClass.__init__가 두번째 호출될때 value 를 다시 5로 리셋한다.

# 파이썬 2.2 에서는 이 문제를 해결하려고 super 라는 내장 함수를 추가하고 메소드 해석순서 (MRO)를 정의했다.
# MRO는 어떤 슈퍼클래스부터 초기화하는지를 정한다.

# 파이썬 3 에서는 super 를 인수없이 호출하면 __class__와  self 를 인수로 넘겨서 호출한 것으로 처리한다.

class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


assert Explicit(10).value == Implicit(10).value

# 파이썬3 에서는 __class__ 변수를 사용한 메소드에서 현재 클래스를 올바르게 참조하도록 해주므로 위의 코드가 잘동작한다.

