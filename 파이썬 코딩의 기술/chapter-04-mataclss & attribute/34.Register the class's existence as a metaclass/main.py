# 메타클래스를 사용하여 프로그램에 있는 타입을 자동으로 등록 할 수 있다.
# 등록은 간닥한 식별자를 대응하는 클래스에 맵핑하는 역방향 조회를 수행할 때 유용하다.
import json


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serializable(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'


point = Point2D(5, 3)
print(f'Object : {point}')
print(f'Serialized : {point.serializable()}')


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterPoint2D({self.x}, {self.y})'


point = BetterPoint2D(5, 3)
print(f'Before : {point}')
data = point.serializable()
print(f'Serialized : {data}')
after = BetterPoint2D.deserialize(data)
print(f'After : {after}')


class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })

    def __repr__(self):
        return f'BetterSerializable({self.args})'


registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y


register_class(EvenBetterPoint2D)

point = EvenBetterPoint2D(5, 3)
print(f'Before : {point}')
data = point.serialize()
print(f'Serialized : {data}')
after = deserialize(data)
print(f'After : {after}')


class Meta(type):
    def __new__(cls, *args, **kwargs):
        class_ = type.__new__(cls, *args, **kwargs)
        register_class(class_)
        return class_


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z


v3 = Vector3D(10, -7, 3)
print(f'Before : {v3}')
data = v3.serialize()
print(f'Serialized : {data}')
after = deserialize(data)
print(f'After : {after}')
