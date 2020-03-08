# 클래스에 __getattr__ 메소드를 정의하면 객체의 인스턴스 딕셔너리에서 속성을 찾을 수 없을 때마다 이 메소드가 호출된다.


class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, item):
        value = f'Value for {item}'
        setattr(self, item, value)
        return value


data = LazyDB()
print(f"Before : {data.__dict__}")  # Before : {'exists': 5}
print(f"foo : {data.foo}")  # foo : Value for foo
print(f"After : {data.__dict__}")  # After : {'exists': 5, 'foo': 'Value for foo'}


class LoggingLazyDB(LazyDB):
    def __getattr__(self, item):
        print(f'Called __getattr__({item})')
        return super().__getattr__(item)


data = LoggingLazyDB()
print(f"exists : {data.exists}")  # exists : 5
print(f"foo : {data.foo}")  # foo : Value for foo
print(f"foo : {data.foo}")  # foo : Value for foo __getattr__ 이 호출되지 않음


# __getattr__ 후크는 기존 속성에 빠르게 접근하려고 객체의 인스턴스 딕셔너리를 사용

# __getattribute__ 라는 또 다른 후크는 객체의 속성에 접근할 때마다 호출 되며, 해당 속성이 속성 딕셔너리에 있을 때도 호출된다.
# 이런 동작 덕분에 속성에 접근할 때마다 전역 트랜잭션 상태를 확인하는 작업 등에 쓸 수 있다.

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, item):
        print(f'Called __getattribute__({item})')
        try:
            return super().__getattribute__(item)
        except AttributeError:
            value = f'Value for {item}'
            setattr(self, item, value)
            return value


data = ValidatingDB()
print(f"exists : {data.exists}")
print(f"foo : {data.foo}")
print(f"foo : {data.foo}")


class MissingPropertyDB(object):
    def __getattr__(self, item):
        if item == 'bad_name':
            raise AttributeError(f'{item} is missing')


# data = MissingPropertyDB()
# data.bad_name

# __getattr__ 은 한번만 호출된다.
print("###########")
data = LoggingLazyDB()
print(f"Before : {data.__dict__}")
print(f"foo exists : {hasattr(data, 'foo')}")
print(f"After : {data.__dict__}")
print(f"foo exists : {hasattr(data, 'foo')}")

# __getattribute__ 은 hasattr 이나 getattr 을 호출 할 때마다 실행된다.
print("###########")
data = ValidatingDB()
print(f"foo exists : {hasattr(data, 'foo')}")
print(f"foo exists : {hasattr(data, 'foo')}")


class SavingDB(object):
    def __setattr__(self, key, value):
        super().__setattr__(key, value)


class LoggingSavingDB(SavingDB):
    def __setattr__(self, key, value):
        print(f'Called __setattr__({key}, {value})')
        super().__setattr__(key, value)


print("################")
data = LoggingSavingDB()
print(f'Before {data.__dict__}')
data.foo = 5
print(f'After {data.__dict__}')
data.foo = 7
print(f'Finally {data.__dict__}')


class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, item):
        print(f'Called __getattribute__ {item}')
        return self._data[item]


# data = BrokenDictionaryDB({'foo': 3})
# data.foo # 재귀호출되며 RecursionError

class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, item):
        data_dict = super().__getattribute__('_data')
        return data_dict[item]


data = DictionaryDB({'foo': 3})
data.foo

# __getattribute__ 와  __setattr__ 에서 인스턴스 속성에 직접 접근할 때 super 메소드를 사용하여 무한 재귀가 일어나지 않게 하자
