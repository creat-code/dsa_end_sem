class Graph:
    def __init__(self, is_weighted=True):
        self.adjacency = {}
        self.is_weighted = is_weighted

    def add_city(self, city):
        if city not in self.adjacency:
            self.adjacency[city] = []

    def add_road(self, city1, city2, distance=1):
        self.add_city(city1)
        self.add_city(city2)
        self.adjacency[city1].append((city2, distance))
        self.adjacency[city2].append((city1, distance))

    def remove_city(self, city):
        if city in self.adjacency:
            del self.adjacency[city]
            for neighbors in self.adjacency.values():
                neighbors[:] = [tup for tup in neighbors if tup[0] != city]

    def remove_road(self, city1, city2):
        if city1 in self.adjacency:
            self.adjacency[city1] = [tup for tup in self.adjacency[city1] if tup[0] != city2]
        if city2 in self.adjacency:
            self.adjacency[city2] = [tup for tup in self.adjacency[city2] if tup[0] != city1]

    def get_graph(self):
        return self.adjacency