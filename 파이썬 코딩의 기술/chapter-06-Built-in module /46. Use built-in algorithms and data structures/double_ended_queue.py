# 더블 엔디드 큐
# collections 모듈의 deque 클래스는 더블 엔디드 큐다.
# deque 는 큐의 처음과 끝에서 아이템을 삽입하거나 삭제할때 항상 일정한 시간이 걸리는 연산을 제공한다.
# 이와 같은 기능은 선입선출 큐를 만들때 이상적이다.
from collections import deque

fifo = deque()
fifo.append(1)
fifo.append(2)
x = fifo.popleft()
print(x)
x = fifo.popleft()
print(x)

# 내장 타입 list 도 큐와 마찬가지로 순서가 있는 아이템 시퀀스를 담는다
# 일정한 시간 내에 리스트의 끝에 서 아이템을 삽입하거나 삭제할 수 있다.
# 하지만 리스트의 시작 부분에서 아이템을 삽입하거나 삭제하는 연산에는 선형적 시간이 걸리므로 deque 의 일정한 시간보다 느리다.

