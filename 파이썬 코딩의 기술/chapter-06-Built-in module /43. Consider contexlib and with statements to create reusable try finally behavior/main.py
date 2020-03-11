# 파이썬의 with 문은 코드를 특별한 컨텍스트 에서 실행함을 나태는 데 사용한다.

# contextlib 를 사용하면 객체와 함수를 with 문에 사용할 수 있게 만들기가 쉽다.
# 이 모듈은 간단한 함수를 with 문에 사용할 수 있게 해주는 contextmanager 데코레이터를 포함한다.
# 이 데코레이터를 이용하는 방법이  __enter__ 와 __exit__  라는 특별한 메서드를 담은 새 클래스를 정의하는 방법 보다 훨씬 쉽다.
import logging
from contextlib import contextmanager


def my_function():
    logging.debug("Some debug data")
    logging.error("Error log here")
    logging.debug("More debug data")


my_function()


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield  # with  블록의 내용이 실행되는 지점이다.
    finally:
        logger.setLevel(old_level)


with debug_logging(logging.DEBUG):
    print("Inside :")
    my_function()

print("After :")

my_function()

# with 문에 전달되는 컨텍스트 매니저에서 객체를 반환할 수도 있다.
# 이 객체는 복합문의 as 부분에 있는 지역 변수에 할당 된다.
# 이 기능을 이용하면 with  블록 안에 있는 코드에서 직접 컨텍스트와 상호 작용 할 수 있다.

with open('test.txt', 'w') as handle:
    handle.write('This is some data')


# 위와 같은 방법을 사용하는 것이 매번 수동으로 파일 핸들을 여닫는 방법보다 낫다.
# with 문에서 실행이 끝날 때 파일이 결국 닫힌다고 확신할 수 있다.

# 함수에서 as 타깃에 값을 제공할 수 있게 하려면, 컨텍스트 매니저에서 yield 를 사용하여 값을 넘겨주기만 하면 된다.

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug("This is my message")
