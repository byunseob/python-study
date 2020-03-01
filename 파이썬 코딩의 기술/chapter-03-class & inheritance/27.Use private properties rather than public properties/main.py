# 파이썬에는 클래스 속성의 가시성이 공개과 비공개 두 유형만 존재한다.


class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_filed = 10

    def get_private_field(self):
        return self.__private_filed


# 공개 속성은 어디서든 객체에 점 연산자를 사용하여 접근할 수있다.

foo = MyObject()
assert foo.public_field == 5

# 비공개 필드는 속성 이름 앞에 밑줄 두개를 붙여 지정한다.
# 같은 클래스에 속한 메서드에서는 비공개 필드에 직접 접근할 수 있다.

assert foo.get_private_field() == 10


# 하지만 클래스 외부에서 직접 비공개 필드에 접근하면 예외가 일어난다.
# foo.__private_field


# AttributeError: 'Myobject' object has no attribute '__private_field'

# 클래스 메서드도 같은 class 블록에 선언되어 있으므로 비공개 속성에 접근할 수 있다.

class MyOtherObject(object):
    def __init__(self):
        self.__private_filed = 71

    @classmethod
    def get_private_field(cls, instance):
        return instance.__private_filed


bar = MyOtherObject()
assert MyOtherObject.get_private_field(bar) == 71


# 비공개 필드라는 용어에서 예상할 수 있듯이 서브클래스에서는 부모 클래스의 비공개 필드에 접근할 수없다.
class MyParentObject(object):
    def __init__(self):
        self.__private_filed = 71


class MyChildObject(MyOtherObject):
    def get_private_field(self):
        return self.__private_filed


baz = MyChildObject()
# baz.get_private_field()
# AttributeError: 'MyChildObject' object has no attribute '_MyChildObject__private_filed'


# 비공개 속성의 동작은 간단하게 속성 이름을 변환하는 방식으로 구현된다.
# 파이썬 컴파일러는 MyChildObject.get_private_filed 같은 메소드에서 비공개
# 속성에 접근하는 코드를 발견하면 _private_field 를 _MyChildObject__private_field 에
# 접근하는 코드로 변환한다.
# 자식 클래스에서 부모의 비공개 속성에 접근하는 동작은 단순히 변환된 속성 이름이 일치하지 않아서 실패한다.

# 이 체계를 이해하면 접근 권한을 확인하지 않고서도 서브클래스나 외부 클래스에서 어떤 클래스의
# 비공개 속성이든 쉽게 접근 할 수 있다.
assert baz._MyOtherObject__private_filed == 71

# 객체의 속성 딕셔너리를 들여다보면 실제로 비공개 속성이 변환 후의 이름으로 저장되어 있음을 알 수있다.
print(baz.__dict__)  # {'_MyOtherObject__private_filed': 71}


# 비공개 속성용 문법이 가시성을 엄격하게 강제하지 않는 이유는
# 파이선 프로그래머들은 개방으로 얻는 장점이 폐쇄로 얻는 단점보다 크다고 믿는다.

# 그럼에도 비공개 속성에 접근하는 것을 막는 이유는 무분별하게 객체의 내부에 접근하는 위험을
# 최소하하려고 _protected_field 를 만들어 클래스의 외부 사용자들이 신중하게 다뤄야 함을 나타내고 있다.

# 하지만 파이썬을 처음 접하는 많은 프로그래머가 서브클래스나 외부에서 접근하면 안 되는 내부 API 를
# 비공개 필드로 나타낸다.

class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)


foo = MyClass(5)
assert foo.get_value() == '5'


# 이 접근 방식은 잘못되었다.
# 누군가 클래스에 새 동작을 추가하거나 기존 메서드의 결함을 해결 하려고 서브클래스를 만들기 마련이다.
# 비공개 속성을 선택하면 서브클래스의 오버라이드와 확장을 다루기 어렵고 불안정하게 만들 뿐이다.
# 나중에 만들 서브클래스에서 꼭 필요하면 여전히 비공개 필드에 접근할 수있다.

class MyIntegerSubClass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)


foo = MyIntegerSubClass(5)
assert foo.get_value() == 5


# 하지만 나중에 클래스의 계층이 변경되면 MyIntegerSubClass 같은 클래스는 비공개 참조가 더는
# 유효하지 않아 제대로 동작하지 않는다.

# 일반적으로 보호 속성을 사용해서 서브클래스가 더 많은 일을 할 수있게 하는 편이 낫다.
# 각각의 보호필드를 문서화해서 서브클래스에서 내부 API 를 상세히 서술하자.
# 이렇게 하면 자신이 작성한 코드를 미래에 안전하게 확장하는 지침이 되는 것처럼 다른 프로그래머에게도 조언이 된다.

class MyClass(object):
    def __init__(self, value):
        # 사용자가 객체에 전달한 값을 저장한다.
        # 문자열로 강제할 수있는 값이어야 하며,
        # 객체에 할달하고 나면 불변으로 취급해야한다.
        self._value = value

# 비공개 속성을 사용할지 진지하게 고민할 시점은 서브클래스와 이름이 충동할 염려가 있을 때 뿐이다.
