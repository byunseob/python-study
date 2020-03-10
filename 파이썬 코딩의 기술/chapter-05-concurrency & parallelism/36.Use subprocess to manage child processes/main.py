import os
import subprocess
from time import sleep, time

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE)

out, err = proc.communicate()  # 자식 프로세스의 출력을 읽어오고 자식 프로세스가 종료할 때까지 대기 한다.
print(out.decode('utf-8'))

# 자식 프로세스는 부모 프로세스와 파이썬 인터프러터와는 독립적으로 실행된다.
# 자식 프로세스의 상태는 파이썬이 다른 작업을 하는 동안 주기적으로 폴링된다.

proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None:
    print('Working....')
    for i in range(2):
        sleep(i)

print('Exit status', proc.poll())


# 부모에서 자식 프로세스를 떼어낸다는 건 부모 프로세스가 자유롭게 여러 자식 프로세스를 병렬로 실행할 수 있음을 의미한다.
# 자식 프로세스를 떼어내려면 모든 자식프로세스를 먼저 시작하면 된다.

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc


start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()

end = time()
print(f"Finished in {(end - start)} sec")


# 프로세스들이 순차적으로 실행했다면 전체 지연시간은 0.1초가 아니라 1초였을것이다.

# 파이썬 프로그램에서 파이프를 이용해 데이터를 서브프로세스로 보낸 다음 서브프로세스의 결과를 받아올 수도 있다.
# 이 방법을 이용하면 다른 프로그램을 활용하여 작업을 병렬로 수행할 수 있다.

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    proc.stdin.write(data)
    proc.stdin.flush()  # 자식 프로레스가 입력을 반드시 받게 함
    return proc


procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])


# 윤기스의 파이프 처럼 한 자식 프로세스의 결과를 다른 프로세스의 입력으로 연결하여 병렬 프로세스의
# 체인을 생성 할 수도 있다.

def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)
    return proc


input_procs = []
hash_procs = []

for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

# 자식 프로세스들이 시작하면 이들 사이의 I/O는 자동으로 일어난다.

for proc in input_procs:
    proc.communicate()

for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())


# 자식 프로세스가 종료되지 않거나 입력 또는 출력 파이프에서 블록될 염려가 있다면
# communicate 메서드에 timeout 파라미터를 사용하자.
# 자식 프로세스가 일정 시간 내 응답을 하지 않을 경우 예외가 일어나서 오동작 하는 자식 프로세스를 종료할 수 있다.

proc = run_sleep(10)

try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print(f'Exit status {proc.poll()}')