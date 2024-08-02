from functools import cache
import random

Vertex = int
Edge = tuple[Vertex, Vertex]
Weight = int
AdjacencyMatrix = dict[Edge, Weight]

def make_bidirectional(edges: AdjacencyMatrix) -> AdjacencyMatrix:
    return edges | {(v, u): w for (u, v), w in edges.items()}

class Graph:

    def __init__(self, n: int, edges: AdjacencyMatrix):
        self.n = n
        self.edges = edges

    @classmethod
    def mkrand(cls, n: int, *, connected: bool = True):
        if not connected: raise NotImplementedError()
        if n < 0: raise ValueError(n)
        g = cls(n, {})
        if n == 0: return g
        vertices = range(g.n)
        while not g.is_connected():
            u, v = random.sample(vertices, k=2)
            assert u != v
            g.edges[u, v] = 1
            g.edges = make_bidirectional(g.edges)
        return g

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
        return visited == set(range(self.n))


def floyd_warshall(g: Graph) -> AdjacencyMatrix:

    vertices = range(g.n)
    dist: AdjacencyMatrix = {(i, j): float('inf')
                             for i in vertices for j in vertices}
    for edge, weight in g.edges.items():
        u, v = edge
        dist[u, v] = weight
    for v in vertices:
        dist[v, v] = 0
    for k in vertices:
        for i in vertices:
            for j in vertices:
                w = dist[i, k] + dist[k, j]
                if w < dist[i, j]:
                    dist[i, j] = w
                continue
                try:
                    w = dist[i, k] + dist[k, j]
                except TypeError:
                    continue
                try:
                    if w < dist[i, j]:
                        dist[i, j] = w
                except TypeError:
                    dist[i, j] = w

    return dist


def floyd_warshall2(g: Graph) -> AdjacencyMatrix:
    vertices = range(g.n)
    return {(i, j): shortestPath(g.edges, i, j, g.n)
            for i in vertices for j in vertices}


# @cache
def shortestPath(edges: AdjacencyMatrix, i: Vertex, j: Vertex, k: int) -> Weight:
    if k == 0:
        return 0 if i == j else edges.get((i, j), float('inf'))

    a = shortestPath(edges, i, j, k - 1)
    b = shortestPath(edges, i, k, k - 1)
    c = shortestPath(edges, k, j, k - 1)
    # if b + c < a:
        # print(f'At {k = }, found path from {i} to {j} of length {b + c}, which is shorter than {a}')
    return min(a, b + c)

    return min(  shortestPath(edges, i, j, k - 1),
                 shortestPath(edges, i, k, k - 1)
               + shortestPath(edges, k, j, k - 1))


def render(n: int, dist: AdjacencyMatrix) -> str:
    render_weight = str
    w = max(len(render_weight(x)) for x in dist.values())
    lines = [
        ' '.join(render_weight(dist[i, j]).rjust(w)
                 for j in range(n)) for i in range(n)
    ]
    return '\n'.join(lines)


if __name__ == '__main__':

    n = 8

    edges = {
        (0, 2): 1,
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 1,
        (4, 2): 1,
        (4, 5): 1,
        (5, 6): 1,
        (1, 7): 1,
    }

    edges = make_bidirectional(edges)

    g = Graph(n, edges)
    assert g.is_connected()

    g = Graph(4, make_bidirectional({
        (0, 1): 1,
        (1, 2): 1,
        (2, 3): 1,
    }))

    # g = Graph.mkrand(4)
    g = Graph(4, make_bidirectional({(0, 1): 1, (0, 2): 1, (2, 3): 1}))
    print(g.is_connected())
    # print(g.edges)
    # print(render(g.n, g.edges))

    x = floyd_warshall(g)
    y = floyd_warshall2(g)

    print(g.edges, end='\n\n')
    print(render(g.n, x), end='\n\n')
    print(render(g.n, y), end='\n\n')
    if x != y:
        print('Algorithms differ!')

    # vertices = range(g.n)
    # for k in range(g.n+1):
    #     print(render(g.n, {(i, j): shortestPath(g.edges, i, j, k)
    #         for i in vertices for j in vertices}))
    #     print()
    exit()

    print(render(g.n, floyd_warshall2(g)))
