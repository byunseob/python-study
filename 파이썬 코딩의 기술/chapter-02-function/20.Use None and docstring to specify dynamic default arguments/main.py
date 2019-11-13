# 키워드 인수의 기본값으로 비정적 타입을 사용해야 할 때도 있다.
from datetime import datetime
from time import sleep


def log(message, when=datetime.now()):
    print(f"{when} {message} ")


log("Hi")  # 2019-11-14 02:50:02.163600 Hi
sleep(1)
log("Hi")  # 2019-11-14 02:50:02.163600 Hi


# datetime.now 는 함수를 정의할 때 딱 한번만 실행되므로 타임 스태프가 동일하게 출력된다.
# 기본 인수의 값은 모듈이 로드될 때 한 번만 평가 되며 보통 프로그램이 시작할 때 일어난다.
# 이 코드를 담고 있는 모듈이 로드된 후에는 기본 인수인 datetime.now 를 다시 평가하지 않는다.

# 파이썬에서 결과가 기대한 대로 나오게 하려면
# 기본값을 None 으로 설정하고 docstring 으로 실제 동작을 문서화 하는게 관례다

def log(message, when=None):
    """Log a message with a timestamp.

    :param message: Message to print
    :param when: datetime of when the message occurred.
    :return:
    """

    when = datetime.now() if when is None else when
    print(f"{when} {message} ")

# 기본 인수 값으로 None 을 사용하는 방법은 인수가 수정가능 할 때 특히 중요하다.
# 값이 동적인 키워드 인수에는 기본값으로 None 을 사용하자.
# 그리고 나서 함수의 docstring 에 실제 기본 동작을 문서화하자.
