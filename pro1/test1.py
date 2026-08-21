print("환영합니다. 파이썬 세상!") 
"""
이건 주석이야
실행과는 상관없이 코드에 설명을 달 때 사용
작은 따옴표 3개를 사용해도 됨
"""
# 한 줄 주석
print("작업 계속")

# 변수 : 기억 장소의 이름 - 동적 (객체값 자체가 아니라 객체의 주소를 기억)
# 상수 : 기억 장소의 이름 - 정적
var1 = '안녕 파이썬'   # 따옴표는 ", 또는 '  둘 다 가능
print(var1)
print(var1)
var1 = 56
print(var1)
Var1 = 123    # 대소문자 구분
print(var1)
print(Var1)
PI = 3.14     # 상수 : 보통 대문자로 이름 부여. 고정된 값임을 약속
print(PI)   

a = 10
print('a = ', a)
print('"a = "', a)
print("'a = '", a)
b = 20.5
c = b
print(a, b, c)
print('주소 출력:', id(a), id(b), id(c))
print(a is b, a == b)  # is  주소 비교, == 값 비교
print(b is c, b == c)
print()
aa = [100]
bb = [100]
print(aa is bb, aa == bb)  # False True
print(id(aa), id(bb))

print()
import keyword   # 외부 모듈 읽기 - 보조 기억장치에 저장된 모듈을 주기억 장치로 로딩
print('키워드(예약어) 목록 : ', keyword.kwlist)
# 주의 : 예약어는 사용자 이름으로 사용하면 안됨

# print()
print('\ntype(자료형) 확인')  # \n : 다음행으로 이동 (line skip)
print(5, type(5))
print(5.4, type(5.4))
print(3 + 4j, type(3 + 4j))
print(True, type(True))
print('kbs', type('kbs'))

print((1,), type((1,)))
print([1], type([1]))
print({1}, type({1}))
print({'key':3}, type({'key':3}))
