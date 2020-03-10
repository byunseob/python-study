from collections import deque
from queue import Queue
from threading import Lock, Thread
from time import sleep


def download(number):
    for _ in range(10):
        pass


def resize(number):
    for _ in range(10):
        pass


def upload(number):
    for _ in range(10):
        pass


class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.worker_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.worker_done += 1


download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()

threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(10000):
    download_queue.put(object())

while len(done_queue.items) < 10000:
    print(f'working... {len(done_queue.items)}')

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f"Processed {processed} items after polling {polled} times")

# IndexError 예외를 잡는 부분이 매우 많이 실행되고 있음

# 작업 수행 함수의 실행 속도가 제각각이면 초기 단계가 후속 단계의 진행을 막아 파이프라인이 정체될 수 있다.
# 후속 단계{에서 처리할 것이 없어서 지속적으로 새 작업을 가져오려고 짧은 주기로 입력 큐를 확인하게 된다.
# 결국 작업 스레드는 유용한 작업을 전혀 하지 않으면서 CPU 시간을 낭비하게 된다.

# 이 문제 말고도 3개의 문제가 더 있다.
# 1. 입력 작업을 모두 완료 했는지 판단하려면 done_queue 에 겨로가가 모두 쌓일 때 까지 기다려야 한다.
# 2. Worker 의 run 메서드는 루프에서 끊임없이 실행된다. 루프를 빠져나오도록 작업 스레드에 신호를 줄 방버이 없다.
# 3. 최악의 문제로 파이프라인이 정체되면 프고그램이 제멋대로 고장이 날 수 있다.
# 첫 번째 단계는 빠르게 진행하지만 두 번째 단계는 느리게 진행하면 첫 번째 단계와 두 번째 단계를 연결하는 큐의 크기가 계속 증가한다.
# 두 번째 단계는 큐가 증가하는 속도를 따라잡지 못한다. 충분한 시간과 충분한 입력 데이터가 있따면 프로그램은 결국 메모리 부족으로 죽는다.


# Queue 는 새 데이터가 생길 때 까지 get 메서드가 블록되게 하여 작업 스레드가 계속해서 데이터가 있는지 체크하는 상황을 없애준다.

queue = Queue()


def consumer():
    print("Consumer waiting")
    queue.get()
    print("Consumer done")


thread = Thread(target=consumer)
thread.start()

# 쓰레드가 처음으로 실행할 때도 Queue 인스턴스에 아이템이 들어가서 get 메서드에서 반환할 아이템이 생기기 전에는 마치지 못한다.

print("Producer putting")
queue.put(object())
thread.join()
print("Producer done")

# 파이프라인 정체 문제를 해결하려면 두 단계 사이에서 대기할 작업의 최대 개수를 Queue 에 설정해야 한다.
# 큐가 이미 이 버퍼 크기만큼 가득 차 있으면 put 호출이 블록된다.


queue = Queue(1)  # 크기가 1인 버퍼


def consumer():
    sleep(0.1)
    queue.get()
    print("Consumer got 1")
    queue.get()
    print("Consumer got 2")


thread = Thread(target=consumer)
thread.start()

queue.put(object())
print("Producer put 1")
queue.put(object())
print("Producer put 2")
thread.join()
print("Producer done")

# Queue 클래스는 task_done 메서드로 작업 진행을 추적할 수도 있다.
# 작업 진행을 추적하면 특정 단계의 입력 큐가 빌 때까지 기다릴 수 있으므로 파이프라인의 끝에서 done_queue 를 폴링하지 않아도 된다.

print("####################")
in_queue = Queue()


def consumer():
    print("Consumer waiting")
    work = in_queue.get()
    print("Consumer working")
    print("Consumer done")
    in_queue.task_done()


Thread(target=consumer).start()

in_queue.put(object())
print("Producer waiting")
in_queue.join()
print("Producer done")


# close 메서드를 정의하여 더는 입력 아이템이 없음을 알리는 특별한 아이템을 큐에 추가

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()

            try:
                if item is self.SENTINEL:
                    return  # 스레드 종료
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()

print(f"{done_queue.qsize()} items finished")
