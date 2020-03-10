from collections import namedtuple

ALIVE = '*'
EMPTY = '-'

Query = namedtuple('Query', ('y', 'X'))


def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)
    ne = yield Query(y + 1, x + 1)

