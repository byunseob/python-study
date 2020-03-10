# 파이썬의 표준 구현을 CPython 이라고 한다.
# CPython 은 파이썬 프로그램을 두 단계로 실행한다.
# 먼저 소스 텍스트를 바이트코드로 파싱하고 컴파일 한다.
# 스택 기반 인터프리터로 바이트 코드를 실행한다.
# 바이트 코드 인터프리터는 파이썬 프로그램이 실행되는 동안 지속되고, 일관성을 유지한다.

# GIL 은 상호 배제 잠금(mutex) 이며 CPython 이 선점형 멀티스레딩의 영향을 받지 않게 막아준다.
import select
from time import time


def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [654363, 4356356, 6543613, 9315613]
start = time()

for number in numbers:
    list(factorize(number))
end = time()
print(f"Took {end - start} sec")

from threading import Thread


class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time()
print(f"Took {end - start} sec")


# 순서대로 인수 분해할 때보다 더 많은 시간이 걸렸다.

# CPython 이 멀티코어를 활용하게 하는 방법은 여러 가지지만, 표준 Thread 클래스에는 동작하지 않는다.
# 쓰레드의 장점
# 1.쓰레드를 이용하면 함수를 마치 병렬로 실행하는 것처럼 해주는 일을 파이썬에 맡길 수 있다
#   비록 GIL 때문에 한 번에 한 스레드만 진행하지만 CPython 은 파이썬 스레드가 어느 정도 공평하게 실행됨을 보장하기 때문이다.
# 2.특정 유형의 시스템 호출을 수행할 때 일어나는 블로킹 I/O 를 다루기 위해서다.
#  시스템 호출은 파이썬 프로그램에서 외부 환경과 대신 상호작용하도록 컴퓨터 운영체제에 요청하는 방법이다.
#  블로킹 I/O로는 파일 읽기/쓰기, 네트워크와의 상호 작용, 디스플레이 같은 장치와의 통신 등이 있다.
#  쓰레드는 운영체제가 이런 요청에 응답하는 데 드는 시간을 프로그램과 분리하므로 블로킹 I/O 를 처리할 때 유용하다.


def slow_systemcall():
    select.select([], [], [], 0.1)


start = time()
for _ in range(5):
    slow_systemcall()  # 메인 스레드는 시흐템 호출 select  때문에 실행이 막혀 있다.
end = time()
print(f"Took {end - start} sec")

# 블로킹 I/O 를 사용하면서 동시에 연산도 해야 한다면 시스템 호출을 스레드로 옮기는 방안을 고려해야 한다.

start = time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    print(index)


for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time()
print(f"Took {end - start} sec")

# 병렬 처리 시간은 직렬 처리 시간보다 5배나 짧다.
# 이 예제는 시스템 호출이 GIL 의 제약을 받지만 여러 파이썬 쓰레드를 모두 병렬로 실행할 수 있음을 보여준다.
# GIL 은 파이썬 코드가 병렬로 실행하지 못하게 한다. 하지만 시스템 호출에서는 이런 부정적인 영향이 없다.
# 이는 파이썬 쓰레드가 시스템 호출을 만들기 전에 GIL 을 풀고 시스템 호출의 작업이 끝나는 대로 GIL 을 다시 얻기 때문이다.
# 쓰레드 이외에도 내장 모듈 asyncio 처럼 블로킹 I/O 를 다루는 다양항 순다닝 있고, 이런 대체 수단에는 중요한 이점이 있다.
# 하지만 이런 옵션을 선택하면 실행 모델에 맞춰서 코드를 재작성 해야하는 추가 작업이 필요하다.
# 스레드를 이용하는 방법은 프로그램의 수정을 최소화 하면서도 블로킹 I/O 를 병렬로 수행하는 가장 간단한 방법이다
