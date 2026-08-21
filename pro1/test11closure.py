# Closure : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭이다.
# 내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기

def funcTimes(a, b):
    c = a * b
    print('c : ', c)
    return c

print(funcTimes(2, 3))
# print('c : ', c)  # NameError: name 'c' is not defined

kbs = funcTimes(2, 3)   # 함수 실행 결과를 치환
print(kbs)
kbs = funcTimes  # 함수 주소를 치환 (별명이 하나 생김)
print(kbs)
print(kbs(2, 3))
print(id(funcTimes), id(kbs))  # 2076660987888 2076660987888

mbc = sbs = kbs
del funcTimes   # funcTimes 함수명 삭제 (참조 변수 삭제)
# print(funcTimes(2, 3))  # NameError: name 'funcTimes' is not defined
print(kbs(3, 4))
print(sbs(3, 4))
print(mbc(3, 4))

print('\n--- 클로저를 사용하지 않은 경우 -------')
def out():
    count = 0
    def inn():
        nonlocal count
        count += 1
        return count
    print(inn())

# print(count)  # err
out()
out()

print('\n--- 클로저를 사용한 경우 -------')
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner   # 요것이 클로저 : 내부 함수의 객체의 주소를 반환함

var1 = outer()
print('var1 주소 : ', var1)  # <function outer.<locals>.inner at 0x0000020459373480>
print('count : ', var1())
print('count : ', var1())
# print(var1.count)  # 외부에서 직접 접근은 불가
print('클로저 내부 확인:', var1.__closure__)  # __명령__ : 파이썬 고유 명령
myvar = var1()
print(myvar)
print()
var2 = outer()   # 새로운 객체(inner 함수) 생성
print(var2())
print(var2())

print('\n수량 * 단가 * 세금한 결과를 출력하기 ---')
def outer2(tax):   # tax는 지역변수
    def inner2(su, dan):
        amount = su * dan * tax
        return amount
    return inner2

# 1분기에는 금액:su * dan에 대한 tax는 0.1 부과
q1 = outer2(0.1)
result1 = q1(5, 50000)
print('result1 : ', result1)
result2 = q1(2, 10000)
print('result2 : ', result2)

# 2분기에는 금액:su * dan에 대한 tax는 0.05 부과
q2 = outer2(0.05)
result3 = q2(5, 50000)
print('result3 : ', result3)
result4 = q2(2, 10000)
print('result4 : ', result4)

print('\n\n일급함수(객체) : 함수를 변수나 상수에 저장, 함수 안에 함수, 인자로 함수 전달, 반환 값이 함수')
def func1(a, b):
    return a + b

func2 = func1  # 함수를 변수나 상수에 저장
print(func1(3, 4))
print(func2(3, 4))

print()
def func3(fu):  # 인자로 함수 전달 받음
    def func4():   # 함수 안에 함수 선언
        print('나는 내부 함수야 ~~~')
    func4()
    return fu   # 반환 값이 함수

mbc = func3(func1)  # 인자로 함수 전달함
print(mbc(6, 7))


print('\n축약함수(Lambda function) : 여러 줄의 함수 정의를 한 줄로 간단하게 줄여서 쓰는 익명 함수')
# 형식 -- lambda 매개변수,... : 표현식    <== return 없이 결과 반환

def hapFunc(x, y):  # 프로그램 종료시 까지 메모리를 유지
    return x + y

print(hapFunc(1, 2))

# 위 코드를 람다로 표현하면
print((lambda x, y:x + y)(1, 2))  # 단발성(휘발성) - 실행과 동시에 메모리 사라짐

gg = lambda x, y:x + y
print(gg)  # <function <lambda> at 0x00000290A2DF3A00>
print(gg(1, 2))

gg2 = lambda x, y:x + y
print(id(gg), id(gg2))
print((lambda x, y:x + y) is (lambda x, y:x + y))  # False

print()
kbs = lambda a, su=10: a + su
print(kbs(5))
print(kbs(5, 6))

print()
sbs = lambda a, *tu, **di : print(a, tu, di)
sbs(1, 2, 3, var1=4, var2=5)  # 1 (2, 3) {'var1': 4, 'var2': 5}

print('\n임의의 함수에서 람다 사용하기')
# filter() : 반복 가능한 객체(리스트 등)에서 특정 조건에 맞는 요소만 골라낼 때 사용. 
# 기본 구조는 filter(함수, 반복가능한객체)
print(list(filter(lambda a:a < 5, range(10))))  # [0, 1, 2, 3, 4]
print(list(filter(lambda a:a % 2, range(10))))  # [1, 3, 5, 7, 9]
# print(bool(0), bool(1))  # False True

# filter를 이용해 1 ~ 100 사이의 정수 중 5의 배수이거나 7의 배수만 출력(리스트로)
print(list(filter(lambda a : a % 5 == 0 or a % 7 == 0, range(1, 101))))
