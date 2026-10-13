# 배열 연산
# 기본 수학함수는 배열에 요소별로 적용되고, 
# +,-,*,/나 또는 add, subtract, multiply, divide 함수를 사용
# 벡터화 연산을 하므로 for문을 사용하지 않고 바로 배열에 대한 연산 가능

import numpy as np

# x = np.array([[1, 2], [3, 4]], dtype=np.float32)
x = np.array([[1., 2], [3, 4]])
print(x, ' ', x.dtype)  # [[1. 2.][3. 4.]]   float32

# y = np.arange(5, 9)    # [5 6 7 8]   int64    1차원 배열 생성
y = np.arange(5, 9).reshape(2, 2)  # 구조 변경 (1차원 -> 2차원)
y = y.astype(np.float32) # type 변경
print(y, ' ', y.dtype)   # [[5. 6.][7. 8.]]   float32

print(x.ndim, ' ', y.ndim)  # 2   2

print()
print(x + y)        # 파이썬 연산자 사용
print(np.add(x, y)) # 넘파이 함수(유니버설 함수:내부적으로 벡터화 연산) - 위 보다 연산 속도 빠름  
print()
print(x - y)
print(np.subtract(x, y))
print()
print(x * y)
print(np.multiply(x, y))
print()
print(x / y)
print(np.divide(x, y))
print()
print(np.sqrt(x), ' ', np.exp(x), ' ', np.log(x), ' ', np.cos(x))

print('\ndot()은 numpy 모듈의 인스턴스 메소드로 내적 연산이 가능')
v = np.array([9, 10])
w = np.array([11, 12])
print(v * w)   # 요소별 곱셈  [ 99 120]  <== 9 * 11, 10 * 12

# 벡터의 내적 (행렬곱)
print(v.dot(w))     # 219  내적의 결과는 스칼라(크기만 있고 방향은 없음)
print(np.dot(v, w)) # 219  <==  방법1:9 * 11 + 10 * 12   
# 219  <==  방법2:a·b=|a||b|*cos(θ)

print()
# 배열 계산 함수  (axis를 지정하지 않고 집계함수를 쓰면 전체 배열의 차원을 떨어뜨림 )
print(x)   # [[1. 2.][3. 4.]]
print(np.mean(x), ' ', np.var(x))
print(np.max(x), ' ', np.min(x))
print(np.argmax(x), ' ', np.argmin(x))   # index 반환
print(np.cumsum(x))   # 누적합
print(np.cumprod(x))  # 누적곱

print()
names1 = np.array(['tom','james','tom','oscar'])
names2 = np.array(['tom','page','john'])
print(np.unique(names1))
print(np.intersect1d(names1, names2))  # 교집합 (중복 X)   ['tom']
print(np.intersect1d(names1, names2, assume_unique=True))  # 교집합 (중복 O)
print(np.union1d(names1, names2))  # 합집합

print('\n전치(Transpose) - 2차원 배열에서 행과 열의 위치를 바꿈')
print(x)
print(x.T)
print(x.transpose())
print(x.swapaxes(0, 1))

print('\nBroadcasting : 크기가 다른 배열 간의 연산'
            ' - 작은 배열을 여러 번 반복해 큰 배열과 연산')
x = np.arange(1, 10).reshape(3, 3)
y = np.array([1, 0, 1])
print(x)
print(y)
print(x + y)

print()
# 배열자료 파일로 저장
np.savetxt("numpy2.txt", x)     # file i/o
imsi = np.loadtxt("numpy2.txt")
print(imsi)




