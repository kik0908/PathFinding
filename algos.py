from collections import deque


def dfd(graph, root, dot=None):  # Поиск дистанции в глубину в графе
    flag = False
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

            if dot is not None:
                if dot in distances:
                    flag = True
                    break
        if flag is True:
            break

    return distances


def bfd(graph, root, end=None):  # Поиск дистанции в ширину в графе
    flag = False
    distances = {}
    distances[root] = 0
    q = deque([root])
    while q:
        current = q.popleft()
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                q.append(neighbor)

            if end is not None:
                if end in distances:
                    flag = True
                    break
        if flag is True:
            break

    return distances


def path_finding_bfd(start, end, graph):
    finaly_path = [end]
    distances = sorted(bfd(graph, start, end).items(), key=lambda x: (x[1], x[0]), reverse=True)
    count = distances[0][-1]
    for i, j in enumerate(distances):
        if j[1] < count:
            distances = distances[i:]
            break
    while count != 0:
        count -= 1
        for i, j in enumerate(distances):
            if j[-1] != count:
                # print(12, i, j)
                distances = distances[i:]
                break
            if end in graph[j[0]]:
                # print(13, i, j)
                end = j[0]
                for l, k in enumerate(distances):
                    if k[-1] < count:
                        distances = distances[l:]
                        break
                break

        finaly_path.append(end)

    if len(set(finaly_path)) == 1:
        return None
    return finaly_path


def path_finding_bfd_iter(start, end, graph):
    finaly_path = [end]
    distances = sorted(bfd(graph, start, end).items(), key=lambda x: (x[1], x[0]), reverse=True)
    count = distances[0][-1]
    for i, j in enumerate(distances):
        if j[1] < count:
            distances = distances[i:]
            break
    while count != 0:
        count -= 1
        for i, j in enumerate(distances):
            if j[-1] != count:
                distances = distances[i:]
                break

            yield j[0]
            if end in graph[j[0]]:
                end = j[0]
                for l, k in enumerate(distances):
                    if k[-1] < count:
                        distances = distances[l:]
                        break
                break

        finaly_path.append(end)

    if len(set(finaly_path)) == 1:
        return None
    return finaly_path


def create_graph(matrix, with_diagonal=False):
    graph = {}
    w = len(matrix[0])
    h = len(matrix)

    for num in range(w * h):
        graph[num] = []
        i, j = num // w, num % w

        if matrix[i][j] != 0:
            continue

        if i - 1 >= 0:
            if matrix[i - 1][j] == 0:
                graph[num].append(num - w)
        if i + 1 < h:
            if matrix[i + 1][j] == 0:
                graph[num].append(num + w)

        if j - 1 >= 0:
            if matrix[i][j - 1] == 0:
                graph[num].append(num - 1)
        if j + 1 < w:
            if matrix[i][j + 1] == 0:
                graph[num].append(num + 1)

        if with_diagonal:
            if i - 1 >= 0 and j - 1 >= 0:
                if matrix[i - 1][j - 1] == 0:
                    graph[num].append(num - w - 1)
            if i + 1 < h and j - 1 >= 0:
                if matrix[i + 1][j - 1] == 0:
                    graph[num].append(num + w - 1)

            if i - 1 >= 0 and j + 1 < w:
                if matrix[i - 1][j + 1] == 0:
                    graph[num].append(num - w + 1)
            if i + 1 < h and j + 1 < w:
                if matrix[i + 1][j + 1] == 0:
                    graph[num].append(num + w + 1)

    return graph


graph = {1: [2, 3],
         2: [4],
         3: [4, 5],
         4: [3, 6, 5, 1, 7],
         5: [6, 2],
         6: [7],
         7: [1, 2]}

graph1 = {1: [6, 5, 8, 2, 7],
          2: [1, 8, 3],
          3: [2, 7, 4],
          4: [3, 8],
          5: [1, 6, 7],
          6: [1, 5],
          7: [1, 5, 3, 9],
          8: [1, 2],
          9: [7, 10],
          10: [9]}

graph2 = {1: [2, 3],
          2: [4],
          3: [5],
          4: [6, 7],
          5: [6],
          6: [5, 4],
          7: []}

matrix1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
           ]

# path = path_finding_bfd(1, 7, graph2)
# if path is not None:
#     print(' -> '.join(map(str, reversed(path))))
# else:
#     print(None)
#
# graph_0 = create_graph(matrix1)
# path = path_finding_bfd(0, 12, graph_0)
# if path is not None:
#     print(' -> '.join(map(str, reversed(path))))
# else:
#     print(None)
