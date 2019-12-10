# 파이썬 프로그래밍의 대부분은 데이터를 담은 클래스들을 정의하고 이 객체들이 연계되는 방법을 명시하는 일이다.
# 모든 파이썬 클래스는 일종의 컨테이너로 속성과 기능을 함께 캡슐화 한다.
# 파이썬은 데이터 관리용 내장 컨테이너타입(리스트,튜플,세트,딕셔너리)도 제공한다.

# 파이썬 세계의 내장 collections.abc 모듈은 각 컨테이너 타입에 필요한 일반적인 메서드를 모두 제공
# 하는 추상 기반 클래스들을 정의한다.
# 이 추상 기반 클래스들에서 상속받아 서브클래스를 구현하면 필수 메소드를 구현하지 않으면 모듈이
# 에러를 알려준다.
