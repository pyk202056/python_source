# 클래스의 다중 상속 - 부모 클래스가 복수 (순서에 유의)

class Tiger:
    data = "호랑이 세상"

    def cry(self):
        print("호랑이 : 어흥")

    def eat(self):
        print("맹수는 고기를 좋아함")
        print("아침에 닭고기, 낮에 소고기, 저녁에 양고기")


class Lion:
    def cry(self):
        print("사자 : 으르렁")

    def hobby(self):
        print("백수의 왕은 낮잠이 취미")


class Liger1(Tiger, Lion):  # 두 개의 클래스를 상속받음
    pass

a1 = Liger1()
print(a1.data)
a1.eat()
a1.hobby()
a1.cry()   # 동일 멤버인 경우 첫번째 클래스의 멤버를 취함

print('----------------')

def hobby():
    print("모듈의 멤버 : 일반 함수")

class Liger2(Lion, Tiger):
    data = "라이거 만세"

    def play(self):
        print("라이거 고유 메소드 - play")

    def hobby(self):
        print("라이거는 공원 산책을 좋아함 - 오버라이딩")

    def showData(self):
        self.hobby()     # 현재 클래스에서 호출하고 없으면 부모에서 호출
        super().hobby()  # 부모에서 호출
        hobby()          # 클래스 바깥 : 모듈에서 함수 호출

        self.eat()
        super().eat()

        print(f"data : {self.data}, {super().data}")

a2 = Liger2()
a2.cry()
a2.showData()


