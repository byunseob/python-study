# 힙은 우선순위 큐를 유지하는 유용한 자료구조다.
# heapq 모듈은 표준 list 타입으로 힙을 생성하는 heappush, heappop, nsmallest 같은 함수도 제공한다.

# 임의의 우선순위를 가지는 아이템을 어떤 순서로도 힙에 삽입할 수 있다.
from heapq import heappush, heappop, nsmallest

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 2)

print(heappop(a), heappop(a), heappop(a), heappop(a))

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 2)

assert a[0] == nsmallest(1, a)[0] == 2

# list 의 sort 메서드를 호출하더라도 힙의 불변성이 유지된다.
print(f'Before : {a}')
a.sort()
print(f'After : {a}')
print(heappop(a), heappop(a), heappop(a), heappop(a))

# 이러한 각 heapq 연산에 걸리는 시간은 리스트의 길이에 비례하여 로그 형태로 증가한다.
# 표준 파이썬 리스트로 같은 동작을 수행하면 시간이 선형적으로 증가한다.
