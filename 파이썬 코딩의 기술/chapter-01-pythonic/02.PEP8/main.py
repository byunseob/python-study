# PEP 8 스타일 가이드는 매우 중요하다
# 예외의 상황
# 규칙을 적용한 코드가 (규칙을 숙지한 사람 눈에도) 읽기 어려운 경우
# 일관성을 지키려고 한 수정이 다른 규칙을 어기는 경우
# 일관성 있는 스타일로 작성하여 나중에 수정을 용이하게 하자


# whitespace
# 공백은 문법적 의미가 있다
# 파이썬 프로그래머느 코드의 명료성 때문에 화이트스페이스에 민감
# 1. 탭대신 스페이스로 들여쓰기
# 2. 문법적으로 의미 있으면 스페이스바 4개의 들여쓰기
# 3. 한 줄의 문자 길이가 79자 이하여야 한다
# 4. 표현식이 길어 다음줄로 이어지면 일반적인 들여쓰기 수준에 추가로 스페이스 네 개를 사용
# 5. 한 파일 내에서 함수와 클래스는 빈 줄 두개로 구분
# 6. 클래스 에서 메서드는 빈 줄 하나로 구분
# 7. 리스트 인덱스, 함수 호출, 키워드 인 수할당에는 스페이스를 사용하지 않음
# 8. 변수 할당 앞뒤에 스페이스 하나만 사용

# naming
# 1. 함수, 변수, 속성은 lowercase_underscore 형식
# 2. _single_leading_underscore: 내부적으로 사용되는 변수를 일컫습니다
# 3. single_trailing_underscore_: 파이썬 기본 키워드와 충돌을 피하려고 사용합니다
# 4. __double_leading_underscore: 클래스 속성으로 사용되면 그 이름을 변경합니다
#    (ex. FooBar 에 정의된 __boo 는 _FooBar__boo 로 바뀝니다.) => *맹글링
# 5. __double_leading_and_trailing_underscore__: 마술(magic)을 부리는 용도로 사용되거나 사용자가 조정할 수 있는 네임스페이스 안의 속성을 뜻합니다.
#    이런 이름을 새로 만들지 마시고 오직 문서대로만 사용하세요.
#    (ex. __init__)
# 6. protected 인스턴스 속성은 _leading_underscore 형식
# 7. private 인스턴스 속성은 __double_leading_underscore 형식
# 8. 클래스와 예외는 CapitalizedWord 형식
# 9. 모듈 수준 상수는 ALL_CAPS 형식
# 10. 클래스의 인스턴스 메서드에서 첫 번째 파라미터(해당 객체를 참조)의 이름을 self 로 지정
# 11. 클래스 메서드에서는 첫 번째 파라미터(해당 클래스를 참조)의 이름을 cls 로 지정
# 12. 모듈(Module) 명은 짧은 소문자로 구성되며 필요하다면 밑줄로 나눕니다.
# 12_1. 모듈은 파이썬 파일(.py)에 대응하기 때문에 파일 시스템의 영향을 받으니 주의
# 12_2. C/C++ 확장 모듈은 밑줄로 시작

# Expressions and Statements
# 1. 긍정 표현식의 부정 (if not a is b) 대신에 인라인 부정 (if a is not b) 을 사용
# 2. 길이를 확인(if len(somelist) == 0)하여 빈값을 확인하지 않는다
#    if not somelist 를 사용하고, 빈 값은 암시적으로 False 가 된다고 가정한다
# 3. 비어있지 않은 값 에도 위와 같은 방식이 적용. 값이 비어 있지 않으면 if somelist 문이 암시적으로 True
# 4. 한 줄로 된 if 문, for 와 while 루프, except 복합문을 쓰지 않는다. 이런 문장은 여러 줄로 나눠서 명료하게 작성
# 5. 항상 파일의 맨 위에 import 문
# 6. 모듈을 임포트 할 때는 항상 모듈의 절대 이름을 사용, 현재 모듈의 경로를 기준으로 상대 경로된 이름을 사용하지 않는다
#    ex. bar 패키지의 foo 모듈을 임포트 하려면 그냥 import foo 가 아닌 from bar import foo 라고 해야 한다
# 7. 상대적인 임포트를 해야한다면 명시적인 구문을 써서  from .import foo 라고 한다
# 8. 임포트는 표준 라이브러리, 서드파티, 자신이 만든 모듈 섹션 순으로 구분해야한다
#    각각의 하위 섹션에서는 알파벳 순서로 임포트한다

# Programming Recommendations
# 1. 코드는 될 수 있으면 어떤 구현(PyPy, Jython, IronPython등)에서도 불이익이 없게끔 작성되어야 합니다
# 2. None 을 비교할때는 is나 is not 만 사용합니다
# 3. 클래스 기반의 예외를 사용하세요
# 4. 모듈이나 패키지에 자기 도메인에 특화된(domain-specific)한 기반 예외 클래스(base exception class)를 빌트인(built-in)된 예외를 서브클래싱해 정의하는게 좋습니다.
#    이 때 클래스는 항상 문서화 문자열을 포함해야 합니다
# class MessageError(Exception):
#     """Base class for errors in the email package."""
# 5. raise ValueError('message')가 (예전에 쓰이던) raise ValueError, 'message' 보다 낫습니다
# 6. 예외를 except:로 잡기보단 명확히 예외를 명시합니다
#    ex. except ImportError:
# 7. try: 블록의 코드는 필요한 것만 최소한으로 작성합니다
# 8. string 모듈보다는 string 메소드를 사용합니다. 메소드는 모듈보다 더 빠르고, 유니코드 문자열에 대해 같은 API를 공유합니다
# 9. 접두사나 접미사를 검사할 때는 startswith()와 endwith()를 사용합니다
# 10. 객체의 타입을 비교할 때는 isinstance()를 사용합니다
# 11. 불린형(boolean)의 값을 조건문에서 ==를 통해 비교하지 마세요


# 맹글링 - 맹글링이란, 컴파일러나 인터프리터가 변수/함수명을 그대로 사용하지 않고 일정한 규칙에 의해 변형시키는 것을 말한다.

# https://spoqa.github.io/2012/08/03/about-python-coding-convention.html 참조
# https://mingrammer.com/underscore-in-python/ 참조
