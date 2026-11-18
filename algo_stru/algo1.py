# 알고리즘(Algorithm)은 어떤 문제를 해결하기 위해 정해진 일련의 명확한 절차나 방법들을 
# 순서대로 정리한 명령어의 집합
# 입력값을 받아 유한한 시간 내에 정해진 논리적 순서에 따라 문제를 해결하고 
# 결과물을 도출하는 과정으로, 컴퓨터 프로그래밍 및 일상생활의 문제 해결에 모두 적용된다. 

# 1 부터 n까지 연속한 숫자의 합을 구하는 알고리즘
def sum_n(n):
    s = 0
    for i in range(1, n + 1):
        s = s + i

    return s

print(sum_n(10))
print(sum_n(100))

print('가우스의 합 공식으로 n까지의 합')
def sum_2(n):
    return n * ( n + 1) // 2

print(sum_2(10))
print(sum_n(100))

print('최대값 구하기')
def find_max(a):
    n = len(a)
    max_v = a[0]
    for i in range(1, n):
        if a[i] > max_v:
            max_v = a[i]  # 최대값을 변경

    return max_v

d = [17, 92, 33, 58, 7, 32, 42]
print(find_max(d))

print('\n최대 공약수 구하기')
# 예) 4, 6 : 4와 6의 공통약수 2
def gcdFunc(a, b):
    i = min(a, b)
    while True:
        if a % i == 0 and b % i == 0:
            return i
        i = i - 1

print(gcdFunc(4, 6))
print(gcdFunc(24, 16))
print(gcdFunc(81, 27))

print('\n최대 공약수 구하기2 (유클리드 알고리즘)')
def gcdFunc2(a, b):
    if b == 0:
        return a

    return gcdFunc2(b, a % b)  # 좀 더 작은 값으로 재귀 호출

print(gcdFunc2(24, 18))   # 6
print(gcdFunc2(1, 5))     # 1
print(gcdFunc2(60, 24))   # 12
