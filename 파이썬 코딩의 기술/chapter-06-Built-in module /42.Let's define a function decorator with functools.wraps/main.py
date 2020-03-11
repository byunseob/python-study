# 데코레이터는 감싸고 있는 함수를 호출하기 전이나 후에 추가로 코드를 실행하는 기능을 갖췄다.
# 이 기능으로 입력 인수와 반환 값을 접근하거나 수정할 수 있다.
from functools import wraps


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args}, {kwargs}) -> {result}")

        return result

    return wrapper


@trace
def fibonacci(n):
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci(3)
print(fibonacci)  # <function trace.<locals>.wrapper at 0x10e24cd40>
help(fibonacci)


def trace(func):
    @wraps(func)  # 데코레이터를 작성하는데 이용하는 데코레이터 이 데코레이터를 wrapper 함수에 적용하면 내부 함수에 있는 중요한 메타데이터가 모두 외부 함수로 복사된다.
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args}, {kwargs}) -> {result}")

        return result

    return wrapper


@trace
def fibonacci(n):
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci(3)
print(fibonacci)  # <function trace.<locals>.wrapper at 0x10e24cd40>
help(fibonacci)
