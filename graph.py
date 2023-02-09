class Vertex():                              # Вершина графа   
    def __init__(self, name, x=None, y=None):
        self.name = name                        # имя должно быть уникальным, т.к. оно будет использоваться в качестве ключа для словаря содержащего все вершины графа
        self.x = x
        self.y = y

    def set_xy(self, x, y):
        self.x = x
        self.y = y      

    def get_xy(self):
        return self.x, self.y     

    def __repr__(self):
        if self.x and self.y:
            return f'{self.name} at ({self.x:.1f}, {self.y:.1f})'
        else:
            return self.name


class Edge():                               # Ребро графа
    def __init__(self, u, v, weight):       # u, v - Vertex names
        self.u = u
        self.v = v
        self.weight = weight
        self._weight = weight
        self.orientation = None

    def reversed(self):
        return Edge(self.v, self.u, self.weight)

    def restore_weight(self):
        self.weight = self._weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f"Edge [{self.u} -> {self.v}] (w={self.weight})"
      
      
    
class Graph():
    def __init__(self, vertex_dict):
        self.vertex_dict = vertex_dict
        self.edge_dict = {key: [] for key in vertex_dict.keys()}     # !!! выражение dict.fromkeys(vertex_dict.keys(), value=[]) создаёт словарь, все элементы которого ссылаются на один и тотже пустой список


    def add_vertex(self, key, value=None):
        assert not(key in self.vertex_dict.keys()), 'vertex key already exists' 
        self.vertex_dict[key] = value
        self.edge_dict[key] = []            # element of dict is list of edges


    def add_edge(self, edge):
        if not(edge.u in self.edge_dict.keys()):
            self.edge_dict[edge.u] = []
        if not(edge.v in self.edge_dict.keys()):
            self.edge_dict[edge.v] = []

        self.edge_dict[edge.u].append(edge)
        self.edge_dict[edge.v].append(edge.reversed())


    def add_edge_by_indice(self, u, v, weight):
        edge = Edge(u, v, weight)
        self.add_edge(edge)


    def get_edge_by_indice(self, u, v):
        edge_list = self.edge_dict[u]
        for e in edge_list:
            if e.v == v:
                return e
        print(f'NO EDGE FIND for vertexes {u, v}')


    def neighbors_for_vertex(self, vertex_name):
        return self.edge_dict[vertex_name]
      
      
class Node():                               # Структура необходимая для реализации поиска по графу
    def __init__(self, vertex, distance, prev_node=None):
        self.vertex = vertex
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __eq__(self, other):
        return self.distance == other.distance
      
      
from heapq import heappush, heappop

class PriorityQueue():          # приоритезированная очередь - структура необходимая для реализации поиска по графу
    def __init__(self):
        self._container = []

    @property
    def empty(self):
        return not self._container  

    def push(self, item):
        heappush(self._container, item)

    def pop(self):
        return heappop(self._container)

    def __repr__(self):
        return repr(self._container)
