# numpy의 ndarray는 단순한 배열이라기 보다,
# 벡터/행열 연산도 가능한 다차원 수치 데이터 구조다.
# 주요 특징 : 
# 동일한 데이터 타입(Homogeneous), 빠른 연산 속도, 메모리 효율성

import numpy as np

ss = ['tom', 'james', 'oscar', 1, True]  # List : 여러 type의 자료로 구성
print(ss, ' ', type(ss))  # ['tom', 'james', 'oscar', 1, True] <class 'list'>

ss2 = np.array(ss)   # List type -> ndarray type으로 변환
print(ss2, ' ', type(ss2)) # ['tom' 'james' 'oscar' '1' 'True'] <class 'numpy.ndarray'>
# 상위 type 순서 : bool -> int -> float -> complex -> str

# 메모리 비교
li = list(range(1, 10))
print(li)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(id(li[0]),id(li[1]), hex(id(li[0])),hex(id(li[1]))) 
print(li * 10)   # 각 요소별 * 10이 아니라 10회 반복 
print("-- " * 10)

for i in li:
    print(i * 10, end = ' ')

print()
num_arr = np.array(li)
print(num_arr[0], ' ', num_arr[1], ' ', id(num_arr[0]), ' ', id(num_arr[1]))
# 1   2   1625439788912   1625439788912
# num_arr[0] : 배열 내부 원소를 읽어서 Numpy scalar 객체로 꺼냄
print(num_arr * 10)   # [10 20 30 40 50 60 70 80 90]

print()
b = np.array([[1, 2, 3], [4, 5, 6]])  # python의 중첩리스트를 배열화 
print(b, ' ', b.shape, ' ', b.ndim, ' ', b.size)  # (2, 3) 2행 3열짜리 배열:2 by 3, 2 * 3로 표현    2   6
print(b[0], ' ', b[[0]], ' ', b[0, 0])  # [1 2 3]   [[1 2 3]]  1

print()
# 배열 선언 후 자동으로 값 채우기
c = np.zeros((2, 2))
print(c)

d = np.ones((2, 3))
print(d)

e = np.eye(3)  # 단위 행렬(주대각선은 1, 나머지는 0으로 채움)
print(e)

print("\n난수 발생 ---")
print(np.random.rand(5))   # 균등 분포(0 이상 1미만의 난수)
print(np.random.randn(5))  # 정규 분포(평균0, 표준편차 1인 난수)

np.set_printoptions(threshold=np.inf)  # 너무 길면 ...이 나오는데 이를 무시
print(np.mean(np.random.rand(5000)))
print(np.mean(np.random.randn(5000)))

np.random.seed(1)  # 난수표(수학적 알고리즘으로 난수처럼 보이는 수열을 생성)의 특정 색인 값 선택해 난수를 고정
print(np.random.randn(2, 3))

print('\n배열의 인덱싱과 슬라이싱')
aa = np.array([1,2,3,4,5])   # (1,2,3,4,5), {1,2,3,4,5}
print(aa, ' ', aa[1])  # 인덱싱 (0부터 시작)
print(aa[1:4])   # 슬라이싱 : 1이상 4미만 인덱스에 해당하는 값 출력
print(aa[1:])
print(aa[0:5:1])  # [start, end, step]  step 1은 생략
print(aa[0:5:2])
print(aa[-2:])
print(aa[-4:-1])  # [2 3 4]

print()
bb = aa   # 주소 치환
print(aa)
print(bb)
print(id(aa), ' ', id(bb))   # 2098293228336   2098293228336
bb[0] = 99
print(bb)  # [99  2  3  4  5]
print(aa)  # [99  2  3  4  5]

print()
cc = np.copy(aa)   # 복사본 별도 생성
print(aa)
print(cc)
cc[0] = 77 
print(aa)  # [99  2  3  4  5]
print(cc)  # [77  2  3  4  5]
print(id(aa), ' ', id(cc))  # 1627475084080   1627475364528

print('\n\2차원 배열의 인덱싱과 슬라이싱')
dd = np.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]
])
print(dd, '\n', dd.shape)   # (3, 4)
print("인덱싱 ---")
print(dd[0])     # 0번째행 열 요소값 모두 출력
print(dd[0, 0])
print(dd[2, 3])

print("슬라이싱 ---")
print(dd[0:2])    # 0행 이상 2행 미만
print(dd[1:])     # 0행 이상 모든 출력
print(dd[:, 0])   # 모든 행 0번째 열    [1 5 9]  
print(dd[:, [1]]) # 모든행의 1번열을 가져오되, 2차원 형태 유지 # [[2][6][10]]
print(dd[1:3, 1:3])  # 1행, 2행의 1열 2열 출력
print(dd[::])     # 모든행, 모든열 출력
print(dd[::2, :])   # 0행, 2행의 모든열 출력
print(dd[::, ::2])  # 모든행, 0열,2열 출력
print(dd[::2, ::2]) # 0행, 2행의 0열,2열 출력

print(dd[-1, -1]) # 마지막행, 마지막 열 값 1개 출력 : 12
print(dd[-1])     # 마지막행
print(dd[:, -1])  # 모든행의 마지막열 출력
print(dd[::-1])     # 행역순
print(dd[:, ::-1])  # 열역순