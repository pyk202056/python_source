# 삽입(insertion) 정렬 : 앞에서 부터 하나씩 꺼내, 자기자리 찾아 끼워넣는 정렬
# 자료 배열의 모든 요소를 앞에서부터 차례대로 이미 정렬된 부분집합과 비교하여, 자신의 위치를 찾아 삽입하여 정렬하는 알고리즘

# 방법1 : 이해용 - 추가 공간이 있음
def find_ins_idx(r, v):
    for i in range(0, len(r)):
        # v 값이 i번 위치값 보다 작으면
        if v < r[i]:
            return i

    # 적정한 위치를 못찾은 경우 맨 뒤에 삽입
    return len(r)

def ins_sort(a):
    result = []
    while a:
        value = a.pop(0)
        ins_idx  = find_ins_idx(result, value)
        result.insert(ins_idx, value)
        print('a(d) : ', a)
        print('result : ', result)

    return result

d = [2,4,5,1,3]
# print(find_ins_idx(d, 1))
print(ins_sort(d))

print('-------------')
# 방법2 : 일반적 - 추가 공간이 거의 없음
def ins_sort2(a):
    n = len(a)
    for i in range(1, n):   # 두번째값(index 1)부터 끝까지 차례대로 삽입대상 선택
        key = a[i]
        j = i - 1  # j를 i바로 왼쪽 위치로 저장

        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]  # 삽입할 공간이 생기도록 값을 우측으로 밀기
            j -= 1  # 그 다음 왼쪽으로 이동하면서 다시 비교
        a[j + 1] = key  # 찾은 삽입 위치에 key를 저장
        print(a, '---')

d = [2,4,5,1,3]
ins_sort2(d)
print(d)

"""
수행 순서
1) i=1, key=4   2보다 크니까 그대로    [2,4,5,1,3]
2) i=2, key=5   2,4보다 크니까 그대로  [2,4,5,1,3]
3) i=3, key=1   2,4,5보다 작으니까 전부 우측으로 밀고 2앞에 (j번째에)1삽입  [1,2,4,5,3]
3) i=4, key=3   4,5보다 작으니까 두개 우측으로 밀고 4앞에 (j번째에)3삽입  [1,2,3,4,5]
"""