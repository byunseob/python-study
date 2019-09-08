# 시퀀스 슬라이싱
# some[start:end]
# start 인덱스는 포함 end 인덱스는 제외
sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print('From 0 to 5:', sequence[:5])
print('Last 5', sequence[-5:])

# 아래와 같은 의미가 분명한 슬라이싱 형태를 사용권장
# sequence[:]  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# sequence[:5]  # [0, 1, 2, 3, 4]
# sequence[:-1]  # [0, 1, 2, 3, 4, 5, 6, 7, 8]
# sequence[4:]  # [4, 5, 6, 7, 8, 9]
# sequence[-3:]  # [7, 8, 9]
# sequence[2:5]  # [2, 3, 4]
# sequence[2:-1]  # [2, 3, 4, 5, 6, 7, 8]
# sequence[-3:-1]  # [7, 8]

# 슬라이싱은 인덱스가 리스트의 범위를 벗어나도 적절한 처리
print(sequence[:30])  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 슬라이싱의 결과는 완전히 새로운 리스트이다.
# 원본 리스트에 들어있는 객체에 대한 참조는 유지된다.
# 하지만 슬라이스 한 결과를 수정해도 원본리스트에 아무런 영향을 미치지 않는다.

a = [1, 2]
b = a[:]
print(b == a)  # True # value check
print(a is b)  # False # reference check
