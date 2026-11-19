# 힙(Heap)은 여러 개의 값 중에서 최댓값이나 최솟값을 빠르게 찾아내기 위해 고안된 
# 완전 이진 트리(Complete Binary Tree) 기반의 자료구조

# 내부 구현 없이 라이브러리로 Heap 처리
import heapq     # 기본이 Min Heap

# Min Heap
heap_li = []

heapq.heappush(heap_li, 30)
heapq.heappush(heap_li, 10)
heapq.heappush(heap_li, 20)
print('현재 힙 상태 : ', heap_li)   # [10, 30, 20] 내부적으로 힙 구조 유지

# 최소값 꺼내기
print('가장 작은 값 : ', heapq.heappop(heap_li))
print('가장 작은 값 : ', heapq.heappop(heap_li))
print('남은 값 : ', heap_li)

print()
# Max Heap
heap_li2 = []

heapq.heappush(heap_li2, -30)  # Max Heap으로 사용하기 위한 trick (-를 붙임)
heapq.heappush(heap_li2, -10)
heapq.heappush(heap_li2, -20)
print('현재 힙 상태 : ', heap_li2)   # [10, 30, 20] 내부적으로 힙 구조 유지

# 최대값 꺼내기
print('가장 큰 값 : ', -heapq.heappop(heap_li2))
print('가장 큰 값 : ', -heapq.heappop(heap_li2))
print('남은 값 : ', heap_li2)