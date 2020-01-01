# 파이썬에서는 명시적인 게터와 세터를 구현할 일이 거의 없다.


class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


r2 = VoltageResistance(1e3)
print(r2.current)
r2.voltage = 10
print(r2.current)


# 프로퍼티에 setter 를 설정하면 클래스에 전달된 값들의 타입을 체크하고 값을 검증할 수도 있다.

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f"{ohms} ohms muse be > 0")
        self._ohms = ohms


r3 = BoundedResistance(1e3)


# r3.ohms = 0 #ValueError: 0 ohms muse be > 0

# 부모 클래스의 __init__함수 때문에 세터 메소드가 호출되기 때문
# 객체 생성이 완료되기도 전에 곧장 검증 코드가 실행
# BoundedResistance(-5) #ValueError: -5 ohms muse be > 0


class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")

        self._ohms = ohms

# @property 의 가장 큰 단점은 속성에 대응하는 메서드를 서브클래스에서만 공유할 수 있다는 점

# @property 메서드로 세터와 게터를 구현할 때 예상과 다르게 동작하지 않게 해야한다.

