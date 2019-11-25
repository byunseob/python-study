# 파이썬은 다중 상속을 다루기 쉽게 하는 기능을 내장한 객체 지향 언어다.
# 하지만 다중 상속은 아예 안하는게 좋다.

# 다중상속으로 얻는 편리함과 캡슐화가 필요하다면 대신 믹스인 을 작성하는 방안을 고려하자.
# 믹스인 이란 클래스에서 제공해야 하는 추가적인 메서드만 정의하는 작은 클래스를 말한다.
# 믹스인 클래스는 자체의 인스턴스 속성을 정의하지 않으며 __init__ 생성자를 호출하도록 요구하지도 않는다.

# 파이썬에서는 타입과 상관없이 객체의 현재 상태를 간단하게 조사할 수 있어서 믹스인을 쉽게 작성할 수 있다.
# 동적 조사를 이용하면 많은 클래스에 적용할 수 있는 범용 기능을 믹스인에 한 번만 작성하면 된다.
# 믹스인들을 조합하고 계층으로 구성하면 반복코드를 최소화 하고 재사용성을 극대화 할 수 있다.

# 파이썬 객체를 메모리 내부 표현에서 직렬화용 딕셔너리로 변환하는 기능이 필요하다고 해보자.
# 이 기능을 모든 클래스에서 사용할 수 있게 범용으로 작성하는 건 어떨까?

# 다음은 상속받는 모든 클래스에 추가될 새 공개 메서드로 이 기능을 구현하는 믹스인이다.
import json


class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    # 세부 구현은 직관적이며 hasattr 을 사용한 동적 속성 접근, ininstance 를 사용한 동적 타입 검사,
    # 인스턴스 딕셔너리 __dict__ 를 이용한다.

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


# 다음은 바이너리 트리를 딕셔너리로 표현하려고 믹스인을 사용하는 예제 클래스다.

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))

print(tree.to_dict())


# 믹스인의 가장 큰 장점은 범용 기능을 교체할 수 있게 만들어서 필요할 때 동작을 오버라이드할 수 있다는 점이다.
# 예를 들어 다음은 부모 노드에 대한 참조를 저장하는 BinaryTree 의 서브 클래스다.
# 이 순환 참조는 ToDictMixin.to_dict 의 기본구현이 무한 루프에 빠지게 만든다.

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value  # 순환 방지
        else:
            return super()._traverse(key, value)


# 해결책은 BinaryTreeWithParent 클래스에서 ToDictMixin._traverse 메소드를 오버라이드해서
# 믹스인이 순환에 빠지지 않도록 필요한 값만 처리하게 하는 것이다.

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(7, parent=root.left)
print(root.to_dict())


# BinaryTreeParent._traverse 를 정의한 덕분에 BinaryTreeParent 타입의 속성이 있는
# 클래스라면 무엇이든 자동으로 ToDictMixin 으로 동작할 수 있게 되었다.

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict())


# 믹스인을 조합할 수도 있다.
# 예를 들어 어떤 클래스에도 동작하는 범용 JSON 직렬화를 제공하는 믹스인이 필요하다고 해보자.
# 이 믹스인은 클래스에 to_dict 메서드(ToDictMixin 클래스에서 제공할 수도 있고 그렇지 않을 수도 있다) 기
# 있다고 가정하고 만들면 된다.

class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


# JsonMixin 클래스가 어떻게 인스턴스 메소드와 클래스 메소드를 둘 다 정의하는지 주목하자.
# 믹스인을 이용하면 이 두종류의 동작을 추가할 수있다.
# 이 예제에서 JsonMixin 의 요구사항은 클래스에 to_dict 메서드가 있고 해당 클래스의 __init__ 메소드에서
# 키워드 인수를 받는 다는 것뿐이다.

# 이 믹스인을 이용하면 짧은 반복 코드로 JSON 으로 직렬화 하고 JSON 에서 역질렬화하는 유틸리티 클래스의
# 계층 구조를 간단하게 생성할 수 있다.
# 예를 들어 당므은 데이터센터 토폴로지를 구성하는 부분들을 표현하는 데이터 클래스의 계층이다.

class DataCenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


serialized = """
    {
  "switch": {
    "ports": 5,
    "speed": "1e9"
  },
  "machines": [
    {
      "cores": 8,
      "ram": "32e9",
      "disk": "5e12"
    },
    {
      "cores": 4,
      "ram": "16e9",
      "disk": "1e12"
    },
    {
      "cores": 2,
      "ram": "4e9",
      "disk": "500e12"
    }
  ]
}
"""
deserialized = DataCenterRack.from_json(serialized)
print(deserialized.to_json())
round_trip = deserialized.to_json()
print(round_trip)
assert json.loads(serialized) == json.loads(round_trip)

# 이런 믹스인을 사용할 때는 클래스가 객체 상속 계층의 상위에서
# 이미 JsonMixin 을 상속 받고 있어도 괜찮다.

