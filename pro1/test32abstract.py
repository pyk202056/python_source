# 추상 클래스(abstract clsss)
# 추상 메소드를 가진 클래스를 추상 클래스라고 하며
# 얘는 인스턴스 할 수 없다.(객체 생성 불가)
# 부모 클래스로만 사용됨
# 추상 클래스는 "직접 객체를 만들려고 존재하는 클래스가 아니라, 
# 자식 클래스들이 반드시 지켜야 할 공통 규칙을 정하는 클래스"이다.
# 추상 클래스 = 자식 클래스에게 규칙을 강제(메서드 오버라이딩)하는 부모 클래스

from abc import *

class AbstractClass(metaclass = ABCMeta):   # 추상 클래스
    @abstractmethod
    def abcMethod(self):   # 추상 메소드 : 자식 클래스에서 오버라이딩 강요
        pass

    def normalMethod(self):
        print('추상 클래스 내의 일반 메소드 : 자식 클래스에서 오버라이딩 선택')

# parent = AbstractClass()  # TypeError: Can't instantiate abstract class

class Child1(AbstractClass):
    name = '난 Child1'

    def abcMethod(self):
        print('부모가 가진 추상 메소드를 재정의 - 강요 당함 ㅠㅠ')

# c1 = Child1()  # 추상메소드 오버라이딩 X - TypeError: Can't instantiate abstract class Child1
ch1 = Child1()
print('name : ', ch1.name)
ch1.abcMethod()
ch1.normalMethod()

print()
class Child2(AbstractClass):
    def abcMethod(self):      # 오버라이딩 강요 당함
        print('오버라이딩 함 : Child2에서 수행할 로직 작성')

    def normalMethod(self):   # 오버라이딩 자의적 선택함
        print('부모의 일반 메소드를 내 맘대로 내용 변경 해 사용')

    def show(self):
        print('Child2 고유 메소드')

ch2 = Child2()
ch2.abcMethod()
ch2.normalMethod()
ch2.show()

print('-- 다형성 -----')
happy = ch1
happy.abcMethod()
print()
happy = ch2
happy.abcMethod()
