# BST(Binary Search Tree, 이진탐색트리) 
# 중위 순회로 자료 정렬하기
# 각 노드 기준으로 left < node < right
# 왼쪽 서브트리 : 현재 노드보다 작은 값
# 오른쪽 서브트리 : 현재 노드보다 큰 값
# 입력 순성에 따라 트리 모양이 달라짐
# 이진트리는 구조만 있으나, BST 구조 + 정렬규칙이 있다.
# 중위순회(왼쪽 -> 현재 -> 오른쪽 순서로 방문)를 하면 오름차순 정렬됨

# BST 노드 정의
class Node:
    def __init__(self, key):
        self.key = key   # 노드가 저장 하는 값
        self.left = None    # 왼쪽 자식 노드(더 작은 값이 저장)
        self.right = None   # 오른쪽 자식 노드(더 큰 값이 저장)

# BST에 자료 삽입
def insert(root, key):
    if root is None:   # 현재 위치가 비워져 있으면
        return Node(key)  # 새 노드 생성 후 그 자리에 값 넣고 리턴

    if key < root.key:  # 넣을 값이 현재 노드보다 작으면
        root.left = insert(root.left, key)  # 왼쪽 노드에 재귀적으로 삽입
    else:
        root.right = insert(root.right, key)  #  오른쪽 노드에 재귀적으로 삽입

    return root

# 중위 순회(정렬 결과 생성) : Left -> Node -> Right
def inorder(root, result):
    if root is None:
        return    # 더 내려갈 노드가 없으면 함수 탈출

    inorder(root.left, result)    # 왼쪽 노드(작은 값) 방문
    result.append(root.key)       # 현재 노드값 추가
    inorder(root.right, result)   # 오른쪽 노드(큰 값) 방문

# values = [5, 3, 7, 2, 4, 9]
values = [9, 7, 5, 4, 3, 1]
root = None
for v in values:
    root = insert(root, v)    # BST에 삽입하고 루트(최상단) 갱신

# BST 정렬 결과 출력
sorted_result = []
inorder(root, sorted_result)
print('순회 결과 : ', sorted_result)