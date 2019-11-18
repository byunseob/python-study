# 파이썬 내장 API 의 상당수에는 함수를 넘겨서 동작을 사용자화하는 기능이 있다.
# API 는 이런 훅(hook)을 이용해 사용자가 작성한 코드를 실행 중에 호출한다.
from collections import defaultdict

names = ['javascript', 'python', 'java']
names.sort(key=lambda x: len(x))
print(names)


# 다른 언어에서라면 훅을 추상 클래스로 정의할 것이라고 예상할 수도 있다.
# 하지만 파이썬의 훅중 상당수는 인수와 반환값을 잘 정의해놓은 단순히 상태가 없는 함수다.
# 함수는 클래스보다 쉽고 정의하기도 간단해서 훅으로 쓰기에 이상적이다.

# defaultdict 클래스의 동작을 사용자화 예제
# defaultdict 에 넘길 함수는 딕셔너리에서 찾을 수없는 키에 대응할 기본값을 반환해야한다.

def log_missing():
    print('key added')
    return 0


current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After:', dict(result))


# log_missing 같은 함수를 넘기면 결정 동작과 부작용을 분리하므로
# API 를 쉽게 구축하고 테스트할 수있다.

# 기본값 훅 을 defaultdict 에 넘겨서 찾을 수없는 키의 총 개수를 세는 예제

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)

    for key, amount in increments:
        result[key] += amount

    return result, added_count


# defaultdict 은 missing 후크가 상태를 유지한다는 사실을 모르지만
# increment_with_report 함수를 실행하면 튜플의 요소로 기대한 개수인 2를 얻는다.
# 이는 간단한 함수를 인터페이스 용으로 사용할때 얻을 수 있는 또 다른 이점이다.
# 클로저 안에 상태를 숨기면 나중에 기능을 추가하기도 쉽다.

result, count = increment_with_report(current, increments)
assert count == 2


# 상태 보존 후크용으로 클로저를 정의할 때 생기는 문제는 상태가 없는 함수의 예제보다
# 이해가기 어렵다는 점이다.

# 보존할 상태를 캡슐화하는 작은 클래스를 정의하는 예제

class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# 파이썬의 일급함수 덕분에 객체로 CountMissing.missing 메소드를
# 직접 참조해서 defaultdict 의 기본값 후크로 넘기기

counter = CountMissing()
result = defaultdict(counter.missing, current)

for key, amount in increments:
    result[key] += amount

assert counter.added == 2


# 헬퍼 클래스로 상태 보존 클로저의 동작을 제공하는 방법이 앞에서
# increment_wit_report 함수를 사용한 방법보다 명확하다.
# 그러나 CountMissing 클래스 자체만으로는 용도가 무엇인지 바로 이해하기 어렵다.
# defaultdict 와 연계해서 사용한 예를 보기 전까지는 이 클래스가 수수께끼로 남는다.

# __call__
# 파이썬에서는 클래스에 __call__이라는 특별한 메소드를 정의해서 이런 상황을 명확하게 할 수있다.
# __call__메소드는 객체를 함수처럼 호출할 수 있게 해준다.
# 또한 내장함수 callable 이 이런 인스턴스에 대해서는 True 를 반환하게 만든다.

class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
counter()
assert callable(counter)

counter = BetterCountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

# 이 예제가 CountMissing.missing 예제보다 명확하다
# __call__ 메소드는 (API 훅처럼) 함수 인수를 사용하기 적합한 위치에 클래스의 인스턴스를
# 사용할 수 있다는 사실을 드러낸다

# 이 코드를 처음 보는 사람을 클래스의 주요 동작을 책임지는 진입점 으로 안내하는 역활도 한다.
# 클래스의 목적이 상태 보존 클로저로 동작하는 것이라는 강력한 힌트를 제공한다.

# !무엇보다도 __call__을 사용할 때 defaultdict 은 여전히 무슨 일이 일어나는지 모른다.
# defaultdict 에 필요한 건 기본값 후크용 함수뿐이다.

