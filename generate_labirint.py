import collections


def bfs(g1, root, end):
    queue = collections.deque([root])
    used[root] = str(root+1)
    while queue:
        vertex = queue.popleft()
        for neighbour in g1[vertex]:
            print(g1[vertex])
            if used[neighbour] == "":
                used[neighbour] = used[vertex] + " " + str(neighbour+1)
                queue.append(neighbour)

                if neighbour + 1 == end:
                    break


graph = []
n = int(input())
g = [[] for _ in range(n)]
used = ["" for _ in range(n)]
for i in range(n):
    a = list(map(int, input().split()))
    graph.append(a)
for i in range(n):
    for j in range(n):
        if graph[i][j] == 1:
            g[i].append(j)
a, b = list(map(int, input().split()))
path = [a]
bfs(g, a - 1, b)
ln = len(used[b-1].split())-1
print(ln)
if ln > 0:
    print(used[b-1])