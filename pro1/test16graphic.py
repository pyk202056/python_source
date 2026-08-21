# 파이썬 지원 그래픽 모듈 사용

from turtle import *

p = Pen()
p.color('red', 'yellow')
p.begin_fill()

while True:
    p.forward(200)
    p.left(170)
    if abs(p.pos()) < 1:
        break

p.end_fill()
input()
