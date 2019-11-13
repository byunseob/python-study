# 선택적인 위치 인수를 받게 만들면 함수 호출을 더 명확하게 할 수있다.


def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print(f"{message} {values_str}")


log("T", [1, 2])
log("T", [])
