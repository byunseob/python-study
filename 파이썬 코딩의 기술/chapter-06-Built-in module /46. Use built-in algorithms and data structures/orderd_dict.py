# 표준 딕셔너리는 정렬되어 있지 않다.
# 즉 같은 키와 값을 담은 dict 를 순회해도 다른 순서가 나올 수 있다.
# 이런 동작은 딕셔너리의 빠른 해시 테이블을 구현하는 방식이 만들어낸 뜻밖의 부작용이다.
from collections import OrderedDict, defaultdict
from random import randint

a = {}
a['foo'] = 1
a['bar'] = 2

# 파이썬 3.7 부터 표준 딕셔너리 dict 가 삽입 순서를 보존합니다.
# 무작위로 'b' 에 데이터를 추가해서 해시 충돌을 일으킴

while True:
    z = randint(20, 100)
    b = {}
    for i in range(z):
        b[i] = i
    b['bar'] = 2
    b['foo'] = 1

    for i in range(z):
        del b[i]

    if str(b) != str(a):
        break

print(a)
print(b)
print(f'Equal ? {a == b}')

# collections 모듈의 OrderedDict 클래스는 키가 삽입된 순서를 유지하는 특별한 딕셔너리 타입이다.
# OrderedDict 의 키를 순회하는 것은 예상가능한 동작이다.
#

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)

# collections 모듈의 defaultdict 클래스는 키가 존재하지 않으면 자동으로 기본값을 저장하도록 한다.
stats = defaultdict(int)
stats['my_counter'] += 1
print(stats)
