
from collections import deque
import sys


class Graph:
    """
    Класс Graph представляет собой  граф с вершинами и рёбрами
    """

    def __init__(self):
        """
        Инициализирует граф с пустым словарём для хранения вершин и их связей.
        """
        self.graph = {}

    def add_vertex(self, vertex):
        """
        Добавляет вершину в граф.


        """
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start, end):
        """
        Добавляет ребро в граф, соединяя две вершины с заданным весом.


        """
        if start in self.graph and end in self.graph:
            self.graph[start].append(end)

    def remove_vertex(self, vertex):
        """
        Удаляет вершину из графа.


        """
        if vertex in self.graph:
            del self.graph[vertex]
            for vertices in self.graph.values():
                if vertex in vertices:
                    vertices.remove(vertex)

    def remove_edge(self, start, end):
        """
        Удаляет ребро между двумя вершинами в графе.


        """
        if start in self.graph:
            self.graph[start].remove(end)

    def has_path(self, start, end):

        visited = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == end:
                return True
            if current not in visited:
                visited.add(current)
                stack.extend(self.graph[current])
        return False

    def has_cycle(self):
        """
        Определяет наличие в графе циклов с помощью алгоритма dfs. Возвращает True если находит петли и False если нет
        """
        visited = set()
        stack = set()

        def dfs(vertex):
            if vertex in stack:
                return True
            if vertex in visited:
                return False

            visited.add(vertex)
            stack.add(vertex)
            for neighbor in self.graph.get(vertex, []):
                if dfs(neighbor):
                    return True
            stack.remove(vertex)
            return False

        for vertex in self.graph:
            if dfs(vertex):
                return True
        return False

    def shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None

        parents = {}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current == end:
                path = []
                while current != start:
                    path.insert(0, current)
                    current = parents.get(current)
                path.insert(0, start)
                return path

            for neighbor in self.graph[current]:
                if neighbor not in parents:
                    parents[neighbor] = current
                    queue.append(neighbor)

        return None


class DirectedGraph(Graph):
    """
    Класс DirectedGraph представляет собой ориентированный граф
    """

    def add_edge(self, start, end):
        if start in self.graph:
            self.graph[start].append(end)
        """
        Добавляет ребро в граф, соединяя две вершины в ориентированном графе.

        
        """


class UndirectedGraph(Graph):
    """
    Класс UndirectedGraph представляет собой неориентированный граф
    """

    def add_edge(self, start, end):
        """
        Добавляет ребро в граф, соединяя две вершины в неориентированном графе.


        """
        if start in self.graph:
            self.graph[start].append(end)
        if end in self.graph:
            self.graph[end].append(start)


class WeightedGraph(Graph):
    """
    Класс WeightedGraph представляет собой взвешенный граф
    """

    def __init__(self):
        """
        Инициализирует граф с пустым словарём для хранения вершин и их связей и пустым словарем весов ребер.
        """
        super().__init__()
        self.weights = {}

    def add_edge(self, start, end, weight):
        if start in self.graph:
            self.graph[start].append(end)
            self.weights[(start, end)] = weight
        """
        Добавляет ребро в граф, соединяя две вершины с заданным весом.

        ]
        """

    def shortest_distance(self, start, end):
        """
        Находит кратчайшее растояние между двумя вершинами с использованием алгоритма Дейкстры.

        \

        Возвращает:
        Кратчайшее растояние c учетом весов  между начальной и конечной вершинами в виде списка вершин.
        """
        n = len(self.graph)
        #   used = [False] * n
        used = {}
        distances = {}
        for i in self.graph:
            distances[i] = sys.maxsize
        distances[start] = 0

        for _ in range(n):
            min_distance = sys.maxsize
            min_index = -1
            for i in self.graph:
                if i not in used and distances[i] < min_distance:
                    min_distance = distances[i]
                    min_index = i

            if min_index == -1:
                break

            used[min_index] = True

            for j in self.graph:
                if (min_index, j) in self.weights:
                    new_distance = distances[min_index] + self.weights[(min_index, j)]
                    if new_distance < distances[j]:
                        distances[j] = new_distance

        return distances[end] if distances[end] != sys.maxsize else -1
