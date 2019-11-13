# todo 예제 코드작성
# 입력 인수를 여러 번 순회하는 함수를 작성할때 주의
# 입력 인수가 이터레이터라면 소진한 이후에는 값을 잃어버리기 때문

numbers = [x for x in range(1000)]


def get_even(numbers_):
    for number in numbers_:
        if number % 2 == 0:
            yield number


def normalize(iter_):
    total = sum(iter_)  # 소진
    result = []
    for value in iter_:
        percent = 100 * value / total
        result.append(percent)
    return result


evens = get_even(numbers)
percentages = normalize(evens)
print(percentages)  # []

evens = get_even(numbers)
print(list(evens))  # 소진 [0, 2, 4, ...]
print(list(evens))  # []


# 이터레이터가 결과를 한번만 생성하기 때문
# StopIteration 예외를 일으킨 이터레이터나 제너레이터를 순회하면 결과가 없다.
# for 루프와 list 생성자, 파이썬 표준 라이브러리의 많은 함수는
# 정상적인 동작 과정에서 StopIteration 예외가 일어날 것이라고 기대한다.
# 이런 함수는 결과가 없는 이터레이터와 결과가 있엇지만 이미 소진한 이터레이터의 차이를 알려주지 않음.

# 이런 문제를 해결하려면 입력 이터레이터를 명시적으로 소진하고
# 복사본을 리스트에 적재하면 되지만 메모리 낭비가 있다.

# 이 문제를 피하는 한 가지 방법은 호출될 때마다 새 이터레이터를 반환하는 함수를 만드는 것이다.

def normalize(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result


# 새 이터레이터를 생성하는 람다 표현식을 넘겨주면 된다.
percentages = normalize(lambda: get_even(numbers))
print(percentages)  # [0.0 , 0.00 ....]


# 이터레이터 프로토콜 #
# 같은 결과를 얻는 더 좋은 방법은 이터레이터 프로토콜을 구현한
# 새 컨터에너 클래스를 제공하는 것이다.

# 이터레이터 프로토콜은 파이썬의 for 루프와 관련 표현식이 컨테이너 타입의 콘텐츠를 탐색하는 방법을 난타낸다.
# 파이썬은 for x in foo 같은 문장을 만나면 실제로는 iter(foo)를 호출한다.
# 내장 함수 iter 는 특별한 메서드인 foo.__iter__ 를 호출한다.
# __iter__ 메소드는 (__next__ 라는 특별한 메소드를 구현하는) 이터레이터 객체를 반환해야 한다.
# for 루프는 이터레이터를 모두 소진할 때까지 이터레이터 객체에 내장 함수 next 를 계속 호출한다.

# 복잡해 보이지만 클래스의 __iter__메소드를 제너레이터로 구현하면 된다.

class ReadEvens(object):
    def __init__(self, number):
        self.numbers = range(number)

    def __iter__(self):
        for number in self.numbers:
            if number % 2 == 0:
                yield number


def normalize(iter_):
    total = sum(iter_)  # 소진
    result = []
    for value in iter_:
        percent = 100 * value / total
        result.append(percent)
    return result


evens = ReadEvens(100)
percentages = normalize(evens)
print(percentages)  # [0.0 , 0.00 ....]


# 이 코드가 동작하는 이유는 normalize 의 sum 새 메서드가 새 이터레이터
# 객체를 할당하려고 ReadEvens.__iter__ 를 호출하기 때문이다.
# for 루프 도 두번째 이터레이터 객체를 할당할때 __iter__ 를 호출한다.
# 이 방법의 유일한 단점은 입력 데이터를 여러 번 읽는다는 점이다.

# 프로토콜에 따르면 내장 함수 iter 에 이터레이터를 넘기면 이터레이터 자체가 반환된다.
# 반면에 iter 에 컨테이너 타입 넘기면 매번 새 이터레이터 객체가 반환된다.

def normalize_defensive(iter_):
    if iter(iter_) is iter(iter_):  # 매번 이터레이터 객체가 반환되는지
        raise TypeError("Must supply a container")
    total = sum(iter_)  # 소진
    result = []
    for value in iter_:
        percent = 100 * value / total
        result.append(percent)
    return result


numbers = [1, 2, 3]  # 리스트도 이터레이터 컨테이너 이다.
percentages1 = normalize_defensive(numbers)
print(percentages1)
evens = ReadEvens(100)
percentages2 = normalize_defensive(evens)
print(percentages2)  # [0.0 , 0.00 ....]

# 입력 인수를 여러 번 순회하는 함수를 작성할 때 주의하자.
