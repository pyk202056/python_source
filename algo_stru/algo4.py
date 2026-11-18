# 병합정렬(Merge sort)
# 대표적인 분할 정복(Divide and Conquer) 기반의 정렬 알고리즘입니다.
# 핵심 동작 방식
# 1. 분할 (Divide): 정렬할 전체 리스트를 원소가 1개 또는 0개가 될 때까지 절반(2개)으로 계속 쪼갭니다.
# 2. 정복 (Conquer): 쪼개진 부분 리스트를 각각 재귀적으로 정렬.
# 3. 결합 (Combine): 정렬된 두 개의 부분 리스트를 하나의 정렬된 리스트로 병합.

# 방법1 : 이해 위주
# 전체 흐름
# 1) 리스트를 반으로 나눔. 1개씩 남을 때까지 계속
# 2) 각각 다시 merge_sort() 함수로 정렬
# 3) 정렬된 두 리스트를 하나로 합친다.(merge)
#    이 때 합치면서 정렬된 상태를 유지한다.

def merge_sort(a):
    n = len(a)

    if n <= 1:
        return a

    mid = n // 2   # 중간을 기준으로 두 그룹으로 분할

    # 참고 : 함수는 독립적인 공간을 갖음. 아래의 g1, g2는 서로 불간섭
    g1 = merge_sort(a[:mid])   # 재귀
    print(f'g1 : {id(g1)}, {g1}')
    g2 = merge_sort(a[mid:])   # 재귀
    print(f'g2 : {id(g2)}, {g2}')

    # 두 그룹을 하나로 병합하기 위한 기억장소를 뱔도 사용
    result = []

    while g1 and g2:
        print(g1[0], ' ', g2[0])
        if g1[0] < g2[0]:
            result.append(g1.pop(0))
        else:
            result.append(g2.pop(0))

    # g1과 g2 중 소진된 것은 skip
    while g1:
        result.append(g1.pop(0))

    while g2:
        result.append(g2.pop(0))

    return result

d = [6,8,3,1,2,4,7,5]
print(merge_sort(d))

print('-------------------')
# 방법2 : 일반 알고리즘
# 재귀호출이 정렬된 리스트를 반환
# 병합도 새 리스트를 만들어 반환
# 원본 리스트는 그대로이고 정렬된 결과는 새 리스트에 저장
def merge_sort2(a):
    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort2(a[:mid])
    print(f'left:{id(left)}, {left}')

    right = merge_sort2(a[mid:])
    print(f'right:{id(right)}, {right}')

    result = []
    i = j = 0

    # 병합  
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 남은 요소 추가
    result += left[i:]
    result += right[j:]
    return result

print()
d = [6,8,3,1,2,4,7,5]
sorted_d = merge_sort2(d)
print(sorted_d)