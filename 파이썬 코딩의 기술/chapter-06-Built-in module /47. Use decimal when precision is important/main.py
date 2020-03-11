from decimal import Decimal, ROUND_UP

rate = Decimal('1.45')
seconds = Decimal('222')

cost = rate * seconds / Decimal('60')
print(cost)

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)

rate = Decimal('0.05')
seconds = Decimal('5')

cost = rate * seconds / Decimal('60')
print(cost)

rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)

# 데시몰이 고정 소수점 수에도 잘 동작하지만 아직도 정확도 면에서는 제약이 있다
# 정확도에 제한이 없는 유리수를 표현하려면 내장 모듈 fractions 의 Fraction 클래스를 사용해야 한다.
