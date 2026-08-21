# 함수 장식자(Decorator)는 기존의 함수 코드를 수정하지 않고도 함수의 앞뒤에 새로운 기능이나 추가 작업을 더해주는 기능. 
# 함수 위에 @장식자이름 기호를 붙여서 간단하게 사용.
# 장식자의 주요 특징
# - 기능 추가: 원래 함수를 바꾸지 않고 실행 전후로 로그 기록, 시간 측정, 권한 확인 등의 작업을 수행.
# - 코드 중복 줄이기: 여러 함수에서 공통으로 쓰는 기능을 하나로 묶어 재사용성을 높임.
# - 가독성 향상: @ 기호를 사용해 코드를 깔끔하고 직관적으로 유지한다.

# 기본 작동 원리
# : 장식자는 함수를 인자로 받아 내부에서 새로운 함수를 감싸서(wrapper) 반환.

def make2(fn):
    return lambda:"안녕 " + fn()

def make1(fn):
    return lambda:"반가워 " + fn()

def helloFunc():
    return "홍길동"

hi = make2(make1(helloFunc))  # Decorator 없이 실행
print(hi())  # 안녕 반가워 홍길동

@make2
@make1
def helloFunc2():
    return "고길동"

print(helloFunc2())

print('----------')
def traceFunc(func):
    def wrapperFunc(a, b):
        r = func(a, b)
        print(f'함수명:{func.__name__} (a={a}, b={b} -> {r})')
        return r
    return wrapperFunc   # 함수 주소 반환

@traceFunc
def addFunc(a, b):
    return a + b

print(addFunc(10, 20))
