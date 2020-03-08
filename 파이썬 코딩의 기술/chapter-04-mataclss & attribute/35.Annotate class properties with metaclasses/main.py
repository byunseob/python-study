# 메타클래스로 해당 클래스를 실제로 사용하기 전에 프로퍼티를 수정하거나 주석을 붙이는 기능 구현 가능


class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer(object):
    # 클래스속성
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


foo = Customer()
print(f'Before : {repr(foo.first_name)} , {foo.__dict__}')
foo.first_name = 'byunseob'
print(f'Before : {repr(foo.first_name)} , {foo.__dict__}')


class Meta(type):
    def __new__(cls, *args, **kwargs):
        for key, value in args[2].items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key

        class_ = type.__new__(cls, *args, **kwargs)
        return class_


class DatabaseRow(object, metaclass=Meta):
    pass


class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


foo = BetterCustomer()
print(f'Before : {repr(foo.first_name)} , {foo.__dict__}')
foo.first_name = 'byunseob'
print(f'Before : {repr(foo.first_name)} , {foo.__dict__}')

# 메타클래스를 이용하면 클래스가 완전히 정의되기 전에 클래스 속성을 수정할 수있다.
# 디스크립터와 메타클래스는 선언적 동작과 런타임 내부조사용으로 강력한 조합을 이룬다.
# 메타클래스와 디스크립터를 연계하여 사용하면 메모리 누수와 weakref 모듈을 모두 피할 수 있다.
