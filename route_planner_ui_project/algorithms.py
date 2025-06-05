import heapq
from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        visited.add(current)
        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)
    return None

def dijkstra(graph, start, goal):
    heap = [(0, start, [])]
    visited = set()
    while heap:
        cost, current, path = heapq.heappop(heap)
        if current in visited:
            continue
        path = path + [current]
        if current == goal:
            return path, cost
        visited.add(current)
        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path))
    return None, float('inf')