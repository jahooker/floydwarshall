from functools import cache
import random


class hashabledict(dict):

    def __hash__(self) -> int:
        return hash(frozenset(self.items()))


Vertex = int
Edge = tuple[Vertex, Vertex]
Weight = int
AdjacencyMatrix = hashabledict[Edge, Weight]


class Graph:

    def __init__(self, n: int = 0, edges: AdjacencyMatrix = AdjacencyMatrix()):
        self.n = int(n)
        self.edges = AdjacencyMatrix(edges)

    def __len__(self) -> int:
        return self.n

    def __iter__(self):
        return iter(self.vertices())

    def __bool__(self) -> bool:
        return bool(self.vertices())

    def vertices(self):
        return range(self.n)

    def __str__(self) -> str:
        render_value = str
        w = max(len(render_value(x)) for x in self.edges.values())
        lines = (' '.join(render_value(self.edges[i, j]).rjust(w) for j in self)
                 for i in self)
        return '\n'.join(lines)

    @classmethod
    def mkrand(cls, n: int, *, connected: bool = True):
        if not connected: raise NotImplementedError()
        if n < 0: raise ValueError(n)
        g = cls(n)
        if not g: return g
        while not g.is_connected():
            u, v = random.sample(g.vertices(), k=2)
            assert u != v
            g.edges[u, v] = 1
            g.edges = Graph.make_bidirectional(g.edges)
        return g

    @staticmethod
    def make_bidirectional(edges: AdjacencyMatrix) -> AdjacencyMatrix:
        return AdjacencyMatrix(edges | {(v, u): w for (u, v), w in edges.items()})

    def is_connected(self):
        if self.n < 0: raise ValueError(self.n)
        if self.n == 0: return True
        visited: set[Vertex] = {0}

        def search():
            return {v for u, v in self.edges
                    if  u     in visited
                    and v not in visited}

        while addenda := search():
            visited |= addenda
        return visited == set(self.vertices())


class FloydWarshall:

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def dp(cls, g: Graph) -> AdjacencyMatrix:
        # By dynamic programming
        vertices = range(g.n)
        dist = AdjacencyMatrix({(i, j): float('inf')
                                for i in g for j in g})
        for edge, weight in g.edges.items():
            u, v = edge
            dist[u, v] = weight
        for v in vertices:
            dist[v, v] = 0
        for k in range(g.n):
            for i in g:
                for j in g:
                    dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
        return dist

    @classmethod
    def recursive(cls, g: Graph) -> AdjacencyMatrix:
        # By recursion
        return {(i, j): cls.shortestPath(g.edges, i, j, g.n)
                for i in g for j in g}

    @classmethod
    @cache
    def shortestPath(cls, edges: AdjacencyMatrix, i: Vertex, j: Vertex, k: int) -> Weight:
        if k < 0: return int(i != j) and edges.get((i, j), float('inf'))
        return min(  cls.shortestPath(edges, i, j, k - 1),
                     cls.shortestPath(edges, i, k, k - 1)
                   + cls.shortestPath(edges, k, j, k - 1))


def demo():

    g = Graph(8, Graph.make_bidirectional({
        (0, 2): 1,
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 1,
        (4, 2): 1,
        (4, 5): 1,
        (5, 6): 1,
        (1, 7): 1,
    }))
    assert g.is_connected()

    g = Graph(4, Graph.make_bidirectional({
        (0, 1): 1,
        (1, 2): 1,
        (2, 3): 1,
    }))
    assert g.is_connected()

    g = Graph.mkrand(4)
    # g = Graph(4, Graph.make_bidirectional({(0, 1): 1, (0, 2): 1, (2, 3): 1}))

    x = FloydWarshall.dp(g)
    y = FloydWarshall.recursive(g)
    assert x == y, 'Algorithms differ!'

    print(g.edges, end='\n\n')
    print(Graph(g.n, x), end='\n\n')
    print(Graph(g.n, y), end='\n\n')


if __name__ == '__main__':

    demo()
