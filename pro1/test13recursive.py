# 재귀함수 : 함수가 자기 자신을 호출 - 반복 처리 가능

def countDown(n):
    if n == 0:
        print('완료')
        return
    else:
        print(n, end = ' ')
        countDown(n - 1)   # 재귀(recursion)

countDown(5)

print('\n--- 1부터 n까지의 정수의 합 구하기 ---')
def totFunc(n):
    if n == 1:
        print('완료')
        return 1

    return n + totFunc(n - 1)  # 재귀

result = totFunc(5)
print('result : ', result)

print('\n--- factorial 계산 ---')
# 팩토리얼(factorial, 계승)은 1부터 어떤 자연수 n까지의 모든 자연수를 차례대로 곱하는 것
#  3! = 3 * 2 * 1
def factFunc(a):
    if a == 1:return 1
    print(a)
    return a * factFunc(a - 1)

result2 = factFunc(5)
print('result2 : ', result2)