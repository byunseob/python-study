# 제너레이터를 사용하는 방법이 누적된 결과의 리스트를 반환하는 방법보다 이해하기에 명확하다.
# 제너레이터에서 반환한 이터레이터는 제너레이터 함수의 본문에 있는 yield 표현식에 전달된 값들의 집합이다.
# 제너레이터는 모든 입력과 출력을 메모리에 저장하지 않으므루 입력값의 양을 알기 어려울 때도 연속된 출력을 만들수 있다.


def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


result = list(index_words_iter("hi my name is Byunseob"))
print(result)
