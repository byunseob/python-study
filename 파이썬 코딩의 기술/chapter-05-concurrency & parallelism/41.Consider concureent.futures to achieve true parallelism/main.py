# concurrent.futures 로 쉽게 접근할 수있는 내장 모듈 multiprocessing  을 사용하면
# 자식 프로세스로 추가적인 인터프리터를 실행하여 병렬로 여러 CPU 코어를 활용할 수있다.
# 이런 자식 프로세스는 주 인터프러터와는 별개이므로 전역 인터프리터 잠금 역시 분리된다.

# 각 자식은 CPU 코어 하나를 완전히 활용할 수 있다. 또한 주 프로세스와 연결되어 계산할 명령어를 받고 수행한 결과를 반환한다.
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from time import time


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % 1 == 0 and b % i == 0:
            return i


numbers = [(341312323, 56123136), (341212232, 81231236), (12532367, 766532134), (12532367, 766532134)]

start = time()
result = list(map(gcd, numbers))
end = time()
print(f"Took {end - start}")

# 여러 파이썬 스레드에서 이 코드를 실행하면 GIL 때문에 병렬로 여러 CPU 코어를 사용하지 못해서 속도가 개선되지 않는다.

start = time()
pool = ThreadPoolExecutor(max_workers=2)
result = list(pool.map(gcd, numbers))
end = time()
print(f"Took {end - start}")

# 위 결과는 스레드 풀을 시작하고 통신하는 데 드는 오버헤드 때문에 더 느리다

start = time()
pool = ProcessPoolExecutor(max_workers=2)
result = list(pool.map(gcd, numbers))
end = time()
print(f"Took {end - start}")

# 프로세스풀익스큐터 클래스(멀티프로세싱 모듈이 제공하는 저수준 구조를 이용해) 가 실제 하는일

# 1. numbers 입력 데이터에서 map 으로 각 아이템을 가져온다.
# 2. pickle  모듈을 사용하여 바이너리 데이터로 직렬화 한다.
# 3. 주 인터프리터 프로세스에서 직렬화한 데이터를 지역 소켓을 통해 자식 인터프리터 프로세스로 복사한다.
# 4. 자식 프로세스에서 pickle 을 사용하여 데이터를 파이썬 객체로 역직렬화 한다.
# 5. gcd  함수가 들어있는 파이썬 모듈을 임포트
# 6. 다른 자식 프로세스를 사용하여 병렬로 입력 데이터에 함수를 실행한다.
# 7. 결과를 다시 바이트로 직렬화
# 8. 소켓을 통해 바이트를 복사
# 9. 바이트를 부모 프로세스에 있는 파이썬 객체로 역직렬화
# 10. 마지막으로 여러 자식에 있는 결과를 반환용 리스트 한 개로 합친다.

# 멀티프로세싱의 비용은 부모와 자식 프로세스 간에 일어날 수밖에없는 모든 직렬화와 역직렬화 때문에 상당히 높다.
# 이런 이유로 고립되고 지렛대 효과가 큰 특정 유형의 작업에 적합하다.


