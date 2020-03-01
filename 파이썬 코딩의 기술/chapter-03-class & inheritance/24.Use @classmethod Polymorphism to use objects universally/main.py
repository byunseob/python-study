# 파이썬에서는 객체가 다형성을 지원할 뿐만 아니라 클래스도 다형성을 잘 지원한다.
# !!!다형성은 계층 구조에 속한 여러 클래스가 자체의 메서드를 독립적인 버전으로 구현하는 방식이다.
# 다형성을 이용하면 여러 클래스가 같은 인터페이스나 추상 기반 클래스를 충족하면서도 다른 기능을 제공할 수 있다.

# 맵리듀스 구현을 작성할 때 입력 데이터를 표현할 공통 클래스가 필요하다고 하자.
# 다음은 서브클래스에서 정의해야 하는 read 메서드가 있는 입력 데이터 클래스이다.
import codecs
import os
from threading import Thread


class InputData(object):
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


# 표준 방식으로 입력 데이터를 처리하는 맵리듀스 작업 클래스에도 비슷한 추상 인터페이스가 필요하다.

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError


# 다음은 적용하려는 특정 맵리듀스 함수를 구현한 Worker 의 구체 서브클래스다

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


# 적절히 인터페이스를 설계하고 추상화한 클래스들이지만 일단 객체를 생성한 후에나 유용하다.
# 무엇으로 객체를 만들고 맵 리듀스 를조율할까?
# 가장 간단한 방법은 헬퍼 함수로 직접 객체를 만들고 연결하는 것이다.


def generate_input(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))

    return workers


# map 단계를 여러 스레드로 나눠서 Worker 인스턴스들을 실행한다
# 그 다음 reduce 를 반복적으로 호출해서 결과를 최종값 하나로 합친다.

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)

    return first.result


def mapreduce(data_dir):
    inputs = generate_input(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


from tempfile import TemporaryDirectory


def write_test_files(tmpdir):
    for filename in ('one', 'two', 'three'):
        path = os.path.join(tmpdir, filename)
        with codecs.open(path, 'w', encoding='utf-8') as fp:
            fp.write(filename + '\n')


with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)

print('There are', result, 'lines')


# 잘동작하는 코드지만 mapreduce 함수가 전혀 범용적이지 않다는 점이다.
# 다른 InputData 나 worker 서브클래스를 작성한다면 각 헬퍼함수를 알맞게 다시 작성해야 한다.

# 이 문제는 결국 객체를 생성하는 범용적인 방법의 필요성으로 귀결된다.
# 다른 언어에서는 이 문제를 생성자 다형성으로 해결한다.
# 이 방식을 따르려면 각 InputData 서브클래스에서 맵리듀스를
# 조율하는 헬퍼 메서드가 범용적으로 사용할 수 있는 특별한 생성자를 제공해야 한다.

# !!!문제는 파이썬이 단일 생성자 메소드 __init__만을 허용한다는 점이다.

# 이 문제를 해결하는 가장 좋은 방법은 @classmethod 다형성을 이요한느 것이다.
# @classmethod 다형성은 생성된 객체가 아니라 전체 클래스에 적용된다는 점만 빼면
# InputData.read 에 사용한 인스턴스 메서드 다형성과 똑같다.

class GenericInputDat(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_input(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputDat):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_input(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):
    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_input(config):
            workers.append(cls(input_data))

        return workers


# 위의 input_class.generate_input 호출이 바로 여기서 보여주려는 클래스 다형성이다.
# 또한 create_workers 가 __ini__메소드를 직접 사용하지 않고 GenericWorker 를 생성하는 또 다른 방법으로 cls 를 호출함을 알 수있다.

# GenericWorker 를 구현할 서브클래스는 부모 클래스만 변경하면 된다.

class LineCountWorker(GenericWorker):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)

print('There are', result, 'lines')

# 이제 GenericInputData 와 GenericWorker 의 다른 서브클래스를 원하는 대로 만들어도 글루코드를 작성할 필요가 없다.

