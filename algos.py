from collections import deque


def dfd(graph, root): # Поиск дистанции в глубину
    distances = {}
    distances[root] = 0

    s = [root]
    while s:
        current = s.pop()
        for neighbor in graph[current]:
            _ = distances[current] + 1
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                s.append(neighbor)
            if _ < distances[neighbor]:
                distances[neighbor] = _

    return distances


def bfd(graph, root):  # Поиск дистанции в ширину
    distances = {}
    distances[root] = 0
    q = deque([root])
    while q:
        current = q.popleft()
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                q.append(neighbor)
    return distances


graph = {1: [2, 3],
         2: [4],
         3: [4, 5],
         4: [3, 6, 5, 1, 7],
         5: [6, 2],
         6: [7],
         7: [1, 2]}
print(*sorted(bfd(graph, 3).items()))
print('---')
print(*sorted(dfd(graph, 3).items()))
