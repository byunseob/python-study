# comprehesion 이란 iterable 한 오브젝트를 생성하기 위한 방법중 하나로 파이썬에서 사용할 수 있는 유용한 기능중 하나이다.

# List Comprehension (LC)
# Set Comprehension (SC)
# Dict Comprehension (DC)
# Generator Expression (GE)
# Generator 의 경우 comprehension 과 형태는 동일하지만 특별히 expression이라고 부른다.

# 한 리스트에서 다른 리스트를 만들어내는 간결한 문법
# 이 문법을 사용한 표션힉을 리스트 컴프리헨션 이라고 함.

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x ** 2 for x in a if x % 2 == 0]
print(squares)
# [4, 16, 36, 64, 100]

# 리스트 컴프리헨션을 사용하면 조건식으로 아이템을 간편하게 걸러 낼 수 있음



# 출처 https://mingrammer.com/introduce-comprehension-of-python/
