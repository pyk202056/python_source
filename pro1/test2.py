# 연산자
# 치환 연산자
v1 = 3
v1 = v2 = v3 = 5
print(v1, v2, v3)

v1 = 10, 20, 30
print('v1 : ', v1)  # v1 :  (10, 20, 30)

v1, v2 = 10, 20
print(v1, v2)
v2, v1 = v1, v2  # 기억장소의 값 맞교환
print(v1, v2)

print('값 할당 packing')
v1, *v2 = 1,2,3,4,5
print(v1, v2)  # 1 [2, 3, 4, 5]
*v1, v2 = 1,2,3,4,5
print(v1, v2)  # [1, 2, 3, 4] 5
*v1, v2, v3 = 1,2,3,4,5
print(v1, v2, v3) # [1, 2, 3] 4 5
v1, v2, *v3 = 1,2,3,4,5
print(v1, v2, v3) # 1 2 [3, 4, 5]
v1, *v2, v3 = 1,2,3,4,5
print(v1, v2, v3) # 1 [2, 3, 4] 5
# *v1, *v2, v3 = 1,2,3,4,5   # err

print('print 함수 알아보기')
print(format(123.45678, '10.3f'))
print(format(123.45678, '10.3'))
print('서식에 의한 자료 출력 %s %d %f'%('문자열', 5, 23.4))
name = "마우스"; price = \
    5000; 
print(f"이름:{name}, 가격:{price}")
print('abc')
print('def')
print('abc', end=' ')
print('def')

print('\n\n연산자 연습 계속')
print(5 + 3, 5 - 3, 5 * 3, 5 / 3, 5 // 3, 5 % 3, 5 ** 3)
#       8 2 15 1.6666666666666667 1 2 125
print(divmod(5, 3))  # (1, 2)
print(3 + 4 * 5, (3 + 4) * 5)  # 23 35
# 연산자 우선순위
# () -> ** -> 단항 -> *, / -> +, - -> 비교 -> not -> and -> or -> =

print('관계(비교) 연산자')
print(5 > 3, 5 == 3, 5 != 3)  # True False True

print('논리 연산자')
print(5 > 4 and 4 < 3, 5 > 4 or 4 < 3, not(5 >= 4))  # False True False

print('문자열 더하기')
print('한' + '국' + " 만세")
print('한국' * 5)

print('누적')
a = 10
a = a + 1
a += 1   # 증감 연산자
print('a는 ', a)
print(f'a는 {a}')

print('부호 변경 : ', a, a * -1, -a, --a, ---a)

print('boolean 처리 : ', bool(123), bool(1), bool(-3.5), bool(True))
print('boolean 처리 : ', bool(0), bool(0.0), bool(False), bool(None))
print('boolean 처리 : ', bool([]), bool({}), bool(set()))

print('(이스케이프 문자 - Escape character - 특별한 의미를 표현하기 위한 문자 조합)')
print('aa\tbb')
print(r'aa\tbb')
print('aa\bbb')
print(r'aa\bbb')
print('aa\nbb')
print(r'aa\nbb')
print('c:\a\abc.txt')
print('c:\n\abc.txt')




