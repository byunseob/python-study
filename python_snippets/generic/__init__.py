import typing
from dataclasses import dataclass

T = typing.TypeVar('T')


@dataclass
class Person:
    name: str


@dataclass
class Response(typing.Generic[T]):
    data: typing.Optional[T]
    err: typing.Optional[Exception]


def A() -> Response[Person]:
    res = Response(data=Person(name='123'), err=None)
    return res


def B():
    res = A()
    print(res.data.name)


B()
