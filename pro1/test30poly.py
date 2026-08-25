# 메소드 오버라이딩을 통한 Polymorphism(다형성) 구현
# 카드결제, 현금결제, 포인트결제를 각 클래스에서 결제 메소드를 오버라이딩하기

class Payment:    # 부모 클래스 : 결제라는 공통 기능 pay()를 정의
    def pay(self, amount):
        print(f"{amount}원 결제를 진행함")
        # pass   - 내용없이 만들수도 있다.

# 이하 자식 클래스
class CardPayment(Payment):   # 카드 결제 클래스 : 카드 수수료 2%를 계산하여 결제
    def __init__(self):     # 이코드는 생략 가능
        pass

    def abc():
        print("CardPayment 고유 메소드")

    def pay(self, amount):    # 메소드 오버라이드 - 강요는 아님. 선택적
        fee = amount * 0.02
        total = amount + fee
        print(f"[카드 결제]")
        print(f"상품 금액 : {amount}원")
        print(f"수수료 : {fee}원")
        print(f"최종 결제 금액 : {total}원")

class CashPayment(Payment):   # 현금 결제 클래스 : 현금 할인 5%를 적용하여 결제
    def pay(self, amount):
        discount = amount * 0.05
        total = amount - discount
        print(f"[현금 결제]")
        print(f"상품 금액 : {amount}원")
        print(f"할인 금액 : {discount}원")
        print(f"최종 결제 금액 : {total}원")

class PointPayment(Payment):   # 포인트 결제 클래스 : 금액 만큼 포인트를 사용
    def pay(self, amount):
        print(f"[포인트 결제]")
        print(f"{amount} 포인트를 사용함")


# 클래스 공통 처리 함수 : 전달받은 객체의 pay()를 호출
def process_payment(paymentAddr:Payment, amount:int) -> None:
    paymentAddr.pay(amount)


if __name__ == "__main__":
    p1 = CardPayment()
    p2 = CashPayment()
    # p3 = PointPayment()

    process_payment(p1, 10000)
    print()
    process_payment(p2, 10000)
    print()
    process_payment(PointPayment(), 10000)

