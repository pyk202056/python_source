# 순차 탐색으로 특정 값의 위치 확인
def searchFunc(aa, x):
    n = len(aa)
    for i in range(0, n):
        if x == aa[i]:
            return i  # 같으면 인덱스 i를 반환

    return -1

values = [17, 92, 18, 33, 55, 7, 32, 44] 
print(searchFunc(values, 18))
print(searchFunc(values, 11))
print(searchFunc(values, 44))


print('\n정렬 알고리즘 --------') 
# 리스트나 배열에 담긴 원소들을 특정한 순서(오름차순, 내림차순, 사전순 등)에 따라 새로 배열하는 알고리즘
# 정렬1) 선택 정렬 (Selection Sort)
# : 전체 데이터 중 가장 작은(또는 큰) 원소를 찾아 맨 앞과 교환하는 방식.
# 방법1 : 이해 위주
def find_min_idx(a):
    n = len(a)
    min_idx = 0
    for i in range(1, n):
        if a[i] < a[min_idx]:
            min_idx = i

    return min_idx

def sel_sort(a):
    result = []   # d의 자료가 정렬되어 저장될 기억장소
    while a:
        min_idx = find_min_idx(a)
        value = a.pop(min_idx)
        result.append(value)

    return result

d = [2,4,5,1,3]
# print(find_min_idx(d))
print(sel_sort(d))


# 방법2 : 일반적인 방법 - 정렬 결과를 result 같은 기억장소 없이 자체 해결
def sel_sort2(a):
    n = len(a)
    for i in range(0, n - 1):   # 0부터 n - 2회 반복
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j

        a[i], a[min_idx] = a[min_idx], a[i]   # 찾은 작은 값을 i번 위치로 이동

d = [2,4,5,1,3]
sel_sort2(d)
print(d)