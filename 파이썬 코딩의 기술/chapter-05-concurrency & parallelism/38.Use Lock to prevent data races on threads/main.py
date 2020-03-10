# 파이썬 인터프리터에서 자료 구조를 다루는 스레드 연산은 두 바이트 코드 명령어 사이에서 인터럽트 될 수 있다.
from threading import Thread, Lock


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


def run_thread(func, how_many, counter):
    threads = []

    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


how_many = 10 ** 5
counter = Counter()
run_thread(worker, how_many, counter)
print(f"Counter should be {5 * how_many} found {counter.count}")

# 결과가 다른이유
# 파이썬 인터프리터는 모든 스레드가 거의 동등한 처리 시간 동안 실행하게 하려고 실행중인 모든 스레드 사이에서 공평성을 유지한다.
# 파이썬은 공평성을 유지하려고 실행 중인 스레드를 잠시 중지하고 차례로 다른 스레드를 재개한다.
# 문제는 파이썬이 스레드를 정확히 언제 중지할지 모른다는 점이다.
# 스레드는 심지어 원자적 연산으로 보이는 작업 중간에서 멈출 수도 있다.

# += 연산자는 사실 파이썬이 보이지 않게 별도의 연산 세 개를 수행하게 한다.
# value = getattr(counter, 'count')
# result = value + offset
# setattr(counter, 'count', result)

# 카운터를 증가시키는 파이썬 스레드는 이 연산들 사이에서 중지될 수 있다.
# 만얀 연산이 끼어든 상황 때문에 value 의 이전 값이 카운터에 할당되면 문제가 된다.


# 파이썬은 이와 같은 데이터 경쟁과 다른 방식의 자료구조 오염을 막으려고 내장모듈 threading 에 강력한 도구들을 갖춰놓고 있다.

# 잠금을 이용하면 여러 스레드가 동시에 접근하더라도 Counter 클래스의 현재 값을 보호할 수 있다.
# 한번에 한 스레드만 잠금을 얻을 수 있다.


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


counter = LockingCounter()
run_thread(worker, how_many, counter)
print(f"Counter should be {5 * how_many} found {counter.count}")