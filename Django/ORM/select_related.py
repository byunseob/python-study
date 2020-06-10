# select_related 와 prefetch_related 는 하나의 QuerySet을 가져올 때,
# 미리 related objects들까지 다 불러와주는 함수이다.
# 비록 query를 복잡하게 만들긴 하지만,
# 그렇게 불러온 data들은 모두 cache에 남아있게 되므로 DB에 다시 접근해야 하는 수고를 덜어줄 수 있다.
# 이렇게 두 함수 모두 DB에 접근하는 수를 줄여, performance를 향상시켜준다는 측면에서는 공통점이 있지만, 그 방식에는 차이점이 있다.
