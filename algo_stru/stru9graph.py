# Graph : Node(vertex)와 Edge의 집합으로 이루어진 자료구조

# Tree : 계층구조, Root 있음, 사이클(순환) 없음, 항상 연결
# Graph: 일반 네트워크 구조, Root 없음, 사이클(순환) 있음, 연결/비연결 모두 가능

graph = {
    'A':('B', 'C'),
    'B':('D', 'E'),
    'C':('F'),
    'D':(),
    'E':(),
    'F':()
}

# DFS : 깊이 우선 탐색 방식 - 재귀 또는 스텍으로 구현 - 경로 추적, 백트레킹에 적합
def dfsFunc(graph, start, visited):
    visited.append(start)    # 현재 노드 방문 기록 저장
    for next_node in graph[start]:   # 이웃 노드 탐색 : 현재 노드(start)에 인접한 노드를 하나씩 확인
        if next_node not in visited:  # 아직 방문하지 않은 노드라면
            dfsFunc(graph, next_node, visited)  # 재귀 (현재 길을 끝까지 내려가며 탐색)

visited_dfs = []   # 방문 순서 저장용
dfsFunc(graph, 'A', visited_dfs)
print('DFS 방문 순서 : ', visited_dfs)  
# ['A', 'B', 'D'(끝), 'E'(끝), 'C', 'F'(끝)]

print()
# BFS : 너비 우선 탐색 방식 - Queue로 구현 - 최단 거리 탐색에 적합
from collections import deque
def bfsFunc(graph, start):
    visited = [start]
    queue = deque([start])    # 큐(FIFO 구조) - 탐색 대기열

    while queue:
        node = queue.popleft()  # 가장 먼저 들어온 노드 꺼냄
        for next_node in graph[node]:    # 현재 노드와 이웃 노드 확인
            if next_node not in visited:
                visited.append(next_node)  # 방문 처리
                queue.append(next_node)  # 다음 탐색 대상으로 큐에 추가

    return visited

visited_bfs = bfsFunc(graph, 'A')
print('BFS 방문 순서 : ', visited_bfs) 
# ['A', 'B', 'C', 'D', 'E', 'F']
# A -> B, C -> D, E, F 방문 즉시 큐에 쌓고, 먼저 들어온 것부터 처리(거리<레벨 개념이 생김)