# 직원 급여 계산 예제
# 직원이라는 개념은 있지만 실제 급여 계산은 정규직과 아르바이트가 서로 다르다.

from abc import ABC, abstractmethod

# 직원들의 공통 규격을 정의하는 추상 클래스
class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_salary(self):  # 자식 클래스가 반드시 구현해야 하는 메소드
        pass

    def show_salary(self): # 모든 직원이 공용하는 일반 메소드
        print('이름 : ', self.name)
        print('급여 : ', self.get_salary(),'원')  # 클래스에 따라 다른 결과(다형성)

# 정규직
class FullTimeEmployee(Employee):
    def __init__(self, name, monthly_salary):
        super().__init__(name)
        self.monthly_salary = monthly_salary

    def get_salary(self):
        return self.monthly_salary

    def showMe(self):
        print('나는 정규직이야')

# 아르바이트
class PartTimeEmployee(Employee):
    def __init__(self, name, hours, hourly_pay):
        super().__init__(name)
        self.hours = hours
        self.hourly_pay = hourly_pay

    def get_salary(self):
        return self.hours * self.hourly_pay

emp1 = FullTimeEmployee("홍길동", 3500000)
emp2 = PartTimeEmployee("한국인", 80, 10500)

emp1.show_salary()
print()
emp2.show_salary()

# 추상 클래스를 사용하는 이유는 한마디로 하면
# 여러 자식 클래스가 반드시 가져야 할 공통 규칙을 정하고, 
# 구현을 강제하기 위함.
