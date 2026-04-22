import heapq
from collections import deque


def bubble_sort(values):
    arr = values[:]
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(values):
    arr = values[:]
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(values):
    arr = values[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(values):
    arr = values[:]

    def _merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        merged = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return _merge_sort(arr)


def quick_sort(values):
    arr = values[:]

    def _quick_sort(a, low, high):
        if low < high:
            p = _partition(a, low, high)
            _quick_sort(a, low, p - 1)
            _quick_sort(a, p + 1, high)

    def _partition(a, low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[high] = a[high], a[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def build_undirected_adj(n, edges):
    adj = [[] for _ in range(n)]
    for edge in edges:
        if len(edge) == 2:
            u, v = edge
            w = 1
        else:
            u, v, w = edge
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def bfs(n, edges, start):
    adj = build_undirected_adj(n, edges)
    visited = [False] * n
    order = []
    q = deque([start])
    visited[start] = True

    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)

    return order


def dfs(n, edges, start):
    adj = build_undirected_adj(n, edges)
    visited = [False] * n
    order = []

    def _dfs(u):
        visited[u] = True
        order.append(u)
        for v, _ in adj[u]:
            if not visited[v]:
                _dfs(v)

    _dfs(start)
    return order


def dijkstra(n, edges, start):
    adj = build_undirected_adj(n, edges)
    inf = float("inf")
    dist = [inf] * n
    parent = [-1] * n
    dist[start] = 0

    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    normalized_dist = [None if x == inf else x for x in dist]
    return {"distances": normalized_dist, "parents": parent}


def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for c in range(capacity + 1):
            if weights[i - 1] <= c:
                dp[i][c] = max(dp[i - 1][c], values[i - 1] + dp[i - 1][c - weights[i - 1]])
            else:
                dp[i][c] = dp[i - 1][c]

    chosen = []
    i = n
    c = capacity
    while i > 0 and c >= 0:
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
        i -= 1

    chosen.reverse()
    return {
        "max_profit": dp[n][capacity],
        "chosen_items": chosen,
        "table": dp,
    }


def lcs(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i, j = m, n
    subseq_chars = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            subseq_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    subseq_chars.reverse()
    subseq = "".join(subseq_chars)

    return {
        "length": dp[m][n],
        "subsequence": subseq,
        "table": dp,
    }
