# 메소드 오버라이딩(메소드 재정의)
# 부모 클래스에서 정의된 메소드를 자식이 동일명의 메소드로 내용만 변경해 사용
# 부모 메소드의 기능을 대체하는 새로운 기능을 구현 가능
# 동작의 구체화(공통 틀은 부모가, 실제 행동은 자식) 실현
# Polymorphism(다형성) - 같은 메소드이나 객체에 따라 다른 기능을 수행
# 확장, 유지보수에 도움 - 부모 코드는 유치한 채 자식 코드만 변경

class Parent:   # 용도 - 부모 클래스
    def printData(self):   # 내용이 없는 메소드 - 의도는 자식 클래스에서 오버라이딩을 기대
        pass

class Child1(Parent):
    def abc():
        print('Child1 클래스의 고유 메소드')

    def printData(self):    # 메소드 오버라이딩(Method overriding)
        su = 6
        a = 5 + su
        # 뭔가를 ...
        print('Child1에서 printData 오버라이딩')

class Child2(Parent):
    good = 'ok'

    def printData(self):    # 메소드 오버라이딩(Method overriding)
        print('Child2에서 printData 재정의함')
        msg = "부모와 동일 메소드명이나 내용은 다름"
        print(msg)

c1 = Child1()
c1.printData()
print()
c2 = Child2()
c2.printData()

print('\n다형성 구현 ------')
par = Parent()
par = c1
par.printData()
print()
par = c2
par.printData()
print('-------')
imsi = c1
imsi.printData()
print()
imsi = c2
imsi.printData()
