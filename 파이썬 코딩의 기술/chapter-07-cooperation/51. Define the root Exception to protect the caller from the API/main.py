# 일반적으로 API 용으로는 자신만의 예외 계층을 정의하는 방법이 표준 라이브러리용 보다 강력하다.
# 예외 계층을 정의하려면 모듈 내에서 루트 Exception 을 제공하면 된다.
# 그런 다음 해당 모듈에서 일어나는 다른 예외가 모두 루트 예외로부터 상속받게 한다.

class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class InvalidDensityError(Error):
    """There was problem with a provided density value."""

# 모듈에 루트 예외를 두면 API 사용자들이 목적을 두고 일으킨 모든 예외를 잡아낼 수 있다.
# 예를 들어 API 사용자는 루트 예외를 잡아내는 try/except 문으로 함수를 호출할 수 있다.


# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.Error as e:
#     logging.error(f'Unexpected error {e}')

# 이 try/except 는 API 의 예외가 너무 멀리 퍼져나가서 호출하는 프로그램을 중단하는 일을 막는다
# 이 구문은 호출하는 코드를 API 로부터 보호한다.
# 이런 보호는 세가지 우용한 효괄르 낸다.

# 1. 루트 예외가 있으면 호출자가 API 를 사용할 때 문제점을 이해할 수 있다.
#  호출자가 API 를 올바르게 사요한다면 의도적으로 일으킨 다양한 예외를 잡아낼 수 있어야 한다.
#  그러한 예외를 처리할 수 없다면 여러분이 작성한 모듈의 루트 예외를 잡아서 보호하는 except 블록까지 전파된다.
#  이 except 블록은 API 사용자가 예외를 주목하게 하여 해당 예외 타입을 적절히 처리하는 코드를 추가하게 만든다.


# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.InvalidDensityError as e:
#     weight = 0
# except my_module.Error as e:
#     logging.error(f'Bug in the calling code {e}')


# 2. API 모듈의 코드에 있는 버그를 찾는데 도움이 된다.
# 코드에서 모듈 계층안에 정의한 예외만 의도적으로 일으킨다면 해당 모듈에서 일어난 다른 타입의 예외는 모두 의도하지 않은 것이 틀림없다.
# 이런 예외는 API 코드에 있는 버그다.
# try/except 문을 사용한다고 해서 API 모듈의 코드에 있는 버그로 부터 API 사용자들을 보호하지는 못한다.
# API 사용자를 보호하려면 호출자가 파이썬의 Exception 기반 클래스를 잡아내는 다른 except 블록을 추가해야 한다.


# try:
#     weight = my_module.determine_weight(1, -1)
# except my_module.InvalidDensityError as e:
#     weight = 0
# except my_module.Error as e:
#     logging.error(f'Bug in the calling code {e}')
# except Exception e:
#     logging.error(f'Bug in the API code {e}')

# 3. API 의 미래를 대비할 수 있다.
# 시간이 지나 특정 환경에서 더 구체적인 예외를 제공하려고 API 를 확장할 수도 있다.
# 예를 들어 밀도를 음수로 넘기는 오류상황을 알리는 Exception 서브클래스를 추가할 수도 있다.

class NegativeDensityError(InvalidDensityError):
    """A provied density value was negative."""


# 구체적인 예외는 이런 일반적인 예외로부터 상속해서 만든다.
# 각 중간 예외는 루트 예외처럼 동작한다.

