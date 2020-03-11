# 내장 모듈 pickle 은 바이썬 객체를 바이트 스트림으로 직렬화 하거나 바이트를 객체로 역직렬화하는 데 사용한다.
# pickle 로 만든 바이트 스트림을 신뢰할 수 없는 부분과 통신하는데 사용하면 안된다.
# pickle 의 목적은 바이너리 채널을 통해 제어하는 프로그램 간에 파이썬 객체를 넘겨주는 것이다.

# pickle 모듈의 직렬화 포맷은 설계 관점에서 안전하지 못하다.
# 직렬화한 데이터는 원래 파이썬 객체를 재구성하는 데 필요한 프로그램을 담는다.
# 이는 악성 pickle 페이로드로 파이썬 프로그램에서 해당 페이로드를 역직렬화 하는 부분을 망가뜨릴 수 있음을 의미한다
import copyreg
import pickle


class GameState(object):
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs)


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


copyreg.pickle(GameState, pickle_game_state)
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)
