# python3 는 bytes, str 두 가지 타입으로 문자 시퀀스를 나타낸다.
# bytes 인스턴스는 raw 8비트 값을 저장한다.
# str 인스턴스는 유니코드 문자를 저장
# python2 는 str, unicode 로 문자시퀀스를 나타낸다.
# python2 의 str 인스턴스는 raw 8비트

b = b'byte'
s = 'str'

# byte to str
print(b.decode())

# str to byte
print(s.encode())