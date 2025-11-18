class SampleGraph:
    def __init__(self):
        self.adjacency_list: dict[int, list[int]] = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list:
            self.adjacency_list[vertex1].append(vertex2)
            self.adjacency_list[vertex2].append(vertex1)

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list:
            if vertex2 in self.adjacency_list[vertex1]:
                self.adjacency_list[vertex1].remove(vertex2)
            if vertex1 in self.adjacency_list[vertex2]:
                self.adjacency_list[vertex2].remove(vertex1)

    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            for adjacent in self.adjacency_list[vertex]:
                self.adjacency_list[adjacent].remove(vertex)
            del self.adjacency_list[vertex]

    def get_vertices(self):
        return list(self.adjacency_list.keys())

    def get_edges(self):
        edges = []
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                if (neighbor, vertex) not in edges:
                    edges.append((vertex, neighbor))
        return edges

    def is_connected(self):
        if not self.adjacency_list:
            return False

        visited = set()
        stack = [next(iter(self.adjacency_list))]

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(self.adjacency_list[vertex])

        return len(visited) == len(self.adjacency_list)
        
    def degree(self, vertex):
        return len(self.adjacency_list.get(vertex, []))

    def get_neighbors(self, vertex):
        return self.adjacency_list.get(vertex, [])