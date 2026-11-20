# A*알고리즘(에이스타 알고리즘)은 출발 노드에서 목표 노드까지의 최단 경로를 
# 빠르게 찾는 그래프 탐색 알고리즘입니다. 
# 다익스트라 알고리즘에 목표 지점까지의 추정 비용(휴리스틱)을 더해 탐색 범위를 줄입니다.

# 핵심 공식
# 각 노드의 우선순위는 평가 함수 f(n)으로 결정합니다.
# • f(n) = g(n) + h(n)
# • g(n): 출발 노드에서 현재 노드 n까지의 실제 이동 비용
# • h(n): 현재 노드 n에서 목표 노드까지의 추정 비용(휴리스틱, 예: 맨해튼 거리, 유클리드 거리)

# 동작 방식
# 1. 출발 노드를 열린 목록(Open List)에 넣고 시작합니다.
# 2. 열린 목록에서 f(n) 값이 가장 작은 노드를 선택합니다.
# 3. 해당 노드가 목표 노드면 탐색을 종료하고 경로를 반환합니다.
# 4. 목표가 아니면 현재 노드를 닫힌 목록(Closed List)으로 옮기고, 
# 인접 이동 가능 노드의 g, h, f 값을 계산해 열린 목록에 추가하거나 갱신합니다.
# 5. 목표에 도달하거나 열린 목록이 빌 때까지 2~4단계를 반복합니다.

import heapq

def astarFunc(graph, start, goal, h):
    pq = [(h[start], 0, start)]   # (f=g+h, g, 현재노드)   시작노드 초기화
    dist = {start:0}
    parent = {}   # 최단 경로 트리 복원을 위한 부모 노드 기록

    while pq:
        f, g, u = heapq.heappop(pq)  # f값이 가장 작은 노드(유망한 노드)를 꺼냄

        if u == goal:
            break

        for v, w in graph[u]:   # 현재 노드 u와 연결된 이웃 노드 v 탐색
            new_g = g + w       # 시작점 -> u -> v 까지의 실제 비용 계산
            if v not in dist or new_g < dist[v]:   # 아직 방문 안했거나 더 짧은 경로 발견시
                dist[v] = new_g   # v까지의 최단 실제 비용 갱신
                parent[v] = u     # v로 오기 직전 노드를 u로 기록(경로 복원용) 
                heapq.heappush(pq, (new_g + h[v], new_g, v))  # f = g + h 값으로 큐에 삽입

    # 경로 복원
    path = [goal]    # 목표 노드부터 역방향으로 경로 구성 시작
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path, dist[goal]    # 최단경로와 총비용 반환


graph = {  # 무방향 형태
    'A':[('B',1),('C',4)],  # A에서 B,C로 가는 가중치 간선 
    'B':[('A',1),('C',1),('D',2)],
    'C':[('A',4),('B',1),('D',3)],
    'D':[('B',2),('C',3)]
}

heuristic = {'A':3, 'B':2, 'C':1, 'D':0}  # 휴리스틱 h(n) : 목표 D까지의 예상 비용
path, cost = astarFunc(graph, 'A', 'D', heuristic)
print('A* 경로 : ', path)
print('총 비용 : ', cost)