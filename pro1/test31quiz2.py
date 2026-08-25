# 다중 상속

class Animal: # 최상위 클래스
    def move(self):
        print("동물은 움직인다")

class Dog(Animal):
    name = "개"

    def move(self): # Animal() 클래스의 move()메서드와 이름만 갖고 기능은 다른 오버라이딩
        print(f"{self.name}는 기분 좋으면 꼬리를 흔든다")

class Cat(Animal):  # Animal에서 move() 받아오기
    name = "고양이"

    def move(self):
        print(f"{self.name}는 그루밍을 한다")

class Wolf(Dog, Cat):
    pass

class Fox(Cat, Dog):
    def foxMethod(self):
        print("아리는 꼬리가 9개")
        
    def move(self):
        print("여우의 움직임")


if __name__ =="__main__":
    Animal().move()

    print()
    d=Dog()
    d.move()
    print()
    c=Cat()
    c.move()
    print()
    w=Wolf()
    w.move()
    print()
    f=Fox()
    f.move()

    print('--다형성-----')
    ani = [d, c, w, f]
    for a in ani:
        print(id(a))
        a.move()
        print()

    
