# 배열에 행, 열 추가 ......

import numpy as np

aa = np.eye(3)
print(aa)

bb = np.c_[aa, aa[2]]  # 2열과 동일한 열 추가
print('bb : \n', bb)

cc = np.r_[aa, [aa[2]]]  # 2행과 동일한 행 추가
print('cc : \n', cc)

print('-------')
print('append, insert, delete 함수 사용 - 새로운 배열을 생성')
a = np.array([1,2,3])
print(a)
# b = np.append(a, [4, 5])   # 추가
b = np.append(a, [4, 5], axis=0)  # 행 기준
print(b)

c = np.insert(a, 0, [6, 7])  # 0번째 위치에 데이터 삽입
print(c)

d = np.delete(a, 1)   # 1번째(인덱스) 자료 삭제
print(d)   # [1 3]

print()
aa = np.arange(1, 10).reshape(3, 3)
print(aa)
print(np.insert(aa, 1, 99))  # [ 1 99  2  3  4  5  6  7  8  9] 차원축소됨
print(np.insert(aa, 1, 99, axis=0))   # 행기준    차원유지
print(np.insert(aa, 1, 99, axis=1))   # 열기준    차원유지

print()
# 조건 연산 : where(조건, 참, 거짓)
x = np.array([1,2,3])
y = np.array([4,5,6])
conditionData = np.array([True, False, True])
result = np.where(conditionData, x, y)
print(result)   # [1 5 3]

print()
print(x)
aa = np.where(x >= 2)
print(aa)    # (array([1, 2]),)  조건을 만족하는 인덱스 위치를 튜플 형태로 반환
print(a[aa]) # [2 3]

print()
kbs = np.concatenate([x, y])   # 배열 결합
print(kbs)    # [1 2 3 4 5 6]

mbc, sbs = np.split(kbs, 2)
print('mbc : ', mbc)
print('sbs : ', sbs)

print()
a = np.arange(1, 17).reshape(4, 4)
print(a)

x1, x2 = np.hsplit(a, 2)   # 가로 방향으로 분할(열을 나눔)
print(x1)
print(x2)

print()
print(np.vsplit(a, 2))     # 행방향 분할

print('-------')
# 표본 추출(Sampling)은 전체 데이터인 모집단(Population)에서 
# 일부 데이터를 뽑아 조사·분석하는 것.
# 단순 무작위 추출 : 전체에서 랜덤으로 추출
# 복원 추출 : 뽑은 데이터를 다시 넣고 또 뽑음 - 중복 허용
# 비복원 추출 : 중복 없음
li = np.array([1,2,3,4,5,6,7])

sample1 = np.random.choice(li, size=3, replace = False)  # 단순 무작위 추출 (비복원)
print(sample1)
sample2 = np.random.choice(li, size=3, replace = True)   # 단순 무작위 추출 (복원)
print(sample2)

print()
# 복원 추출
for _ in range(5):  
    print(li[np.random.randint(0, len(li) - 1)], end = ' ')  # 5 4 3 3 4 

print()
# 비복원 추출
import random
print(random.sample(li.tolist(), 5))  # random.sample은 list type을 원함
