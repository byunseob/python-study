# @property 의 큰 문제점은 재사용성이다.
# 여러 속성에 사용하지 못한다.

# 과목이 늘어날수록 프로퍼티와 체크그레이드 를 반복적으로 작성해야함
from weakref import WeakKeyDictionary


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


# 디스크립터 프로토콜은 속성에 대한 접근을 언어에서 해석할 방법을 정의한다.
# 디스크립터 클래스는 반복 코드 없이도 성적 검증 동작을 재사용하게 해주는 _get_ 과 _set_
# 메소드를 제공할 수 있다
# 디스크립터를 이용하면 한 클래스의 서로 다른 많은 속성에 같은 로직을 재사용할 수 있다.

class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('0 ~ 100')
        self._value = value


class Exam(object):
    # 클래스 속성
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


exam = Exam()
exam.writing_grade = 40

# 위코드는 아래와같다
# Exam.__dict__['writing_grade'].__set__(exam, 40)

print(exam.writing_grade)


# 위코드는 아래와 같이 해석된다.
# Exam.__dict__['writing_grade'].__get__(exam, Exam)

# 이렇게 동작하게 만드는건 object 의  __getattribute__ 메소드다
# Exam 인스턴스에 writing_grade 속성이 없으면
# 파이썬은 대신 Exam 클래스의 속성을 이용한다

# 위 Exam 클래스의 문제는 여러개의 다른 인스턴스에서도 Exam 인스턴스의
# writing_grade 를 클래스 속성으로 공유된다는 점이다.
# 이 속성에 대응하는 Grade 인스턴스는 프로그램에서 Exam 인스턴스를
# 생성할 때마다 생성되는 게 아니라 Exam 클래스를 처음 정의할 때 한번만 생성된다.

# 이 문제를 해결하려면 각 Exam 인스턴스별로 값을 추적하는 Grade 클래스가 필요하다.
# 여기서는 딕셔너리에 각 인스턴스의 상태를 저장하는 방법으로 값을 추적한다.

class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('0 ~ 100')
        self._values[instance] = value


# 이 구현은 간단하지만 메모리 누수라는 문제점이 있다.
# _values 딕셔너리는 프로그램의 수명동안
# __set__에 전달된 모든 Exam 인스턴스의 참조를 저장한다.
# 결국 인스턴스의 참조 개수가 절대로 0이 되지 않아 가비지 컬렉터가 정리하지 못하게된다.

# 파이썬의 내장 모듈 weakref 를 사용하면 이 문제를 해결할 수 있다.
# 이 모듈은 _values에 사용한 간단한 딕셔너리를 대체할 수 있는 WeakKeyDictionary 라는 특별한 메소드를 제공한다.
# WeakKeyDictionary 클래스 고유의 동작은 런타임에 마지막으로 남은 Exam 인스턴스의
# 참조를 갖고 있다는 사실을 알면 키 집합에서 Exam 인스턴스를 제거하는 것이다.
# 파이썬이 대신 참조를 관리해주고 모든 Exam 인스턴스가 더는 사용되지 않으면 _values 딕셔너리가 비어있게한다.

class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('0 ~ 100')
        self._values[instance] = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(first_exam.writing_grade)
print(second_exam.writing_grade)