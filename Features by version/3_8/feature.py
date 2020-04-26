# Assignment expressions

"""
statement의 entry point 레벨에서, 해당 block scope에 대한 변수 정의

복잡성을 줄이고 가독성을 개선하는 명확한 사례로 바다코끼리 연산자 사용을 제한하십시오.

더 큰 표현식의 일부로 변수에 값을 대입하는 새로운 문법 := 이 있습니다.
바다코끼리의 눈과 엄니를 닮아서 "바다코끼리 연산자(the walrus operator)"라고 친근하게 알려져 있습니다.

이 예에서, 대입 표현식은 len()을 두 번 호출하지 않도록 합니다:
"""
import re
from datetime import date

a = range(11)

if (n := len(a)) > 10:
    print(f"List is too long ({n} elements, expected <= 10)")

input_data = [range(100)]

# Positional-only parameters
"""
다음 예에서, 매개 변수 a와 b는 위치 전용이며, c나 d는 위치나 키워드일 수 있으며, e나 f는 키워드 전용이어야 합니다:
"""


def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)


f(10, 20, 30, d=40, e=50, f=60)

# Debug support for f-strings

"""
f-문자열은 스스로 설명하는 표현식과 디버깅을 위해 =를 지원합니다.
"""

user = 'eric_idle'
member_since = date(1975, 7, 31)
print(f'{user=} {member_since=}')
# "user='eric_idle' member_since=datetime.date(1975, 7, 31)"
