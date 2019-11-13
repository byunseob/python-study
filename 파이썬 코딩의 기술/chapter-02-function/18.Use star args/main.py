# 선택적인 위치 인수를 받게 만들면 함수 호출을 더 명확하게 할 수있다.


def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print(f"{message} {values_str}")


log("T", [1, 2])
log("T", [])


def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print(f"{message} {values_str}")


log("T", 1, 2)
log("T")

# 가변 개수의 위치 인수를 받는 방법에는 두 가지 문제가 있다.
# 가변 인수가 함수에 전달되기에 앞서 항상 튜플로 반환된다는 점이다.
# 이는 함수를 호출하는 쪽에서 제너레이터에 * 연산자를 쓰면 제너레이터가
# 모두 소진될 때까지 순회딤을 의미한다.
# *args 를 받는 함수는 인수 리스트에 있는 입력의 수가 적다는 사실을 아는 상황에서
# 가장 좋은 방법이다. 이런 함수는 많은 리터럴이나 변수 이름을 한꺼번에 넘기는 호출에 이상적이다.

# 추후에 호출 코드를 모두 변경하지 않고서는 새 위치 인수를 추가할 수없다는 점이다.

