# PEP 257 참고

# 모듈 문서화
# 이 docstring 의 목적은 모듈과 모듈의 내용에 대한 소개다.
# docstring 의 첫 번째 줄은 모듈의 목적을 기술하는 한 문장으로 구성해야 한다.
# 그 이후의 문단은 모듈의 모든 사용자가 알아야하는 모듈의 동작을 자세히 설명한 내용을 포함한다.
# 또한 모듈의 docstring 은 모듈내의 중요클래스나 함수를 강죠하는 중요한 부분이다.

# example

# words.py
"""Library for testing words for various linguistic patterns.

Testing how words telate eto each other can be tricky sometimes!
This module....

Available functions:
- palindrome : Determine if a word is a palindrome
....
"""


# 클래스 문서화
# 첫 번째 줄은 클래스의 목적을 기술하는 한 문장으로 구성한다.
# 그 이후의 문단에는 클래스의 동작과 관련해 중요한 내용을 기술한다.
# 클래스의 중요한 공개 속성과 메서드는 클래스 수준 docstring 에서 강조해야 한다.
# 또한 서브클래스가 보호 속성, 슈퍼릌래스의 메서드와 올바르게 상호 작용하는 방법을 안내해야 한다.

class Player(object):
    """Represents a player of game.

    SubClasses may override the 'tick' method to provide custom animations for ...

    Public attributes:
    - power : Unused power-ups (float between 0 and 1).
    ...

    """

# 함수 문서화
# 각 공개 함수와 메서드에는 docstring 이 있어야 한다.
# 첫 번째 줄은 함수가 수행하는 일을 한 문장으로 설명한다.
# 그 다음의 문단에서는 함수의 특별한 동작이나 인수에 대해 설명한다.
# 반환 값도 언급해야 한다.
# 호출하는 쪽에서 함수 인터페이스의 일부로 처리해야 하는 예외도 설명해야 한다.


def find_anagrams(word, dictionary):
    """Find all anagrams for a word.

    This function donly runs as fast as the test for membership in the ....


    Args:
        word: String of the target word.
        dictionary: Container with all string that are ...

    Returns:
        List of anagrams that were found.
    """

