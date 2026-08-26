# 추상클래스를 사용해 다형성 - 배송 관련(일반, 퀵, 직접수령)

from abc import ABC, abstractmethod

# 공통 규격(틀) 클래스 : 모든 배송 클래스는 '배송비를 가져야한다'라는 규칙
class Delivery(ABC):
    @abstractmethod
    def get_fee(self, distance):
        # pass
        return 0

class NormalDelivery(Delivery):  # 일반 배송
    def get_fee(self, distance):
        return 3000    # 기본 배송비

class QuickDelivery(Delivery):  # 퀵 배송
    def get_fee(self, distance):
        return 3000 + distance * 1000  # 거리까지 고려  

class Pickup(Delivery):    # 직접 수령
    def get_fee(self, distance):
        return 0

class DeliveryUtil:   # 어떤 배송 객체든 배송비 출력 담당
    def print_fee(delivery, distance):
        fee = delivery.get_fee(distance)

        print('배송방식 : ', delivery.__class__.__name__)
        print('배송거리 : ', distance, 'km')
        print('배송요금 : ', fee, '원')


c1 = NormalDelivery()
c2 = QuickDelivery()
c3 = Pickup()

DeliveryUtil.print_fee(c1, 5)
print()
DeliveryUtil.print_fee(c2, 5)
print()
DeliveryUtil.print_fee(c3, 5)
