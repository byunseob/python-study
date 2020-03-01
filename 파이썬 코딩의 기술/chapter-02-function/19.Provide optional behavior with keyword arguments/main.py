# 키워드 인수

# 위치 인수는 키워드 인수 앞에 지정해야 한다.
# function(test, value=123)

# 키워드 인수는 기본값을 설정할 수있다.

# 기존의 호출 코드와 호환성을 유지하면서도 함수의 파라미터를 확장할 수 있는 강력한 수단이 된다.


def force_keyword_arg(*, key, value):
    print(f"key:{key} value:{value}")


force_keyword_arg(key="key", value="value")
