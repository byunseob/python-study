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
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
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
