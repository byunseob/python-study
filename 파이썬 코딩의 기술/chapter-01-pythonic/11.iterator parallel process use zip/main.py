# 파이썬 3에서 zip 은 지연 제너레이터로 이터레이터 두개 이상을 감싼다.
# zip 제너레이터는 각 이터레이터로 부터 다음 값을 담은 튜플을 얻어온다.


longest_name = None
max_letters = 0

names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]

for name, count in zip(names, letters):
    print(name)
    print(count)
    if count > max_letters:
        longest_name = name
        max_letters = count


# 입력 이터레이터들의 길이는 같아야한다.
# 감싼 이터레이터가 끝날 때 까지 튜플을 넘겨준다. 길이가 다르다면 zip 은 결과를 잘라낸다.
# zip으로 실행할 리스트의 길이가 같다고 확실할 수 없다면
# 내장 모듈의 itertools 의 zip_longest 를 사용
