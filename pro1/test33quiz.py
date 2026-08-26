from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, irum, nai):
        self.irum = irum
        self.nai = nai

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self):
        pass

    def irumnai_print(self):
        print(f'이름 : {self.irum}, 나이 : {self.nai},', end=' ')


class Temporary(Employee):
    def __init__(self, irum, nai, ilsu, ildang):
        super().__init__(irum, nai)
        # Employee.__init__(self, irum, nai)
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):
        return self.ilsu * self.ildang

    def data_print(self):
        self.irumnai_print()
        print(f'월급 : {self.pay()}')


class Regular(Employee):
    def __init__(self, irum, nai, salary):
        super().__init__(irum, nai)
        self.salary = salary

    def pay(self):
        return self.salary

    def data_print(self):
        self.irumnai_print()    # super().irumnai_print()
        print(f'급여 : {self.pay()}')


class Salesman(Regular):
    def __init__(self, irum, nai, salary, sales, commission):
        super().__init__(irum, nai, salary)
        self.sales = sales
        self.commission = commission

    def pay(self):
        return super().pay() + (self.sales * self.commission)

    def data_print(self):
        self.irumnai_print()
        print(f'수령액 : {round(self.pay())}')

if __name__ == '__main__':
    t = Temporary(irum= '홍길동', nai= 25, ilsu= 20, ildang= 15000)
    r = Regular(irum= '한국인', nai= 27, salary= 3500000)
    s = Salesman(irum= '손오공', nai= 29, salary= 1200000, sales= 5000000, commission=0.25)

    t.data_print()
    r.data_print()
    s.data_print()