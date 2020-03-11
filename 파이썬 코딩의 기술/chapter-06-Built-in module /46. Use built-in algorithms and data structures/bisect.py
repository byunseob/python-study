# list 에서 아이템을 검색하는 작업은 index 메서드를 호출할 때 리스트의 길이에 비례한 선형적 시간이 걸린다.
from _bisect import bisect_left

x = list(range(10 ** 6))
i = x.index(991234)

# bisect_left 같은 bisect 모듈의 함수는 정렬된 아이템 시퀀스를 대상으로 한 효율적인 바이너리 검색을 제공한다.
# bisect_left 가 반환한 인덱스는 시퀀스에 들어간 값의 삽입 지점이다.

i = bisect_left(x, 991234)
print(i)

# 바이너리 검색의 복잡도는 로그 형태로 증가한다. 다시 말해 아이템 백만 개를 담은 리스트를 bisect 로 검색할 때
# 걸리는 시간은 아이템 14개를 담은 리스트를 index 로 순차 검색할 떄 걸리는 시간과 거의 같다.


