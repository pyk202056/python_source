# 퀵 정렬(Quicksort)은 분할 정복(Divide and Conquer) 기반의 정렬 알고리즘입니다.

# 기본 동작 방식
# 1. 피벗(Pivot) 선택: 배열 안에서 하나의 원소(기준점)를 고릅니다 
#    (예: 첫 번째, 마지막, 중앙값, 또는 랜덤 값).
# 2. 분할 (Partition): 피벗을 기준으로 작은 값은 왼쪽으로, 큰 값은 오른쪽으로 재배치합니다. 이 과정이 끝나면 피벗은 최종 정렬 위치에 고정됩니다.
# 3. 재귀 (Recursion): 피벗으로 인해 나눠진 왼쪽 부분 배열과 오른쪽 부분 배열에 대해 동일한 과정을 재귀적으로 반복합니다.
# 4. 종료: 부분 배열의 크기가 0이나 1이 되면 정렬이 완료됩니다.

# 하나의 기준점을 중심으로 작은값과 큰값을 나눠서 각각 정렬 후
# 마지막에 이어 붙이는 방법
# g1:기준값 보다 작은 그룹 + 기준값 + g2:기준값 보다 큰 그룹

# 방법1 : 이해 위주
def quick_sort(a):
    n = len(a)
    if n <= 1:
        return a

    # 기준값(pivot) : 편의상 가장 마지막 값을 취함
    pivot = a[-1]

    g1 = []  # pivot 보다 작은 그룹
    g2 = []  # pivot 보다 큰 그룹

    for i in range(0, n - 1):
        if a[i] < pivot:
            g1.append(a[i])
        else:
            g2.append(a[i])

    print(f'g1({id(g1)}) : {g1}')
    print(f'g2({id(g2)}) : {g2}')
    return quick_sort(g1) + [pivot] + quick_sort(g2)

d = [6,8,3,1,2,4,7,5]
print(quick_sort(d))

print('---------')
# 방법2 : 일반 알고리즘
def quick_sort2_sub(a, start, end):
    # 종료 조건 : 정렬 대상이 한 개 이하이면 정렬X
    if end - start <= 0:
        return

    pivot = a[end]
    i = start
    for j in range(start, end):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            print(f'{a[i]}, {a[j]} = {a[j]}, {a[i]}')
            i += 1

    a[i], a[end] = a[end], a[i]
    print(f'{a[i]}, {a[end]} = {a[end]}, {a[i]}')

    quick_sort2_sub(a, start, i - 1)   # 기준값 보다 작은 그룹을 재귀로 다시 정렬
    quick_sort2_sub(a, i + 1, end)     # 기준값 보다 큰 그룹을 재귀로 다시 정렬

def quick_sort2(a):
    quick_sort2_sub(a, 0, len(a) - 1)  # 자료, 시작인덱스, 끝인덱스

d = [6,8,3,1,2,4,7,5]
quick_sort2(d)
print(d)